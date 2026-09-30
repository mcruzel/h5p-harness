"""Sugar for Course Presentation with automatic layout.

One slide per `# Titre`; its content is a flow of blocks (as in a column): Markdown text, one
image/vidéo line, `::: type` interactions. Positions are computed on the 16:9 slide of H5P (base
width 640 px, font 16 px): title on top, text left and media right when both exist, one interaction
inline under the text (or as buttons when several or not enough room).
"""
import math
import re

from . import adapter
from .common import lines_of, split_headings, join
from .containers import parse_blocks

SLIDE_RATIO = 16 / 9
LINE = 6.7          # % of slide height per text line (16 px * 1.5 / 360 px)
CPL_FULL = 80       # characters per line at 100 % width
MARGIN = 4
TOP = 3
MEDIA = {"H5P.Image", "H5P.Video", "H5P.Audio"}


def _text_height(markdown, width):
    cpl = max(10, int(CPL_FULL * width / 100))
    lines, blocks = 0, 0
    for para in re.split(r"\n\s*\n", markdown.strip()):
        blocks += 1
        for raw in para.split("\n"):
            raw = re.sub(r"[*_`#>]|\[([^\]]*)\]\([^)]*\)", r"\1", raw).strip()
            scale = 1.6 if raw.startswith("#") or para.lstrip().startswith("#") else 1.0
            lines += max(1, math.ceil(len(raw) / cpl)) * scale
    return lines * LINE + blocks * 2.5 + 3


def _media_ratio(block, s):
    """height/width of an image block, from the actual file when readable."""
    if block.get("library") != "H5P.Image":
        return 9 / 16
    src = (block.get("file") or {}).get("src")
    try:
        from io import BytesIO
        from PIL import Image
        data, _ = s.ctx.media._read(src)
        w, h = Image.open(BytesIO(data)).size
        return h / w
    except Exception:
        return 0.75


def _element(action, x, y, w, h, **extra):
    el = {"x": round(x, 2), "y": round(y, 2), "width": round(w, 2), "height": round(h, 2), "action": action}
    el.update(extra)
    return el


def arrange(title, texts, ratios, n_interactions, warn):
    """Boxes (x, y, width, height in % of the slide) for a title, stacked texts (Markdown or plain text),
    media (height/width ratios) and interactions. Interactions go inline under the text when there are
    at most two and enough room, else they become buttons (as_button=True)."""
    geo = {"title": None, "texts": [], "media": [], "interactions": []}
    top = TOP
    if title is not None:
        title_h = 12 if len(title) <= 45 else 20
        geo["title"] = (MARGIN, TOP, 100 - 2 * MARGIN, title_h)
        top = TOP + title_h + 1
    text_w = 52 if ratios and texts else 100 - 2 * MARGIN
    y = top
    for text in texts:
        need, room = _text_height(text, text_w), 100 - y - 3
        if need > room:
            warn("texte probablement trop long pour une diapo (la couper en deux)")
        h = max(min(need, room), 5)
        geo["texts"].append((MARGIN, y, text_w, h))
        y += h + 1
    text_bottom = y - 1 if texts else top
    if ratios:
        if len(ratios) > 1:
            warn("une seule image/vidéo par diapo en mise en page automatique (les suivantes sont empilées)")
        col_x = 58 if texts else MARGIN
        col_w = 38 if texts else 100 - 2 * MARGIN
        my = top
        for ratio in ratios:
            w = col_w
            h = w * ratio * SLIDE_RATIO
            room = 100 - my - 3
            if h > room:
                h = max(room, 5)
                w = h / (ratio * SLIDE_RATIO)
            geo["media"].append((col_x + (col_w - w) / 2, my, w, h))
            my += h + 2
        text_bottom = max(text_bottom, my - 2)
    if n_interactions:
        room = 100 - text_bottom - 4
        if n_interactions <= 2 and room >= 40:
            col_w = (100 - 2 * MARGIN - (n_interactions - 1) * 3) / n_interactions
            for i in range(n_interactions):
                geo["interactions"].append(((MARGIN + i * (col_w + 3), text_bottom + 2, col_w, room), False))
        else:
            size = 12
            for i in range(n_interactions):
                geo["interactions"].append(((MARGIN + i * (size + 3), 100 - size * SLIDE_RATIO - 3, size,
                                             size * SLIDE_RATIO), True))
    return geo


def layout(title, blocks, s, line):
    texts = [b for b in blocks if b.get("library") == "H5P.AdvancedText"]
    media = [b for b in blocks if b.get("library") in MEDIA]
    interactions = [b for b in blocks if b.get("library") not in MEDIA and b.get("library") != "H5P.AdvancedText"]
    text_md = "\n\n".join(b["text"] for b in texts)
    geo = arrange(title, [text_md] if texts else [], [_media_ratio(m, s) for m in media], len(interactions),
                  lambda msg: s.warn(line, f"diapo « {title[:30]} » : {msg}"))
    elements = [_element({"library": "H5P.AdvancedText", "text": f"## {title}"}, *geo["title"])]
    if texts:
        elements.append(_element({"library": "H5P.AdvancedText", "text": text_md}, *geo["texts"][0]))
    for m, box in zip(media, geo["media"]):
        elements.append(_element(m, *box))
    for i, (act, (box, as_button)) in enumerate(zip(interactions, geo["interactions"])):
        if as_button:
            label = act.get("metadata", {}).get("title") or f"Question {i + 1}"
            elements.append(_element(act, *box, displayAsButton=True, buttonSize="big", title=label))
        else:
            elements.append(_element(act, *box))
    return elements


@adapter("H5P.CoursePresentation")
def presentation(text, s, arg=None):
    pre, sections = split_headings(lines_of(text), 1)
    if join(pre).strip():
        s.error(0, "texte avant la première diapo : chaque diapo commence par « # Titre »")
    slides = []
    for title, hl, body in sections:
        blocks = parse_blocks(body, s)
        slides.append({"elements": layout(title, blocks, s, hl), "keywords": [{"main": title}]})
    if not slides:
        s.error(None, "aucune diapo : une section « # Titre » par diapo")
    return {"presentation": {"slides": slides}}
