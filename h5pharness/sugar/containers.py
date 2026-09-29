"""Sugar for containers: accordéon, colonne, livre interactif.

Inside a container, content is a flow of blocks:
  - Markdown text                      -> Texte (H5P.AdvancedText)
  - a line ![description](image|vidéo) -> Image / Vidéo / Audio
  - ::: type [argument]  …  :::        -> any sub-content written with that type's own sugar
  - ::: type yaml        …  :::        -> any sub-content written as raw YAML fields
"""
import yaml

from . import adapter, parse_sugar
from .common import DIRECTIVE, IMAGE, join, lines_of, media_library, split_headings


def parse_blocks(numbered, s):
    blocks, text = [], []

    def flush():
        # a run of lines starting with '|' is a Markdown table -> H5P.Table (texts do not accept tables)
        segment, is_table = [], None
        for item in text + [(None, "")]:
            table_line = item[1].lstrip().startswith("|")
            if item[0] is None or (is_table is not None and table_line != is_table and item[1].strip()):
                body = join(segment)
                if body.strip():
                    blocks.append({"library": "H5P.Table" if is_table else "H5P.AdvancedText", "text": body})
                segment = []
            if item[0] is not None:
                if item[1].strip():
                    is_table = table_line
                segment.append(item)
        text.clear()

    i = 0
    while i < len(numbered):
        ln, line = numbered[i]
        st = line.strip()
        d = DIRECTIVE.match(st) if st.startswith(":::") and st != ":::" else None
        if d:
            flush()
            j, inner = i + 1, []
            while j < len(numbered) and numbered[j][1].strip() != ":::":
                inner.append(numbered[j])
                j += 1
            if j >= len(numbered):
                s.error(ln, "bloc « ::: » non fermé (ligne « ::: » seule attendue)")
            kind, rest = d.group(1), d.group(2).lstrip(":").strip()
            try:
                machine, _, _ = s.ctx.registry.machine_of(kind)
            except KeyError:
                s.error(ln, f"type « {kind} » inconnu")
                i = j + 1
                continue
            if rest.lower() == "yaml":
                try:
                    params = yaml.safe_load(join(inner)) or {}
                except yaml.YAMLError as e:
                    s.error(ln, f"YAML invalide dans le bloc ({getattr(e, 'problem', e)})")
                    params = {}
                if not isinstance(params, dict):
                    s.error(ln, "le bloc yaml doit contenir des champs « nom: valeur »")
                    params = {}
            else:
                params = parse_sugar(machine, join(inner), s.ctx, s.path,
                                     line_offset=s.line_offset + ln + 1, arg=rest or None)
            blocks.append({"library": machine, **params})
            i = j + 1
            continue
        im = IMAGE.match(line)
        if im:
            flush()
            blocks.append(media_library(im.group(1), im.group(2), im.group(3)))
            i += 1
            continue
        text.append((ln, line))
        i += 1
    flush()
    return blocks


@adapter("H5P.Column")
def column(text, s, arg=None):
    blocks = parse_blocks(lines_of(text), s)
    if not blocks:
        s.error(None, "colonne vide")
    return {"content": [{"content": b} for b in blocks]}


@adapter("H5P.Accordion")
def accordion(text, s, arg=None):
    pre, sections = split_headings(lines_of(text), 2)
    if join(pre).strip():
        s.error(0, "texte avant le premier panneau « ## Titre »")
    panels = [{"title": h, "content": {"library": "H5P.AdvancedText", "text": join(body)}}
              for h, hl, body in sections]
    if not panels:
        s.error(None, "aucun panneau: une section « ## Titre » par panneau")
    return {"panels": panels}


@adapter("H5P.InteractiveBook")
def interactivebook(text, s, arg=None):
    pre, sections = split_headings(lines_of(text), 1)
    chapters = []
    for heading, hl, body in sections:
        blocks = parse_blocks(body, s)
        if not blocks:
            s.error(hl, f"chapitre « {heading} » vide")
        chapters.append({"library": "H5P.Column", "metadata": {"title": heading},
                         "content": [{"content": b} for b in blocks]})
    if not chapters:
        s.error(None, "aucun chapitre: une section « # Titre du chapitre » par chapitre")
    out = {"chapters": chapters}
    cover = [(ln, l) for ln, l in pre if l.strip()]
    if cover:
        out["showCoverPage"] = True
        media = [IMAGE.match(l) for _, l in cover if IMAGE.match(l)]
        desc = [(ln, l) for ln, l in cover if not IMAGE.match(l)]
        out["bookCover"] = {"coverDescription": join(desc)}
        if media:
            out["bookCover"]["coverMedium"] = media_library(media[0].group(1), media[0].group(2), media[0].group(3))
    return out
