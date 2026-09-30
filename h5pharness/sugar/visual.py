"""Sugar for image-centred types: image interactive, frise, séquence/paires d'images, devinette,
agamotto, avant/après."""
import re

from . import adapter
from .common import BULLET, IMAGE, join, lines_of, media_library, split_headings

IMG = r"!\[([^\]]*)\]\(\s*<?([^)\s>]+)>?(?:\s+\"([^\"]*)\")?\s*\)"
PAIR = re.compile(r"^\s*[-*+]\s+" + IMG + r"(?:\s*=\s*" + IMG + r")?\s*$")


def _image_lib(alt, src, title=None):
    lib = media_library(alt, src, title)
    if lib.get("library") != "H5P.Image":
        return None
    return lib


def _intro(pre, s):
    text, image = [], None
    for ln, line in pre:
        im = IMAGE.match(line)
        if im and image is None:
            image = im
        elif line.strip():
            text.append(line)
    return "\n".join(text).strip(), image


@adapter("H5P.ImageHotspots")
def imagehotspots(text, s, arg=None):
    """![fond](image) puis « ## x,y Titre » (x, y en %) suivi du contenu du point (texte, image, vidéo)."""
    pre, sections = split_headings(lines_of(text), 2)
    _, image = _intro(pre, s)
    if image is None:
        s.error(None, "image de fond manquante : « ![description](image) » avant les points")
        return {}
    hotspots = []
    for heading, hl, body in sections:
        m = re.match(r"^(\d+(?:[.,]\d+)?)\s*[,;]\s*(\d+(?:[.,]\d+)?)\s*(.*)$", heading)
        if not m:
            s.error(hl, "titre attendu : « ## x,y Titre » (position en % de l'image, ex. « ## 30,45 Le toit »)")
            continue
        content, buf = [], []

        def flush():
            if join(buf).strip():
                content.append({"library": "H5P.Text", "text": join(buf)})
            buf.clear()

        for ln, line in body:
            im = IMAGE.match(line)
            if im:
                flush()
                content.append(media_library(im.group(1), im.group(2), im.group(3)))
            else:
                buf.append((ln, line))
        flush()
        if not content:
            s.error(hl, f"point « {heading} » : contenu vide")
        hotspot = {"position": {"x": float(m.group(1).replace(",", ".")), "y": float(m.group(2).replace(",", ".")),
                                "legacyPositioning": False}, "content": content}
        if m.group(3).strip():
            hotspot["header"] = m.group(3).strip()
        hotspots.append(hotspot)
    if not hotspots:
        s.error(None, "aucun point : sections « ## x,y Titre » (position en %)")
    return {"image": {"src": image.group(2)}, "backgroundImageAltText": image.group(1) or "Image", "hotspots": hotspots}


DATE = r"-?\d{1,4}(?:-\d{1,2}(?:-\d{1,2})?)?|\d{1,2}/\d{1,2}/-?\d{1,4}"
EVENT = re.compile(rf"^({DATE})(?:\s*(?:→|->|–|à)\s*({DATE}))?\s*(?::|—)\s*(.+)$")


def _tl_date(text):
    """ISO (1789-07-14), année (1789, -500) ou JJ/MM/AAAA -> 'AAAA,MM,JJ' (TimelineJS)."""
    if "/" in text:
        d, m, y = text.split("/")
        return f"{y},{int(m):02d},{int(d):02d}"
    neg = text.startswith("-")
    parts = text.lstrip("-").split("-")
    parts[0] = ("-" if neg else "") + parts[0]
    return ",".join([parts[0]] + [f"{int(p):02d}" for p in parts[1:]])


@adapter("H5P.Timeline")
def timeline(text, s, arg=None):
    """# Titre, introduction, puis « ## 1789-07-14 : Événement » (ou « ## 1939 → 1945 : Période ») + texte."""
    pre, sections = split_headings(lines_of(text), 2)
    title, intro = None, []
    for ln, line in pre:
        h = re.match(r"^#\s+(.+)$", line)
        if h and title is None:
            title = h.group(1).strip()
        elif line.strip():
            intro.append(line)
    dates = []
    for heading, hl, body in sections:
        m = EVENT.match(heading)
        if not m:
            s.error(hl, "titre attendu : « ## 1789 : Titre », « ## 1789-07-14 : Titre » ou « ## 1939 → 1945 : Titre »")
            continue
        ev = {"startDate": _tl_date(m.group(1)), "headline": m.group(3).strip()}
        if m.group(2):
            ev["endDate"] = _tl_date(m.group(2))
        body_text = join(body)
        if body_text.strip():
            ev["text"] = body_text
        dates.append(ev)
    if not dates:
        s.error(None, "aucun événement : sections « ## date : titre »")
    tl = {"headline": title or "Frise chronologique", "date": dates, "language": "fr"}
    if intro:
        tl["text"] = "\n".join(intro)
    return {"timeline": tl}


def _image_list(text, s, minimum):
    intro, items = [], []
    for ln, line in lines_of(text):
        m = PAIR.match(line)
        if m:
            items.append((ln, m))
        elif BULLET.match(line):
            s.error(ln, "élément attendu : « - ![description](image) »")
        elif line.strip():
            intro.append(line)
    if len(items) < minimum:
        s.error(None, f"au moins {minimum} images « - ![description](image) »")
    return "\n".join(intro).strip(), items


@adapter("H5P.ImageSequencing")
def imagesequencing(text, s, arg=None):
    """Consigne puis les images dans l'ordre correct : « - ![description](image) »."""
    intro, items = _image_list(text, s, 3)
    out = {"sequenceImages": [{"image": {"src": m.group(2)}, "imageDescription": m.group(1) or f"Image {i + 1}"}
                              for i, (ln, m) in enumerate(items)]}
    if intro:
        out["taskDescription"] = intro
    return out


@adapter("H5P.ImagePair")
def imagepair(text, s, arg=None):
    """Consigne puis une paire par ligne : « - ![a](image1) = ![b](image2) » (ou une image : paire identique)."""
    intro, items = _image_list(text, s, 2)
    cards = []
    for ln, m in items:
        card = {"image": {"src": m.group(2)}, "imageAlt": m.group(1) or "image"}
        if m.group(5):
            card["match"] = {"src": m.group(5)}
            card["matchAlt"] = m.group(4) or card["imageAlt"]
        cards.append(card)
    out = {"cards": cards}
    if intro:
        out["taskDescription"] = intro
    return out


@adapter("H5P.GuessTheAnswer")
def guesstheanswer(text, s, arg=None):
    """Consigne, une image ou vidéo « ![…](…) », puis « Réponse: … » (et « Bouton: … » facultatif)."""
    task, media, answer, label = [], None, None, None
    for ln, line in lines_of(text):
        im = IMAGE.match(line)
        a = re.match(r"^\s*(réponse|reponse|solution|answer)\s*:\s*(.+)$", line, re.I)
        b = re.match(r"^\s*(bouton|button)\s*:\s*(.+)$", line, re.I)
        if im and media is None:
            media = media_library(im.group(1), im.group(2), im.group(3))
        elif a:
            answer = a.group(2).strip()
        elif b:
            label = b.group(2).strip()
        else:
            task.append(line)
    if not answer:
        s.error(None, "réponse manquante : une ligne « Réponse: … »")
    out = {"taskDescription": "\n".join(task).strip(), "solutionText": answer or ""}
    if media:
        out["media"] = {"type": media}
    if label:
        out["solutionLabel"] = label
    return out


@adapter("H5P.Agamotto")
def agamotto(text, s, arg=None):
    """« # Titre » facultatif, puis « ## Libellé » + une image + description, pour chaque étape."""
    pre, sections = split_headings(lines_of(text), 2)
    title = next((re.match(r"^#\s+(.+)$", l).group(1) for _, l in pre if re.match(r"^#\s+(.+)$", l)), None)
    items = []
    for heading, hl, body in sections:
        image, desc = None, []
        for ln, line in body:
            im = IMAGE.match(line)
            if im and image is None:
                image = _image_lib(im.group(1) or heading, im.group(2), im.group(3))
            else:
                desc.append((ln, line))
        if image is None:
            s.error(hl, f"étape « {heading} » : image manquante « ![description](image) »")
            continue
        item = {"image": image, "labelText": heading}
        if join(desc).strip():
            item["description"] = join(desc)
        items.append(item)
    if len(items) < 2:
        s.error(None, "au moins 2 étapes « ## Libellé » avec chacune une image")
    out = {"items": items}
    if title:
        out["title"] = title
    return out


@adapter("H5P.ImageJuxtaposition")
def imagejuxtaposition(text, s, arg=None):
    """Consigne puis deux lignes d'image : avant puis après (le texte alternatif sert de libellé)."""
    imgs, task = [], []
    for ln, line in lines_of(text):
        im = IMAGE.match(line)
        if im:
            imgs.append(im)
        elif line.strip():
            task.append(line)
    if len(imgs) != 2:
        s.error(None, "deux images attendues : « ![Avant](image1) » puis « ![Après](image2) »")
        return {}
    before, after = imgs
    out = {"imageBefore": {"imageBefore": _image_lib(before.group(1) or "Avant", before.group(2)),
                           "labelBefore": before.group(1) or "Avant"},
           "imageAfter": {"imageAfter": _image_lib(after.group(1) or "Après", after.group(2)),
                          "labelAfter": after.group(1) or "Après"}}
    if task:
        out["taskDescription"] = "\n".join(task)
    return out
