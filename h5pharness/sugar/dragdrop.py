"""Sugar for Drag and Drop (H5P.DragQuestion): sorting items into zones, with automatic layout.

    Consigne (texte fixe en haut).
    ![fond](image)            facultatif : image de fond (zones alors à placer avec « @ x,y »)
    ## Mammifères             une zone de dépôt par section (« ## Nom @ 30,40 » = position en %)
    - chat                    éléments à y déposer (texte, ou ![description](image))
    - ![Dauphin](dauphin.png)

Units follow H5P: x/y in % of the play area, width/height in em (16 px).
"""
import math
import re

from . import adapter
from .common import BULLET, IMAGE, join, lines_of, split_headings

WIDTH_PX, EM = 620, 16
W_EM = WIDTH_PX / EM            # 38.75 em
GAP = 0.8
ZONE_AT = re.compile(r"^(.*?)\s*@\s*(\d+(?:[.,]\d+)?)\s*[,;]\s*(\d+(?:[.,]\d+)?)\s*$")


def _text_width(text):
    return min(12.0, max(5.0, len(text) * 0.55 + 1.6))


@adapter("H5P.DragQuestion")
def dragquestion(text, s, arg=None):
    pre, sections = split_headings(lines_of(text), 2)
    intro, background = [], None
    for ln, line in pre:
        im = IMAGE.match(line)
        if im and background is None:
            background = {"src": im.group(2)}
        elif line.strip():
            intro.append(line)
    if not sections:
        s.error(None, "aucune zone : une section « ## Nom de la zone » suivie des éléments « - … » à y déposer")
        return {}
    zones, items = [], []   # items: (zone index, kind, value, alt)
    for zi, (heading, hl, body) in enumerate(sections):
        m = ZONE_AT.match(heading)
        label = m.group(1).strip() if m else heading
        pos = (float(m.group(2).replace(",", ".")), float(m.group(3).replace(",", "."))) if m else None
        if background and not pos:
            s.error(hl, f"zone « {label} » : avec une image de fond, préciser sa position « ## {label} @ x,y » (en %)")
        zones.append((label, pos))
        for ln, line in body:
            b = BULLET.match(line)
            if not b:
                if line.strip():
                    s.error(ln, "élément attendu : « - texte » ou « - ![description](image) »")
                continue
            im = IMAGE.match(b.group(2))
            if im:
                items.append((zi, "image", im.group(2), im.group(1)))
            else:
                items.append((zi, "text", b.group(2).strip(), None))
    if not items:
        s.error(None, "aucun élément à déplacer")
        return {}

    # ---- layout in em ---------------------------------------------------------------------------------
    y = 0.8
    elements = []
    if intro:
        n_lines = max(1, math.ceil(len(" ".join(intro)) / 60))
        elements.append({"type": {"library": "H5P.AdvancedText", "text": "\n".join(intro)},
                         "x": 0.8, "y": y, "width": W_EM - 1.6, "height": 1.6 * n_lines + 0.6,
                         "dropZones": [], "_em": True})
        y += 1.6 * n_lines + 1.2
    x, row_h = 0.8, 0
    placed = []
    for zi, kind, value, alt in items:
        w = _text_width(value) if kind == "text" else 5.0
        h = 2.25 if kind == "text" else 5.0
        if x + w > W_EM - 0.8:
            x, y = 0.8, y + row_h + GAP
            row_h = 0
        placed.append((zi, kind, value, alt, x, y, w, h))
        x += w + GAP
        row_h = max(row_h, h)
    top_zones = y + row_h + 1.5
    n = len(zones)
    per_zone = [sum(1 for it in items if it[0] == i) for i in range(n)]
    zone_w = (W_EM - GAP * (n + 1)) / n
    zone_h = max(6.0, max(per_zone) * 2.9 + 2.2)
    height_em = top_zones + zone_h + 1.0 if not background else max(top_zones + 8, W_EM / 2)
    height_px = round(height_em * EM)

    def pct_x(v):
        return round(v * EM / WIDTH_PX * 100, 3)

    def pct_y(v):
        return round(v * EM / height_px * 100, 3)

    out_elements = []
    for el in elements:  # static instruction text
        out_elements.append({"type": el["type"], "x": pct_x(el["x"]), "y": pct_y(el["y"]),
                             "width": round(el["width"], 3), "height": round(el["height"], 3),
                             "dropZones": [], "backgroundOpacity": 0})
    first_item = len(out_elements)
    all_zones = [str(i) for i in range(n)]
    for zi, kind, value, alt, ex, ey, w, h in placed:
        if kind == "text":
            content = {"library": "H5P.AdvancedText", "text": value}
        else:
            content = {"library": "H5P.Image", "file": {"src": value}}
            if alt:
                content["alt"] = alt
            else:
                content["decorative"] = True
        out_elements.append({"type": content, "x": pct_x(ex), "y": pct_y(ey), "width": round(w, 3),
                             "height": round(h, 3), "dropZones": all_zones})
    out_zones = []
    for i, (label, pos) in enumerate(zones):
        correct = [str(first_item + k) for k, it in enumerate(items) if it[0] == i]
        if pos:
            zx, zy, zw, zh = pos[0], pos[1], 8.0, max(2.5, per_zone[i] * 2.9 + 0.6)
        else:
            zx, zy, zw, zh = pct_x(GAP + i * (zone_w + GAP)), pct_y(top_zones), zone_w, zone_h
        out_zones.append({"label": label, "showLabel": True, "x": zx, "y": zy, "width": round(zw, 3),
                          "height": round(zh, 3), "correctElements": correct, "autoAlign": True})
    settings = {"size": {"width": WIDTH_PX, "height": height_px}}
    if background:
        settings["background"] = background
    return {"question": {"settings": settings, "task": {"elements": out_elements, "dropZones": out_zones}}}


_ = join
