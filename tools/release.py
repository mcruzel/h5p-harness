#!/usr/bin/env python3
"""Publish built packages as assets of a per-branch GitHub pre-release (used by CI).

The .h5p files are not committed (they are rebuilt identically from sources/); CI attaches them to
the release "h5p-<branch>" so they can be downloaded without bloating the git history.
Requires the GitHub CLI (`gh`) with GH_TOKEN, GITHUB_REF_NAME and GITHUB_SHA (set by Actions).
"""
import datetime as dt
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


def main():
    dist = Path(sys.argv[1] if len(sys.argv) > 1 else "dist")
    branch = os.environ["GITHUB_REF_NAME"]
    sha = os.environ.get("GITHUB_SHA", "")[:7]
    tag = "h5p-" + re.sub(r"[^A-Za-z0-9._-]+", "-", branch).strip("-")
    packages = {p.relative_to(dist).as_posix().replace("/", "--"): p for p in sorted(dist.rglob("*.h5p"))}
    now = dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    notes = (f"Paquets H5P construits automatiquement depuis `sources/` (branche `{branch}`, commit {sha}, {now}).\n\n"
             "Importer un fichier `.h5p` dans Moodle : activité « Contenu interactif H5P » ou banque de contenus.\n\n"
             + "\n".join(f"- `{name}`" for name in packages))
    if gh("release", "view", tag, check=False).returncode != 0:
        gh("release", "create", tag, "--prerelease", "--title", f"Paquets H5P — {branch}", "--notes", notes,
           "--target", os.environ.get("GITHUB_SHA", branch))
    else:
        gh("release", "edit", tag, "--notes", notes)
    existing = set(filter(None, gh("release", "view", tag, "--json", "assets", "-q", ".assets[].name").stdout.split()))
    staging = dist / ".release"
    staging.mkdir(exist_ok=True)
    files = []
    for name, path in packages.items():
        target = staging / name
        target.write_bytes(path.read_bytes())
        files.append(str(target))
    if files:
        gh("release", "upload", tag, *files, "--clobber")
    for stale in sorted(existing - set(packages)):
        gh("release", "delete-asset", tag, stale, "-y")
    print(f"{len(packages)} paquet(s) publiés dans la release {tag}" +
          (f", {len(existing - set(packages))} retiré(s)" if existing - set(packages) else ""))


if __name__ == "__main__":
    main()
