"""git add / commit / push of the sources (the .h5p itself is rebuilt by CI, see README)."""
import os
import subprocess
import time
from pathlib import Path

from .library import ROOT


class PublishError(Exception):
    pass


def _git(*args, timeout=120):
    res = subprocess.run(["git", "-C", str(ROOT), *args], capture_output=True, text=True, timeout=timeout)
    return res.returncode, (res.stdout + res.stderr).strip()


def publish(paths, message):
    """Commit the given files and push the current branch; returns a short status line."""
    files = sorted({str(Path(p).resolve()) for p in paths if Path(p).exists()})
    if not files:
        return "rien à publier"
    code, out = _git("add", "--", *files)
    if code:
        raise PublishError(f"git add: {out.splitlines()[-1] if out else code}")
    code, _ = _git("diff", "--cached", "--quiet")
    if code == 0:
        return "déjà à jour (rien de nouveau à publier)"
    trailers = os.environ.get("H5P_COMMIT_TRAILERS", "").strip()   # e.g. Co-Authored-By lines required by a team
    if trailers:
        message = f"{message}\n\n{trailers}"
    code, out = _git("commit", "-q", "-m", message)
    if code:
        raise PublishError(f"git commit: {out.splitlines()[-1] if out else code}")
    code, branch = _git("rev-parse", "--abbrev-ref", "HEAD")
    if code or branch == "HEAD":
        raise PublishError("branche git introuvable (HEAD détaché)")
    delay, last = 2, ""
    for _attempt in range(5):
        code, out = _git("push", "-u", "origin", branch, timeout=300)
        if code == 0:
            _, sha = _git("rev-parse", "--short", "HEAD")
            return f"commit {sha} poussé sur {branch}"
        last = out.splitlines()[-1] if out else str(code)
        if "rejected" in out or "non-fast-forward" in out or "fetch first" in out:
            code, out = _git("pull", "-q", "--rebase", "origin", branch, timeout=300)
            if code:
                _git("rebase", "--abort")
                raise PublishError(f"conflit git lors du rebase: {out.splitlines()[-1] if out else code}")
            continue
        time.sleep(delay)  # network hiccup: exponential backoff
        delay *= 2
    raise PublishError(f"git push: {last}")
