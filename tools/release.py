#!/usr/bin/env python3
"""Publish built packages as assets of a per-branch GitHub pre-release (used by CI).

The .h5p files are not committed (they are rebuilt identically from sources/); CI attaches them to
the release "h5p-<branch>" so they can be downloaded without bloating the git history.
Requires the GitHub CLI (`gh`) with GH_TOKEN, GITHUB_REF_NAME and GITHUB_SHA (set by Actions).
"""
import datetime as dt
import hashlib
import json
import os
import re
import subprocess
import sys
from pathlib import Path


def gh(*args, check=True):
    res = subprocess.run(["gh", *args], capture_output=True, text=True)
    if check and res.returncode != 0:
        raise SystemExit(f"gh {' '.join(args[:3])}…: {res.stderr.strip()[-400:]}")
    return res


def remote_assets(tag):
    """{asset name: 'sha256:…' digest (None when GitHub does not report one)} of the release."""
    res = gh("api", f"repos/{os.environ['GITHUB_REPOSITORY']}/releases/tags/{tag}", check=False)
    if res.returncode != 0:
        return {}
    return {a["name"]: a.get("digest") for a in json.loads(res.stdout).get("assets", [])}


def to_upload(packages, remote):
    """Builds are byte-reproducible: only send a package whose content differs from the published one
    (keeps each run short now that sources/exemples holds one package per type)."""
    out = []
    for name, path in packages.items():
        digest = "sha256:" + hashlib.sha256(path.read_bytes()).hexdigest()
        if remote.get(name) != digest:
            out.append(name)
    return out


def main():
    dist = Path(sys.argv[1] if len(sys.argv) > 1 else "dist")
    lite = Path(sys.argv[2]) if len(sys.argv) > 2 else None   # content-only variants (no libraries)
    branch = os.environ["GITHUB_REF_NAME"]
    sha = os.environ.get("GITHUB_SHA", "")[:7]
    tag = "h5p-" + re.sub(r"[^A-Za-z0-9._-]+", "-", branch).strip("-")
    packages = {p.relative_to(dist).as_posix().replace("/", "--"): p for p in sorted(dist.rglob("*.h5p"))}
    if lite and lite.exists():
        packages.update({p.relative_to(lite).as_posix().replace("/", "--")[:-4] + ".contenu-seul.h5p": p
                         for p in sorted(lite.rglob("*.h5p"))})
    now = dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    notes = (f"Paquets H5P construits automatiquement depuis `sources/` (branche `{branch}`, commit {sha}, {now}).\n\n"
             "Importer un fichier `.h5p` dans Moodle : activité « Contenu interactif H5P » ou banque de contenus. "
             "Les fichiers `.contenu-seul.h5p` n'embarquent pas les bibliothèques (quelques Ko) : à utiliser si le "
             "site possède déjà les mêmes versions des types de contenu (limite de dépôt faible).\n\n"
             + "\n".join(f"- `{name}`" for name in packages))
    if gh("release", "view", tag, check=False).returncode != 0:
        gh("release", "create", tag, "--prerelease", "--title", f"Paquets H5P — {branch}", "--notes", notes,
           "--target", os.environ.get("GITHUB_SHA", branch))
    else:
        gh("release", "edit", tag, "--notes", notes)
    remote = remote_assets(tag)
    changed = to_upload(packages, remote)
    staging = dist / ".release"
    staging.mkdir(exist_ok=True)
    files = []
    for name in changed:
        target = staging / name
        target.write_bytes(packages[name].read_bytes())
        files.append(str(target))
    for i in range(0, len(files), 20):
        gh("release", "upload", tag, *files[i:i + 20], "--clobber")
    stale = sorted(set(remote) - set(packages))
    for name in stale:
        gh("release", "delete-asset", tag, name, "-y")
    print(f"release {tag} : {len(packages)} paquet(s) dont {len(changed)} envoyé(s) et "
          f"{len(packages) - len(changed)} inchangé(s)" + (f", {len(stale)} retiré(s)" if stale else ""))


if __name__ == "__main__":
    main()
