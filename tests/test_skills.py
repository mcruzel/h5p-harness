"""Skills portables : listés, sans chemin de machine, frontmatter valide, exportés avec les chemins réels."""
import re

import yaml

from h5pharness import cli, skills
from h5pharness.library import ROOT

EXPECTED = ["activite-h5p", "controler-activite-h5p", "depot-moodle-h5p", "maintenir-harnais-h5p"]


def _frontmatter(text):
    m = re.match(r"---\n(.*?)\n---\n", text, re.S)
    assert m, "frontmatter absent"
    return yaml.safe_load(m.group(1))


def test_portable_skills_are_listed_and_free_of_machine_paths():
    assert skills.names() == EXPECTED
    for n in skills.names():
        text = (skills.SRC / n / "SKILL.md").read_text(encoding="utf-8")
        meta = _frontmatter(text)
        assert set(meta) == {"name", "description"} and meta["name"] == n, n
        assert len(meta["description"]) > 40, n
        assert "<HARNAIS>" in text, n
        assert "/home/" not in text and "ubuntu" not in text and "course-composer" not in text, n


def test_skills_cite_real_commands_and_files():
    """Une commande ou un fichier cité par un skill doit exister dans le harnais (le skill ne ment pas)."""
    text = "\n".join((skills.SRC / n / "SKILL.md").read_text(encoding="utf-8") for n in skills.names())
    for needle in ("tools/qa.py", "--render", "--shots", "H5P_MOODLE_DIR", "H5P_MOODLE_RUNAS", "H5P_MOODLE_USER",
                   "H5P_MOODLE_BANQUE", "H5P_MOODLE_OWNER", "--banque", "--as banque", "--hidden", "transcript:"):
        assert needle in text, needle
    for path in ("tools/qa.py", "tools/vendor_libraries.py", "specs/README.md", "h5pharness/moodle_deploy.php",
                 "vendor/libraries.lock.json", "docs/INTEGRATION.md"):
        assert (ROOT / path).exists(), path
    cli_text = (ROOT / "h5pharness" / "cli.py").read_text(encoding="utf-8")
    for option in ("--banque", "--moodle-dir", "--hidden", "--publish", "--page", "--as"):
        assert option in cli_text, option


def test_every_environment_variable_is_documented():
    """docs/INTEGRATION.md liste chaque variable H5P_* lue par le code du harnais."""
    doc = (ROOT / "docs" / "INTEGRATION.md").read_text(encoding="utf-8")
    used = set()
    for folder in ("h5pharness", "tools"):
        for f in (ROOT / folder).glob("*.py"):
            used |= set(re.findall(r"[\"'](H5P_[A-Z_]+)[\"']", f.read_text(encoding="utf-8")))
        for f in (ROOT / folder).glob("*.mjs"):
            used |= set(re.findall(r"process\.env\.(H5P_[A-Z_]+)", f.read_text(encoding="utf-8")))
    assert used >= {"H5P_MOODLE_DIR", "H5P_MOODLE_RUNAS", "H5P_HARNESS_CACHE"}, used
    for var in sorted(used):
        assert var in doc, f"{var} n'est pas documentée dans docs/INTEGRATION.md"


def test_export_replaces_the_placeholders(tmp_path, capsys):
    dest = tmp_path / "skills"
    assert cli.main(["skills", "--exporter", str(dest), "--projet", "/srv/mon-projet"]) == 0
    assert f"{len(EXPECTED)} skill(s)" in capsys.readouterr().out
    for n in skills.names():
        text = (dest / n / "SKILL.md").read_text(encoding="utf-8")
        assert "<HARNAIS>" not in text and "<PROJET>" not in text
        assert str(ROOT.resolve()) in text
        assert _frontmatter(text)["name"] == n
    assert "/srv/mon-projet" in (dest / "activite-h5p" / "SKILL.md").read_text(encoding="utf-8")
    assert cli.main(["skills"]) == 0
    assert "activite-h5p" in capsys.readouterr().out
