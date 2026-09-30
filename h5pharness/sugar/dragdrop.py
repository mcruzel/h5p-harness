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
EXTRA_W, EXTRA_H = 1.6, 0.8     # handle, padding and border H5P adds around a draggable (measured)
LABEL_H = 1.8                   # zone label
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

    statics = [" ".join(intro)] if intro else []
    sizes = [(_text_width(value), 2.25) if kind == "text" else (5.0, 5.0) for _, kind, value, _ in items]
    members = [[k for k, it in enumerate(items) if it[0] == i] for i in range(len(zones))]
    geo = geometry(statics, sizes, members, bool(background), [pos for _, pos in zones])
    out_elements = []
    for text, box in zip(statics, geo["statics"]):  # static instruction text
        out_elements.append({"type": {"library": "H5P.AdvancedText", "text": "\n".join(intro)}, **box,
                             "dropZones": [], "backgroundOpacity": 0})
    first_item = len(out_elements)
    all_zones = [str(i) for i in range(len(zones))]
    for (zi, kind, value, alt), box in zip(items, geo["items"]):
        if kind == "text":
            content = {"library": "H5P.AdvancedText", "text": value}
        else:
            content = {"library": "H5P.Image", "file": {"src": value}}
            if alt:
                content["alt"] = alt
            else:
                content["decorative"] = True
        out_elements.append({"type": content, **box, "dropZones": all_zones})
    out_zones = []
    for i, ((label, pos), box) in enumerate(zip(zones, geo["zones"])):
        correct = [str(first_item + k) for k, it in enumerate(items) if it[0] == i]
        out_zones.append({"label": label, "showLabel": True, **box, "correctElements": correct, "autoAlign": True})
    settings = {"size": {"width": WIDTH_PX, "height": geo["height"]}}
    if background:
        settings["background"] = background
    return {"question": {"settings": settings, "task": {"elements": out_elements, "dropZones": out_zones}}}


def _flow_height(sizes, width):
    """Height taken by items dropped in a zone of this width (H5P aligns them in rows)."""
    x, y, row = 0.0, 0.0, 0.0
    for w, h in sizes:
        w, h = w + EXTRA_W, h + EXTRA_H
        if x and x + w > width:
            x, y, row = 0.0, y + row, 0.0
        x += w
        row = max(row, h)
    return y + row


def geometry(statics, sizes, members, background, zone_positions):
    """Layout of a play area WIDTH_PX wide: static texts on top (full width), then the draggable items in
    rows, then one column per drop zone (or the zone's own position, in %). H5P units: x/y in % of the
    area, width/height in em. statics: texts; sizes: nominal (w, h) of each item in em; members: for
    each zone, the indexes (in sizes) of the items that belong there (to make room for them)."""
    y, boxes = 0.8, []
    for text in statics:
        n_lines = max(1, math.ceil(len(text) / 60))
        boxes.append((0.8, y, W_EM - 1.6, 1.6 * n_lines + 0.6))
        y += 1.6 * n_lines + 0.6 + EXTRA_H + GAP
    x, row_h, placed = 0.8, 0, []
    for w, h in sizes:
        if x + w + EXTRA_W > W_EM - 0.8 and x > 0.8:
            x, y = 0.8, y + row_h + GAP
            row_h = 0
        placed.append((x, y, w, h))
        x += w + EXTRA_W + GAP
        row_h = max(row_h, h + EXTRA_H)
    top_zones = y + row_h + 1.5
    n = max(len(members), 1)
    zone_w = (W_EM - GAP * (n + 1)) / n

    def zone_height(idx, width):
        return max(6.0, LABEL_H + _flow_height([sizes[k] for k in idx if k < len(sizes)], width - 0.6) + 0.8)

    zone_h = max([zone_height(m, zone_w) for m in members] or [6.0])
    height_em = top_zones + zone_h + 1.0 if not background else max(top_zones + 8, W_EM / 2)
    height_px = round(height_em * EM)

    def box(bx, by, bw, bh):
        return {"x": round(bx * EM / WIDTH_PX * 100, 3), "y": round(by * EM / height_px * 100, 3),
                "width": round(bw, 3), "height": round(bh, 3)}

    zones = []
    for i, idx in enumerate(members):
        pos = zone_positions[i] if i < len(zone_positions) else None
        if pos:
            zones.append({"x": pos[0], "y": pos[1], "width": 8.0, "height": round(zone_height(idx, 8.0), 3)})
        else:
            zones.append(box(GAP + i * (zone_w + GAP), top_zones, zone_w, zone_h))
    return {"statics": [box(*b) for b in boxes], "items": [box(*b) for b in placed], "zones": zones,
            "height": height_px}


_ = join
