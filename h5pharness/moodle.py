"""Direct deposit into a Moodle installed on the same machine as the agent (activity or page).

Moodle has no web service that creates activities, so the harness runs a small PHP script inside the
local Moodle (h5pharness/moodle_deploy.php), which uses Moodle's own API: capabilities, course cache,
H5P deployment and logs behave as if a teacher had uploaded the package.

Configuration (environment of the agent):
  H5P_MOODLE_DIR    Moodle folder (the one holding config.php); otherwise usual places are searched
  H5P_MOODLE_PHP    PHP binary (default: php)
  H5P_MOODLE_RUNAS  system user that owns moodledata, e.g. www-data (run through sudo -n / runuser)
  H5P_MOODLE_USER   Moodle account the deposit is made with (default: the main administrator)
  H5P_MOODLE_BANQUE 1 = also put every content in the course content bank (like --banque)
  H5P_MOODLE_OWNER  teacher account the content bank items are attributed to (so that it can edit them)
"""
import json
import os
import re
import shutil
import subprocess
import tempfile
from pathlib import Path

SCRIPT = Path(__file__).with_name("moodle_deploy.php")
CANDIDATES = ("/var/www/moodle", "/var/www/html/moodle", "/var/www/html", "/srv/moodle", "/opt/moodle",
              "/usr/share/moodle", "~/moodle")
AS = {"activite": "activity", "activité": "activity", "activity": "activity", "h5pactivity": "activity",
      "page": "page", "banque": "bank", "bank": "bank", "contentbank": "bank"}
YES = {"1", "true", "oui", "yes", "on"}


class MoodleError(Exception):
    pass


def find_moodle(explicit=None):
    tried = [explicit] if explicit else []
    if os.environ.get("H5P_MOODLE_DIR"):
        tried.append(os.environ["H5P_MOODLE_DIR"])
    for c in tried + list(CANDIDATES):
        p = Path(c).expanduser()
        cfg = p / "config.php"
        try:
            if cfg.is_file() and "wwwroot" in cfg.read_text(errors="replace"):
                return p
        except OSError:
            continue
    raise MoodleError("Moodle introuvable sur cette machine : indiquer le dossier qui contient config.php "
                      "(--moodle-dir ou variable H5P_MOODLE_DIR)")


def target(meta, cli):
    """Where to deposit: front matter `moodle:` block completed/overridden by the command line."""
    fm = meta.get("moodle") or {}
    if not isinstance(fm, dict):
        raise MoodleError("en-tête: « moodle: » attend des clés course, section, as, page, hidden")
    t = {"course": fm.get("course", fm.get("cours")), "section": fm.get("section", 0),
         "as": fm.get("as", fm.get("forme", "activite")), "page": fm.get("page"), "hidden": fm.get("hidden", False),
         "bank": bool(fm.get("banque", fm.get("bank", False)))
         or os.environ.get("H5P_MOODLE_BANQUE", "").strip().lower() in YES}
    for k in ("course", "section", "as", "page"):
        if cli.get(k) not in (None, ""):
            t[k] = cli[k]
    if cli.get("hidden"):
        t["hidden"] = True
    if cli.get("bank"):
        t["bank"] = True
    if t["page"]:
        t["as"] = "page"
    if t["as"] not in AS:
        raise MoodleError(f"forme « {t['as']} » inconnue : activite (activité H5P) ou page")
    t["as"] = AS[t["as"]]
    t["bank"] = t["bank"] or t["as"] == "bank"
    if t["course"] in (None, ""):
        raise MoodleError("cours Moodle non précisé : --moodle <id ou nom abrégé du cours> (ou « moodle: {course: …} » "
                          "dans l'en-tête)")
    return t


def _slug(text):
    return re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")[:60] or "activite"


def deploy(package, *, key, name, course, section=0, as_="activity", page=None, hidden=False, bank=False,
           moodle_dir=None):
    """Create or update the activity/page (and/or content bank item) of this source; returns the JSON answer."""
    root = find_moodle(moodle_dir)
    request = {"course": str(course), "section": int(section or 0), "as": as_, "page": page, "key": key,
               "bank": bool(bank),
               "name": name, "visible": not hidden, "filename": _slug(key.rsplit(".", 1)[0]) + ".h5p",
               "user": os.environ.get("H5P_MOODLE_USER") or None, "owner": os.environ.get("H5P_MOODLE_OWNER") or None}
    with tempfile.TemporaryDirectory(prefix="h5pharness-") as tmp:
        os.chmod(tmp, 0o755)   # readable by the web server account when H5P_MOODLE_RUNAS is set
        work = Path(tmp)
        shutil.copyfile(package, work / "paquet.h5p")
        shutil.copyfile(SCRIPT, work / SCRIPT.name)
        request["h5p"] = str(work / "paquet.h5p")
        (work / "request.json").write_text(json.dumps(request, ensure_ascii=False), encoding="utf-8")
        for f in work.iterdir():
            os.chmod(f, 0o644)
        cmd = [os.environ.get("H5P_MOODLE_PHP", "php"), str(work / SCRIPT.name), str(root), str(work / "request.json")]
        runas = os.environ.get("H5P_MOODLE_RUNAS")
        if runas:
            cmd = (["runuser", "-u", runas, "--"] if os.geteuid() == 0 else ["sudo", "-n", "-u", runas]) + cmd
        try:
            res = subprocess.run(cmd, capture_output=True, text=True, timeout=900)
        except (OSError, subprocess.TimeoutExpired) as e:
            raise MoodleError(f"exécution de PHP impossible ({e})") from None
    answer = next((line for line in reversed(res.stdout.splitlines()) if line.startswith("{")), None)
    if answer is None:
        detail = (res.stderr or res.stdout).strip().splitlines()
        raise MoodleError(f"réponse inattendue de Moodle ({detail[-1][:300] if detail else res.returncode})")
    data = json.loads(answer)
    if not data.get("ok"):
        raise MoodleError(data.get("error", "erreur inconnue"))
    return data
