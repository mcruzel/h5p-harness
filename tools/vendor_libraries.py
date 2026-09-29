#!/usr/bin/env python3
"""Vendor H5P libraries (runtime, editor and sub-content options) from their sources.

The canonical source of H5P libraries is the H5P Hub (what Moodle's scheduled task
installs). When the Hub is unreachable, the registry used by the official h5p-cli
(github.com/h5p/h5p-registry) maps every library to its GitHub repository: this tool
resolves the full dependency closure, builds the libraries that need it (webpack) and
copies only the distributable files into vendor/libraries/<Machine>-<major>.<minor>/.

Usage:
    python tools/vendor_libraries.py                 # every runnable content type
    python tools/vendor_libraries.py H5P.MultiChoice # one type and its closure
"""
import argparse
import concurrent.futures as cf
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import io
import tarfile
import threading
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
REGISTRY = ROOT / "vendor" / "registry.json"
REGISTRY_EXTRA = ROOT / "vendor" / "registry-extra.json"
OUT = ROOT / "vendor" / "libraries"
LOCK = ROOT / "vendor" / "libraries.lock.json"
CACHE = Path(os.environ.get("H5P_HARNESS_CACHE", Path.home() / ".cache" / "h5p-harness"))

# H5PCore::$defaultContentWhitelist + $defaultLibraryWhitelistExtras (h5p-php-library)
ALLOWED_EXT = set(
    "json png jpg jpeg gif bmp tif tiff eot ttf woff woff2 otf webm mp4 ogg mp3 m4a wav txt pdf rtf doc "
    "docx xls xlsx ppt pptx odt ods odp csv diff patch swf md textile vtt webvtt gltf glb js css svg xml".split())
DEV_FILES = {"package.json", "package-lock.json", "yarn.lock", "composer.json", "tsconfig.json", "jsconfig.json",
             "README.md", "CONTRIBUTING.md", "CHANGELOG.md", "CODE_OF_CONDUCT.md", "SECURITY.md"}
DEV_FILE_RE = re.compile(r"^(webpack|karma|babel|eslint|postcss|jest|vite|rollup|gulpfile|gruntfile|\.?stylelint)"
                         r"[\w.-]*\.(js|mjs|cjs|json)$", re.I)
DEV_DIRS = {"node_modules", "test", "tests", "spec", "specs", "docs", "doc", "Documentation", "reports", "coverage",
            "dev", "demo", "examples", "worknotes", "cypress", "playwright"}
MAYBE_DEV_DIRS = {"src", "build", "scripts-src"}  # kept only when library.json references them
VERSION_TAG = re.compile(r"^v?(\d+)\.(\d+)\.(\d+)$")
PREFERRED_BRANCHES = ["release", "master", "main", "stable"]

log_lock = threading.Lock()


def log(msg):
    with log_lock:
        print(msg, flush=True)


def sh(cmd, cwd=None, timeout=900, env=None, check=True):
    res = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True, timeout=timeout,
                         env={**os.environ, **(env or {})})
    if check and res.returncode != 0:
        raise RuntimeError(f"{' '.join(cmd)} -> {res.returncode}\n{res.stdout[-2000:]}\n{res.stderr[-3000:]}")
    return res


class Repo:
    """Shallow, lazily fetched mirror of one GitHub repository."""

    def __init__(self, url):
        self.url = url
        slug = url.rstrip("/").split("github.com/")[-1].replace("/", "__")
        self.dir = CACHE / "src" / slug
        self.lock = threading.Lock()
        self._refs = None
        self.default = None

    def _git(self, *args, **kw):
        return sh(["git", "-C", str(self.dir), *args], **kw)

    def init(self):
        with self.lock:
            if self._refs is not None:
                return
            if not (self.dir / ".git").exists():
                self.dir.mkdir(parents=True, exist_ok=True)
                sh(["git", "init", "-q", str(self.dir)])
                self._git("remote", "add", "origin", self.url)
            out = sh(["git", "ls-remote", "--symref", self.url, "HEAD", "refs/heads/*", "refs/tags/*"],
                     timeout=120).stdout
            refs = {}
            for line in out.splitlines():
                if line.startswith("ref:"):
                    self.default = line.split()[1].replace("refs/heads/", "")
                    continue
                sha, name = line.split("\t")
                if name.endswith("^{}"):
                    continue
                refs[name] = sha
            self._refs = refs

    def candidates(self, major=None, minor=None):
        """Refs to try, most likely first."""
        self.init()
        heads = [r for r in self._refs if r.startswith("refs/heads/")]
        order = []
        if self._release_is_maintained():
            # H5P Group publishes to the Hub from "release"; the default branch may hold unreleased
            # (sometimes broken) work, e.g. h5p/timelinejs master redeclares LazyLoad as a const.
            order.append("refs/heads/release")
        if self.default:
            order.append(f"refs/heads/{self.default}")
        order += [f"refs/heads/{b}" for b in PREFERRED_BRANCHES if f"refs/heads/{b}" in self._refs]
        tags = []
        for r in self._refs:
            if r.startswith("refs/tags/"):
                m = VERSION_TAG.match(r[len("refs/tags/"):])
                if m and (major is None or (int(m[1]), int(m[2])) == (major, minor)):
                    tags.append(((int(m[1]), int(m[2]), int(m[3])), r))
        order += [r for _, r in sorted(tags, reverse=True)]
        if major is not None:
            order += sorted(heads)  # last resort: any branch
        seen, out = set(), []
        for r in order:
            if r not in seen:
                seen.add(r)
                out.append(r)
        return out

    def _release_is_maintained(self):
        """Prefer 'release' when it carries the same version as the default branch (what the Hub
        publishes; the default branch may hold unreleased work) or was updated within a year of it."""
        if self.default in (None, "release") or "refs/heads/release" not in self._refs:
            return False
        refs = (f"refs/heads/{self.default}", "refs/heads/release")
        try:
            versions = []
            for r in refs:
                lj = json.loads(self.show(r, "library.json") or "{}")
                versions.append((lj.get("majorVersion"), lj.get("minorVersion"), lj.get("patchVersion")))
            if versions[0] == versions[1] and versions[0][0] is not None:
                return True
            dates = [int(self._git("log", "-1", "--format=%ct", self.fetch(r)).stdout.strip()) for r in refs]
        except (RuntimeError, ValueError):
            return False
        return dates[0] - dates[1] < 365 * 24 * 3600

    def fetch(self, ref):
        local = "refs/cache/" + ref.split("/", 2)[-1]
        with self.lock:
            if self._git("rev-parse", "-q", "--verify", local, check=False).returncode != 0:
                self._git("fetch", "-q", "--depth", "1", "origin", f"+{ref}:{local}", timeout=600)
        return local

    def show(self, ref, path):
        res = self._git("show", f"{self.fetch(ref)}:{path}", check=False)
        return res.stdout if res.returncode == 0 else None

    def sha(self, ref):
        return self._git("rev-parse", self.fetch(ref)).stdout.strip()


def export_tree(repo: Repo, ref, dest: Path):
    if dest.exists():
        shutil.rmtree(dest)
    dest.mkdir(parents=True)
    proc = subprocess.run(["git", "-C", str(repo.dir), "archive", "--format=tar", repo.fetch(ref)],
                          capture_output=True, timeout=600, check=True)
    with tarfile.open(fileobj=io.BytesIO(proc.stdout)) as tar:
        tar.extractall(dest, filter="data")


def library_paths(lib_json):
    for key in ("preloadedJs", "preloadedCss"):
        for item in lib_json.get(key, []):
            yield item["path"]


def needs_build(tree: Path, lib_json):
    return any(not (tree / p).exists() for p in library_paths(lib_json))


def build(tree: Path, name):
    pkg = json.loads((tree / "package.json").read_text()) if (tree / "package.json").exists() else {}
    if "build" not in pkg.get("scripts", {}):
        raise RuntimeError("fichiers compilés absents et aucun script npm 'build'")
    env = {"CI": "1", "npm_config_update_notifier": "false", "npm_config_fund": "false",
           "npm_config_audit": "false", "HUSKY": "0"}
    install = ["npm", "ci"] if (tree / "package-lock.json").exists() else ["npm", "install"]
    try:
        sh(install + ["--loglevel=error"], cwd=tree, env=env)
    except RuntimeError:
        sh(["npm", "install", "--legacy-peer-deps", "--loglevel=error"], cwd=tree, env=env)
    try:
        sh(["npm", "run", "build"], cwd=tree, env=env)
    except RuntimeError as e:
        if "ERR_OSSL_EVP_UNSUPPORTED" in str(e) or "digital envelope" in str(e):
            sh(["npm", "run", "build"], cwd=tree, env={**env, "NODE_OPTIONS": "--openssl-legacy-provider"})
        else:
            raise


def h5pignore(tree: Path):
    f = tree / ".h5pignore"
    if not f.exists():
        return set()
    return {line.strip().strip("/") for line in f.read_text().splitlines()
            if line.strip() and not line.startswith("#")}


def copy_distributable(tree: Path, dest: Path, lib_json):
    referenced = {p.split("/")[0] for p in library_paths(lib_json)}
    ignore = h5pignore(tree)
    if dest.exists():
        shutil.rmtree(dest)
    count = 0
    for f in sorted(tree.rglob("*")):
        rel = f.relative_to(tree)
        top = rel.parts[0]
        if not f.is_file() or any(p.startswith((".", "_")) for p in rel.parts):
            continue
        if top in ignore and top not in referenced and top != "library.json":
            continue
        if top in DEV_DIRS or (top in MAYBE_DEV_DIRS and top not in referenced):
            continue
        if "node_modules" in rel.parts:
            continue
        if len(rel.parts) == 1 and (rel.name in DEV_FILES or DEV_FILE_RE.match(rel.name)):
            continue
        if f.suffix.lower().lstrip(".") not in ALLOWED_EXT:
            continue
        target = dest / rel
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(f, target)
        count += 1
    missing = [p for p in library_paths(lib_json) if not (dest / p).exists()]
    if missing:
        raise RuntimeError(f"fichiers déclarés manquants après copie: {missing[:5]}")
    return count


def tree_digest(folder: Path):
    h = hashlib.sha256()
    for f in sorted(folder.rglob("*")):
        if f.is_file():
            h.update(f.relative_to(folder).as_posix().encode())
            h.update(hashlib.sha256(f.read_bytes()).digest())
    return h.hexdigest()


def library_options(semantics):
    """'Machine major.minor' strings allowed in library fields (embeddable sub-content)."""
    found = set()

    def walk(field):
        if isinstance(field, dict):
            if field.get("type") == "library":
                for o in field.get("options", []):
                    found.add(o if isinstance(o, str) else o.get("name"))
            for v in field.values():
                walk(v)
        elif isinstance(field, list):
            for v in field:
                walk(v)

    walk(semantics)
    return {o for o in found if o}


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("types", nargs="*", help="machine names (défaut: tous les types exécutables du registre)")
    ap.add_argument("--jobs", type=int, default=max(2, (os.cpu_count() or 2)))
    ap.add_argument("--no-options", action="store_true", help="ne pas suivre les sous-contenus proposés")
    args = ap.parse_args()

    registry = json.loads(REGISTRY.read_text())
    if REGISTRY_EXTRA.exists():
        registry.update({k: v for k, v in json.loads(REGISTRY_EXTRA.read_text()).items() if not k.startswith("_")})
    roots = args.types or sorted(k for k, v in registry.items() if v.get("runnable") in (1, True))
    repos = {}

    def repo_for(machine):
        info = registry.get(machine)
        if not info:
            return None
        url = info["repo"]["url"]
        return repos.setdefault(url, Repo(url))

    # Phase 1: resolve the closure from git metadata only (no build needed).
    resolved, failures = {}, {}
    pending = [(m, None, None, "racine") for m in roots]
    wanted = set()
    lock = threading.Lock()

    def resolve(item):
        machine, major, minor, why = item
        repo = repo_for(machine)
        if repo is None:
            return item, None, "absent du registre"
        try:
            for ref in repo.candidates(major, minor):
                raw = repo.show(ref, "library.json")
                if not raw:
                    continue
                lj = json.loads(raw)
                if major is None or (lj["majorVersion"], lj["minorVersion"]) == (major, minor):
                    sem_raw = repo.show(ref, "semantics.json")
                    sem = json.loads(sem_raw) if sem_raw else []
                    return item, (repo, ref, lj, sem), None
            return item, None, f"version {major}.{minor} introuvable (branches et tags)"
        except Exception as e:  # network or git error
            return item, None, str(e)[:300]

    with cf.ThreadPoolExecutor(max_workers=args.jobs * 2) as pool:
        while pending:
            batch, pending = pending, []
            for item, res, err in pool.map(resolve, batch):
                machine, major, minor, why = item
                if err:
                    key = f"{machine} {major}.{minor}" if major is not None else machine
                    failures[key] = f"{err} (requis par {why})"
                    continue
                repo, ref, lj, sem = res
                key = f"{lj['machineName']}-{lj['majorVersion']}.{lj['minorVersion']}"
                with lock:
                    if key in resolved:
                        continue
                    resolved[key] = {"repo": repo, "ref": ref, "lib": lj, "semantics": sem, "why": why}
                deps = []
                for kind in ("preloadedDependencies", "editorDependencies", "dynamicDependencies"):
                    for d in lj.get(kind, []):
                        deps.append((d["machineName"], d["majorVersion"], d["minorVersion"]))
                if not args.no_options:
                    for opt in library_options(sem):
                        m, v = opt.split(" ")
                        ma, mi = (int(x) for x in v.split("."))
                        deps.append((m, ma, mi))
                for m, ma, mi in deps:
                    k = f"{m}-{ma}.{mi}"
                    with lock:
                        if k in resolved or k in wanted:
                            continue
                        wanted.add(k)
                    pending.append((m, ma, mi, key))
            log(f"résolution: {len(resolved)} bibliothèques, {len(pending)} en attente, {len(failures)} échecs")

    # Keep only what is reachable from the roots (deps + sub-content options): robust against
    # stale branches/tags that would otherwise drag in obsolete versions.
    def edges(key):
        lj, sem = resolved[key]["lib"], resolved[key]["semantics"]
        out = [f"{d['machineName']}-{d['majorVersion']}.{d['minorVersion']}"
               for kind in ("preloadedDependencies", "editorDependencies", "dynamicDependencies")
               for d in lj.get(kind, [])]
        if not args.no_options:
            out += [o.replace(" ", "-") for o in library_options(sem)]
        return out

    reach, stack = {}, [(k, "racine") for k, v in resolved.items() if v["why"] == "racine"]
    while stack:
        key, why = stack.pop()
        if key in reach or key not in resolved:
            continue
        reach[key] = why
        stack.extend((k, key) for k in edges(key))
    dropped = sorted(set(resolved) - set(reach))
    if dropped:
        log(f"{len(dropped)} version(s) inatteignable(s) depuis les types racines ignorée(s)")
    resolved = {k: {**v, "why": reach[k]} for k, v in resolved.items() if k in reach}
    failures = {k: v for k, v in failures.items()
                if any(v.endswith(f"(requis par {r})") for r in reach) or "racine" in v}

    # Phase 2: export, build when needed, copy distributable files.
    OUT.mkdir(parents=True, exist_ok=True)
    old_lock = json.loads(LOCK.read_text()) if LOCK.exists() else {}
    lock_data = {}

    def materialize(key):
        entry = resolved[key]
        repo, ref, lj = entry["repo"], entry["ref"], entry["lib"]
        sha = repo.sha(ref)
        dest = OUT / key
        prev = old_lock.get(key)
        if prev and prev.get("commit") == sha and dest.exists():
            return key, prev, None, "inchangée"
        tree = CACHE / "build" / f"{key}@{sha[:12]}"
        if not (tree / ".ok").exists():
            export_tree(repo, ref, tree)
            if needs_build(tree, lj):
                build(tree, key)
                (tree / ".built").write_text("ok")
            (tree / ".ok").write_text("ok")
        built = (tree / ".built").exists()
        count = copy_distributable(tree, dest, lj)
        info = {"machineName": lj["machineName"], "majorVersion": lj["majorVersion"],
                "minorVersion": lj["minorVersion"], "patchVersion": lj["patchVersion"],
                "runnable": lj.get("runnable", 0), "repo": repo.url, "ref": ref.replace("refs/", ""),
                "commit": sha, "built": built, "requiredBy": entry["why"],
                "files": count, "sha256": tree_digest(dest)}
        return key, info, None, "compilée" if built else "copiée"

    with cf.ThreadPoolExecutor(max_workers=args.jobs) as pool:
        futures = {pool.submit(materialize, k): k for k in sorted(resolved)}
        for fut in cf.as_completed(futures):
            key = futures[fut]
            try:
                key, info, _, status = fut.result()
                lock_data[key] = info
                log(f"  {status:9} {key}")
            except Exception as e:
                failures[key] = str(e)[-600:]
                log(f"  ÉCHEC     {key}: {str(e).splitlines()[0][:200]}")

    # keep previously vendored entries that were not part of this run (partial runs)
    for k, v in old_lock.items():
        if k not in lock_data and (OUT / k).exists() and k not in resolved and args.types:
            lock_data[k] = v
    if not args.types:  # full run: prune folders that are no longer part of the closure
        for d in OUT.iterdir():
            if d.is_dir() and d.name not in lock_data:
                shutil.rmtree(d)
                log(f"  retirée   {d.name}")
    LOCK.write_text(json.dumps(dict(sorted(lock_data.items())), indent=1, ensure_ascii=False) + "\n")
    report = CACHE / "vendor-report.json"
    report.write_text(json.dumps(failures, indent=1, ensure_ascii=False))
    log(f"\n{len(lock_data)} bibliothèques dans {OUT.relative_to(ROOT)}; {len(failures)} échec(s) -> {report}")
    for k, v in sorted(failures.items()):
        log(f"  - {k}: {v.splitlines()[0][:220]}")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
