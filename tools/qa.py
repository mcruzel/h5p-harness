#!/usr/bin/env python3
"""Quality gate for built packages: official H5P PHP validator (+ display filter) and headless rendering.

    python tools/qa.py dist/                 # every .h5p under dist/
    python tools/qa.py dist/x.h5p --render   # also play it in Chromium (h5p-standalone)
    python tools/qa.py dist/ --render --shots out/   # + screenshots

Prerequisites (fetched into ~/.cache/h5p-harness on first use): git, php (zip, mbstring), and for
--render: node + npm (h5p-standalone, playwright with a Chromium).
"""
import argparse
import concurrent.futures as cf
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CACHE = Path(os.environ.get("H5P_HARNESS_CACHE", Path.home() / ".cache" / "h5p-harness"))
CORE = CACHE / "h5p-php-library"
RENDER = CACHE / "render"
H5P_STANDALONE = "h5p-standalone@3.8.2"


def ensure_core():
    if not (CORE / "h5p.classes.php").exists():
        subprocess.run(["git", "clone", "-q", "--depth", "1", "https://github.com/h5p/h5p-php-library", str(CORE)],
                       check=True)
    return CORE


def ensure_render():
    mods = RENDER / "node_modules"
    if not (mods / "h5p-standalone").exists():
        RENDER.mkdir(parents=True, exist_ok=True)
        (RENDER / "package.json").write_text('{"private": true}')
        pkgs = [H5P_STANDALONE]
        if subprocess.run(["node", "-e", "require.resolve('playwright')"], capture_output=True,
                          env={**os.environ, "NODE_PATH": str(mods)}).returncode != 0 and not global_playwright():
            pkgs.append("playwright")
        subprocess.run(["npm", "i", "--no-audit", "--no-fund", "--loglevel=error", *pkgs], cwd=RENDER, check=True)
    if not (mods / "playwright").exists():
        glob = global_playwright()
        if glob:
            (mods / "playwright").symlink_to(glob)
    return mods


def global_playwright():
    try:
        root = subprocess.run(["npm", "root", "-g"], capture_output=True, text=True).stdout.strip()
    except OSError:
        return None
    p = Path(root) / "playwright"
    return p if p.exists() else None


def php_check(pkg, mode):
    res = subprocess.run(["php", str(ROOT / "tools" / "official_validator.php"), str(pkg),
                          str(ROOT / "vendor" / "libraries"), str(ensure_core()), mode],
                         capture_output=True, text=True, timeout=300)
    try:
        return json.loads(res.stdout)
    except json.JSONDecodeError:
        return {"valid": False, "messages": [f"php: {(res.stderr or res.stdout).strip()[-300:]}"], "altered": []}


def render(pkg, shot=None):
    env = {**os.environ, "H5P_RENDER_MODULES": str(ensure_render())}
    if Path("/opt/pw-browsers/chromium").exists() and "H5P_CHROMIUM" not in env:
        env["H5P_CHROMIUM"] = "/opt/pw-browsers/chromium"
    cmd = ["node", str(ROOT / "tools" / "render.mjs"), str(pkg)] + ([str(shot)] if shot else [])
    res = subprocess.run(cmd, capture_output=True, text=True, timeout=180, env=env)
    try:
        return json.loads(res.stdout.strip().splitlines()[-1])
    except (json.JSONDecodeError, IndexError):
        return {"initError": (res.stderr or res.stdout).strip()[-300:], "errors": [], "missing": [], "text": ""}


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("targets", nargs="+")
    ap.add_argument("--render", action="store_true")
    ap.add_argument("--shots", help="dossier des captures d'écran (avec --render)")
    ap.add_argument("--no-php", action="store_true")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("-j", "--jobs", type=int, default=4)
    args = ap.parse_args()
    pkgs = []
    for t in args.targets:
        p = Path(t)
        pkgs += sorted(p.rglob("*.h5p")) if p.is_dir() else [p]
    if not args.no_php and not shutil.which("php"):
        print("php introuvable: installer php-cli (+ zip, mbstring) ou utiliser --no-php")
        return 2
    if not args.no_php:
        ensure_core()
    if args.render:
        ensure_render()
    shots = Path(args.shots) if args.shots else None
    if shots:
        shots.mkdir(parents=True, exist_ok=True)

    def one(pkg):
        out = {"package": str(pkg)}
        if not args.no_php:
            out["admin"] = php_check(pkg, "admin")
            out["teacher"] = php_check(pkg, "teacher")
        if args.render:
            out["render"] = render(pkg, shots / (pkg.stem + ".png") if shots else None)
        return out

    with cf.ThreadPoolExecutor(max_workers=args.jobs) as pool:
        results = list(pool.map(one, pkgs))
    failed = 0
    for r in results:
        issues = []
        for mode in ("admin", "teacher"):
            if mode in r and not r[mode]["valid"]:
                issues.append(f"{mode}: " + "; ".join(m for m in r[mode]["messages"] if m.startswith("ERREUR"))[:300])
        alt = r.get("teacher", {}).get("altered") or r.get("admin", {}).get("altered") or []
        if alt:
            issues.append(f"filtre H5P: {len(alt)} altération(s): " + "; ".join(alt[:3]))
        rd = r.get("render")
        blank = rd and not rd.get("text") and not rd.get("media")
        if rd and (rd.get("initError") or rd.get("errors") or rd.get("missing") or blank):
            parts = [rd.get("initError")] + rd.get("errors", [])[:3] + rd.get("missing", [])[:2]
            if blank:
                parts.append("rien d'affiché")
            issues.append("rendu: " + "; ".join(filter(None, parts)))
        name = r["package"]
        if issues:
            failed += 1
            print(f"ÉCHEC {name}")
            for i in issues:
                print(f"  - {i}")
        elif not args.json:
            print(f"OK    {name}" + (f"  « {rd['text'][:70]} »" if rd else ""))
    if args.json:
        print(json.dumps(results, ensure_ascii=False, indent=1))
    print(f"\n{len(results) - failed}/{len(results)} paquet(s) conformes")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
