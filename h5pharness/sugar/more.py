"""Sugar for graphique, choix d'images, onglets, dictée."""
import re

from . import adapter
from .common import CHECK, IMAGE, join, lines_of, media_library, split_headings
from .containers import parse_blocks

IMG = re.compile(r"^!\[([^\]]*)\]\(\s*<?([^)\s>]+)>?(?:\s+\"([^\"]*)\")?\s*\)\s*$")


@adapter("H5P.Chart")
def chart(text, s, arg=None):
    """« type: barres|secteurs » facultatif, puis « - Libellé : valeur [#couleur] »."""
    mode, rows = None, []
    for ln, line in lines_of(text):
        m = re.match(r"^\s*(type|graphique)\s*:\s*(\w+)\s*$", line, re.I)
        r = re.match(r"^\s*[-*+]\s+(.+?)\s*:\s*(\d+(?:[.,]\d+)?)\s*(#[0-9a-fA-F]{3,6})?\s*$", line)
        if m:
            w = m.group(2).lower()
            mode = "barChart" if w.startswith(("bar", "histo", "colonne")) else "pieChart" if w.startswith(
                ("sect", "cam", "pie")) else None
            if mode is None:
                s.error(ln, "type de graphique : barres ou secteurs")
        elif r:
            row = {"text": r.group(1), "value": float(r.group(2).replace(",", "."))}
            if r.group(3):
                row["color"] = r.group(3)
            rows.append(row)
        elif line.strip():
            s.error(ln, "ligne attendue : « - Libellé : valeur » (couleur facultative #rrggbb)")
    if not rows:
        s.error(None, "aucune donnée : lignes « - Libellé : valeur »")
    palette = ["#1f77b4", "#ff7f0e", "#2ca02c", "#d62728", "#9467bd", "#8c564b", "#e377c2", "#7f7f7f"]
    for i, row in enumerate(rows):
        row.setdefault("color", palette[i % len(palette)])
    out = {"listOfTypes": rows}
    if mode:
        out["graphMode"] = mode
    return out


@adapter("H5P.MultiMediaChoice")
def multimediachoice(text, s, arg=None):
    """Question, puis « - [x] ![description](image) » (bonne) / « - [ ] ![…](…) »."""
    question, options = [], []
    for ln, line in lines_of(text):
        m = CHECK.match(line)
        if m:
            im = IMG.match(m.group(3).strip())
            if not im:
                s.error(ln, "option attendue : « - [x] ![description](image) »")
                continue
            options.append({"media": media_library(im.group(1), im.group(2), im.group(3)),
                            "correct": m.group(2) != " "})
        elif line.strip():
            question.append(line)
    if len(options) < 2:
        s.error(None, "au moins 2 options « - [ ] ![description](image) »")
    if options and not any(o["correct"] for o in options):
        s.error(None, "aucune option correcte « - [x] … »")
    return {"question": "\n".join(question).strip(), "options": options}


@adapter("H5P.Tabs")
def tabs(text, s, arg=None):
    """Un onglet par section « ## Titre », contenu comme une colonne (texte, images, ::: sous-contenus)."""
    pre, sections = split_headings(lines_of(text), 2)
    if join(pre).strip():
        s.error(0, "texte avant le premier onglet « ## Titre »")
    out = []
    for heading, hl, body in sections:
        blocks = parse_blocks(body, s)
        if not blocks:
            s.error(hl, f"onglet « {heading} » vide")
        out.append({"library": "H5P.Column", "metadata": {"title": heading},
                    "content": [{"content": b} for b in blocks]})
    if not out:
        s.error(None, "aucun onglet : sections « ## Titre »")
    return {"tabs": out}


@adapter("H5P.Dictation")
def dictation(text, s, arg=None):
    """Consigne, puis une phrase par ligne : « - ![](audio.mp3) Phrase attendue » (+ « :: indication »)."""
    task, sentences = [], []
    rx = re.compile(r"^\s*[-*+]\s+!\[([^\]]*)\]\(\s*<?([^)\s>]+)>?\s*\)\s*(.+?)(?:\s*::\s*(.+))?\s*$")
    for ln, line in lines_of(text):
        m = rx.match(line)
        if m:
            sent = {"sample": [m.group(2)], "text": m.group(3).strip()}
            if m.group(4):
                sent["description"] = m.group(4).strip()
            sentences.append(sent)
        elif IMAGE.match(line) or not line.strip():
            continue
        else:
            task.append(line)
    if not sentences:
        s.error(None, "aucune phrase : lignes « - ![](audio.mp3) Phrase attendue »")
    return {"taskDescription": "\n".join(task).strip() or "Écoute et écris la phrase.", "sentences": sentences}
