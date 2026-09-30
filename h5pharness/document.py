"""Source document: YAML front matter + Markdown body (+ optional ```yaml blocks of raw params)."""
import re
from dataclasses import dataclass, field
from pathlib import Path

import yaml

FRONT_KEYS = {
    "type": "type de contenu (alias ou nom H5P)",
    "title": "titre du paquet",
    "language": "langue (fr par défaut)",
    "preset": "préréglage pédagogique",
    "license": "licence du contenu (ex. CC BY-SA 4.0)",
    "authors": "auteur(s)",
    "source": "URL source",
    "year": "année",
    "description": "note libre (non publiée)",
    "moodle": "dépôt dans un Moodle local : {course: id ou nom abrégé, section: n, as: activite|page, page: …}",
    "transcript": "transcrit horodaté de la vidéo (.vtt/.srt), requis pour ajouter des interactions à une vidéo",
}
FENCE = re.compile(r"^(```|~~~)\s*(yaml|yml|h5p)\s*$", re.I)


class Loader(yaml.SafeLoader):
    """YAML with YAML 1.2 scalars: what the author wrote stays text unless it is plainly a number or
    true/false. PyYAML (YAML 1.1) would silently turn a padlock code 0472 into 314 (octal), 1:20 into
    80 (base 60) and yes/no/on/off (or the language code "no") into booleans."""


Loader.yaml_implicit_resolvers = {
    k: [(tag, rx) for tag, rx in v if tag not in ("tag:yaml.org,2002:bool", "tag:yaml.org,2002:int",
                                                  "tag:yaml.org,2002:float")]
    for k, v in yaml.SafeLoader.yaml_implicit_resolvers.items()}
Loader.add_implicit_resolver("tag:yaml.org,2002:bool", re.compile(r"^(?:true|True|TRUE|false|False|FALSE)$"),
                             list("tTfF"))
Loader.add_implicit_resolver("tag:yaml.org,2002:int", re.compile(r"^[-+]?(?:0|[1-9][0-9]*)$"),
                             list("-+0123456789"))
Loader.add_implicit_resolver("tag:yaml.org,2002:float", re.compile(
    r"^(?:[-+]?(?:0|[1-9][0-9]*)?\.[0-9]+(?:[eE][-+]?[0-9]+)?|[-+]?(?:0|[1-9][0-9]*)[eE][-+]?[0-9]+"
    r"|[-+]?\.(?:inf|Inf|INF)|\.(?:nan|NaN|NAN))$"), list("-+0123456789."))


def load_yaml(text):
    return yaml.load(text, Loader=Loader)  # noqa: S506 (SafeLoader subclass)


class DocumentError(Exception):
    def __init__(self, messages):
        super().__init__("; ".join(messages))
        self.messages = messages


@dataclass
class Document:
    path: Path
    meta: dict
    body: str                 # Markdown body, yaml blocks blanked (line numbers preserved)
    body_line: int            # 1-based line of the body's first line in the file
    yaml_blocks: list = field(default_factory=list)   # [(line, dict)]

    @property
    def has_sugar(self):
        return bool(self.body.strip())


def load(path: Path) -> Document:
    text = path.read_text(encoding="utf-8").replace("\r\n", "\n").lstrip("﻿")
    m = re.match(r"^---[ \t]*\n(.*?)\n---[ \t]*(\n|$)", text, re.S)
    if not m:
        raise DocumentError(["l.1: en-tête YAML manquant (--- type: … title: … ---)"])
    try:
        meta = load_yaml(m.group(1)) or {}
    except yaml.YAMLError as e:
        mark = getattr(e, "problem_mark", None)
        line = mark.line + 2 if mark else 1
        raise DocumentError([f"l.{line}: en-tête YAML invalide ({getattr(e, 'problem', e)})"]) from None
    if not isinstance(meta, dict):
        raise DocumentError(["l.2: l'en-tête doit être une liste de clés « clé: valeur »"])
    errors = []
    for k in meta:
        if k not in FRONT_KEYS:
            errors.append(f"en-tête: clé « {k} » inconnue (possibles: {', '.join(FRONT_KEYS)})")
    for k in ("type", "title"):
        if not meta.get(k):
            errors.append(f"en-tête: « {k}: » manquant ({FRONT_KEYS[k]})")
    body_line = m.group(0).count("\n") + 1
    lines = text[m.end():].split("\n")
    blocks, out, i = [], [], 0
    while i < len(lines):
        fm = FENCE.match(lines[i].strip())
        if fm:
            start = i
            j = i + 1
            while j < len(lines) and not lines[j].strip().startswith(fm.group(1)):
                j += 1
            if j >= len(lines):
                errors.append(f"l.{body_line + start}: bloc ```yaml non fermé")
                break
            raw = "\n".join(lines[start + 1:j])
            try:
                data = load_yaml(raw) or {}
                if not isinstance(data, dict):
                    errors.append(f"l.{body_line + start}: le bloc yaml doit contenir des clés « champ: valeur »")
                else:
                    blocks.append((body_line + start, data))
            except yaml.YAMLError as e:
                mark = getattr(e, "problem_mark", None)
                line = body_line + start + 1 + (mark.line if mark else 0)
                errors.append(f"l.{line}: YAML invalide ({getattr(e, 'problem', e)})")
            out.extend([""] * (j - start + 1))
            i = j + 1
            continue
        out.append(lines[i])
        i += 1
    if errors:
        raise DocumentError(errors)
    return Document(path=path, meta=meta, body="\n".join(out), body_line=body_line, yaml_blocks=blocks)
