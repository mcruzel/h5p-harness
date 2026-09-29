"""Sugar for cards: cartes de dialogue, flashcards."""
from . import adapter
from .common import IMAGE, image_field, join, lines_of, split_headings


def _card_parts(body, s):
    text, image, alt, tips = [], None, None, {}
    for ln, line in body:
        im = IMAGE.match(line)
        if im and image is None:
            image, alt = image_field(im.group(1), im.group(2), im.group(3)), im.group(1)
            continue
        st = line.strip()
        if st.startswith("?"):
            tips.setdefault("front", st[1:].strip())
            continue
        text.append((ln, line))
    return join(text), image, alt, tips


@adapter("H5P.Dialogcards")
def dialogcards(text, s, arg=None):
    """## recto  /  verso (texte)  /  ![alt](image)  /  ? indice"""
    pre, sections = split_headings(lines_of(text), 2)
    dialogs = []
    for heading, hl, body in sections:
        back, image, alt, tips = _card_parts(body, s)
        if not back:
            s.error(hl, f"carte « {heading[:30]} »: verso vide (texte sous le titre ##)")
        card = {"text": heading, "answer": back}
        if image:
            card["image"] = image
            card["imageAltText"] = alt or heading
        if tips:
            card["tips"] = tips
        dialogs.append(card)
    if not dialogs:
        s.error(None, "aucune carte: une section « ## recto » suivie du verso")
    out = {"dialogs": dialogs}
    intro = join(pre)
    if intro:
        first, _, rest = intro.partition("\n")
        if first.startswith("# "):
            out["title"] = first[2:].strip()
            intro = rest.strip()
        if intro:
            out["description"] = intro
    return out


@adapter("H5P.Flashcards")
def flashcards(text, s, arg=None):
    """## question / réponse (texte court, saisie par l'élève) / ![alt](image) / ? indice"""
    pre, sections = split_headings(lines_of(text), 2)
    cards = []
    for heading, hl, body in sections:
        answer, image, alt, tips = _card_parts(body, s)
        card = {"text": heading, "answer": answer}
        if image:
            card["image"] = image
            card["imageAltText"] = alt or heading
        if tips.get("front"):
            card["tip"] = tips["front"]
        cards.append(card)
    if not cards:
        s.error(None, "aucune carte: une section « ## question » suivie de la réponse")
    return {"cards": cards, "description": join(pre) or "Réponds à chaque carte."}
