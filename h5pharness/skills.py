"""Skills portables du harnais (skills/<nom>/SKILL.md) -> skills d'un environnement : « skills --exporter <dossier> ».

Les gabarits écrivent leurs chemins avec <HARNAIS> (dossier du harnais) et <PROJET> (dossier du projet : sources,
spécification de ses exercices) ; l'export les remplace par les chemins réels de cette installation.
"""
from pathlib import Path

from .library import ROOT

SRC = ROOT / "skills"


class SkillsError(Exception):
    pass


def names():
    return sorted(p.parent.name for p in SRC.glob("*/SKILL.md"))


def export(dest, project=None):
    """Écrit dest/<nom>/SKILL.md pour chaque skill portable ; -> [(nom, chemin)]."""
    found = names()
    if not found:
        raise SkillsError(f"aucun skill portable dans {SRC}")
    dest = Path(dest).expanduser().resolve()
    harness = ROOT.resolve()
    proj = Path(project).expanduser().resolve() if project else Path.cwd().resolve()
    out = []
    for name in found:
        text = (SRC / name / "SKILL.md").read_text(encoding="utf-8")
        text = text.replace("<HARNAIS>", str(harness)).replace("<PROJET>", str(proj))
        target = dest / name / "SKILL.md"
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(text, encoding="utf-8")
        out.append((name, target))
    return out
