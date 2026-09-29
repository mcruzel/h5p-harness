"""Sugar for word games and ordering: mots croisés, mots mêlés, trier les paragraphes, memory."""
import re

from . import adapter
from .common import BULLET, IMAGE, join, lines_of, media_library

WORD_LINE = re.compile(r"^\s*[-*+]\s+(.+?)\s*(?:\s:\s|\s—\s|\s–\s|\s=\s)\s*(.+?)\s*$")


@adapter("H5P.Crossword")
def crossword(text, s, arg=None):
    intro, words = [], []
    for ln, line in lines_of(text):
        m = WORD_LINE.match(line)
        if m:
            words.append({"answer": m.group(1).strip(), "clue": m.group(2).strip()})
        elif BULLET.match(line):
            s.error(ln, "format attendu: « - RÉPONSE : définition »")
        elif line.strip():
            intro.append(line)
    if len(words) < 2:
        s.error(None, "au moins 2 mots: « - RÉPONSE : définition »")
    out = {"words": words}
    if intro:
        out["taskDescription"] = "\n".join(intro)
    return out


@adapter("H5P.FindTheWords")
def findthewords(text, s, arg=None):
    intro, words = [], []
    for ln, line in lines_of(text):
        b = BULLET.match(line)
        m = re.match(r"^\s*(mots?|words?)\s*:\s*(.+)$", line, re.I)
        if m:
            words += [w.strip() for w in re.split(r"[,;]", m.group(2)) if w.strip()]
        elif b:
            words += [w.strip() for w in re.split(r"[,;]", b.group(2)) if w.strip()]
        elif line.strip():
            intro.append(line)
    if not words:
        s.error(None, "aucun mot: lignes « - mot » ou « mots: a, b, c »")
    return {"taskDescription": "\n".join(intro).strip() or "Trouve les mots cachés dans la grille.",
            "wordList": ",".join(words)}


@adapter("H5P.SortParagraphs")
def sortparagraphs(text, s, arg=None):
    intro, items, media = [], [], None
    for ln, line in lines_of(text):
        b = BULLET.match(line)
        if b and not line[:1].isspace():
            items.append(b.group(2).strip())
        elif items and line[:1] in (" ", "\t") and line.strip():
            items[-1] += "\n" + line.strip()
        elif IMAGE.match(line) and media is None and not items:
            im = IMAGE.match(line)
            media = media_library(im.group(1), im.group(2), im.group(3))
        elif line.strip():
            if items:
                s.error(ln, "texte après la liste: chaque paragraphe est un élément « - … » (dans le bon ordre)")
            else:
                intro.append(line)
    if len(items) < 2:
        s.error(None, "au moins 2 paragraphes « - … », dans l'ordre correct")
    out = {"paragraphs": items, "taskDescription": "\n".join(intro).strip() or "Remets les paragraphes dans l'ordre."}
    if media:
        out["media"] = {"type": media}
    return out


@adapter("H5P.MemoryGame")
def memorygame(text, s, arg=None):
    """'- ![alt](img)' (paire identique) or '- ![alt](img) = ![alt2](img2)' (+ ' :: description')."""
    img = r"!\[([^\]]*)\]\(\s*<?([^)\s>]+)>?\s*\)"
    rx = re.compile(r"^\s*[-*+]\s+" + img + r"(?:\s*=\s*" + img + r")?(?:\s*::\s*(.+))?\s*$")
    cards, intro = [], []
    for ln, line in lines_of(text):
        m = rx.match(line)
        if m:
            card = {"image": {"src": m.group(2)}, "imageAlt": m.group(1) or "image"}
            if m.group(4):
                card["match"] = {"src": m.group(4)}
                card["matchAlt"] = m.group(3) or card["imageAlt"]
            if m.group(5):
                card["description"] = m.group(5).strip()
            if not m.group(1):
                s.warn(ln, "texte alternatif vide")
            cards.append(card)
        elif line.strip():
            if BULLET.match(line):
                s.error(ln, "format attendu: « - ![description](image) » ou « - ![a](img1) = ![b](img2) »")
            else:
                intro.append(line)
    if len(cards) < 2:
        s.error(None, "au moins 2 cartes « - ![description](image) »")
    return {"cards": cards}


_ = join
