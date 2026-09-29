"""Sugar for Branching Scenario: named nodes instead of numeric indexes.

    # Titre du scénario
    Sous-titre de l'écran d'accueil.        (+ image facultative)

    ## debut                                 nœud = section « ## identifiant »
    Texte Markdown (ou une image, une vidéo, un bloc ::: type … :::)
    → choix                                  suite (→ fin, ou → fin: Titre (score))

    ## choix ? Que fais-tu ?                 nœud question : « ## identifiant ? question »
    - Je préviens le professeur → bravo
      > Bon réflexe !                        retour affiché (facultatif)
    - J'essuie avec un mouchoir → fin: Accident (0)
"""
import re

from . import adapter
from .common import BULLET, IMAGE, join, lines_of, split_headings
from .containers import parse_blocks

ARROW = re.compile(r"^\s*(?:→|->|=>)\s*(.+?)\s*$")
END = re.compile(r"^fin(?:\s*:\s*(.*?))?(?:\s*\((-?\d+(?:[.,]\d+)?)\))?\s*$", re.I)
CHOICE = re.compile(r"^(.*?)\s*(?:→|->|=>)\s*(.+?)\s*$")


def _slug(text):
    return re.sub(r"[^\w-]+", "-", text.strip().lower()).strip("-")


def _target(text):
    """'id' -> ('id', None); 'fin: Titre (5)' -> (None, {'title':…, 'endScreenScore': 5})."""
    m = END.match(text.strip())
    if m:
        fb = {}
        if m.group(1):
            fb["title"] = m.group(1).strip()
        if m.group(2):
            fb["endScreenScore"] = float(m.group(2).replace(",", "."))
        return None, fb
    return _slug(text), None


@adapter("H5P.BranchingScenario")
def branchingscenario(text, s, arg=None):
    pre, sections = split_headings(lines_of(text), 2)
    title, intro, start_image = None, [], None
    for ln, line in pre:
        h = re.match(r"^#\s+(.+)$", line)
        im = IMAGE.match(line)
        if h and title is None:
            title = h.group(1).strip()
        elif im and start_image is None:
            start_image = im
        elif line.strip():
            intro.append(line)
    if not sections:
        s.error(None, "aucun nœud : sections « ## identifiant » (texte) ou « ## identifiant ? question »")
        return {}
    ids, nodes = {}, []
    for heading, hl, body in sections:
        node_id, _, question = heading.partition("?")
        key = _slug(node_id)
        if not key:
            s.error(hl, "identifiant de nœud manquant : « ## identifiant »")
            continue
        if key in ids:
            s.error(hl, f"identifiant « {key} » déjà utilisé")
        ids[key] = len(nodes)
        nodes.append((key, question.strip(), hl, body))
    content, scored = [], False
    for index, (key, question, hl, body) in enumerate(nodes):
        if question:
            alternatives = []
            for ln, line in body:
                b = BULLET.match(line)
                if b and not line[:1].isspace():
                    c = CHOICE.match(b.group(2))
                    if not c:
                        s.error(ln, "choix attendu : « - texte → identifiant » (ou → fin: Titre (score))")
                        continue
                    target, end_fb = _target(c.group(2))
                    alt = {"text": c.group(1).strip(), "nextContentId": -1}
                    if target is not None:
                        if target not in ids:
                            s.error(ln, f"nœud « {target} » inconnu (identifiants : {', '.join(ids)})")
                        else:
                            alt["nextContentId"] = ids[target]
                    if end_fb:
                        alt["feedback"] = dict(end_fb)
                        scored = scored or "endScreenScore" in end_fb
                    alternatives.append(alt)
                elif line.strip().startswith(">") and alternatives:
                    fb = alternatives[-1].setdefault("feedback", {})
                    fb["subtitle" if "title" in fb else "title"] = line.strip()[1:].strip()
                elif line.strip():
                    s.error(ln, "dans un nœud question, seulement des choix « - texte → identifiant »")
            if len(alternatives) < 2:
                s.error(hl, f"nœud « {key} » : au moins 2 choix")
            content.append({"type": {"library": "H5P.BranchingQuestion",
                                     "branchingQuestion": {"question": question, "alternatives": alternatives}}})
            continue
        next_id, feedback, kept = (index + 1 if index + 1 < len(nodes) else -1), None, []
        for ln, line in body:
            a = ARROW.match(line)
            if a:
                target, end_fb = _target(a.group(1))
                if target is None:
                    next_id, feedback = -1, end_fb or None
                    scored = scored or bool(end_fb and "endScreenScore" in end_fb)
                elif target not in ids:
                    s.error(ln, f"nœud « {target} » inconnu (identifiants : {', '.join(ids)})")
                else:
                    next_id = ids[target]
            else:
                kept.append((ln, line))
        blocks = parse_blocks(kept, s)
        if not blocks:
            s.error(hl, f"nœud « {key} » vide")
            continue
        if len(blocks) > 1:
            texts = [b for b in blocks if b.get("library") == "H5P.AdvancedText"]
            if len(texts) == len(blocks):
                blocks = [{"library": "H5P.AdvancedText", "text": "\n\n".join(b["text"] for b in texts)}]
            else:
                s.error(hl, f"nœud « {key} » : un seul contenu par nœud (texte OU image OU bloc ::: …)")
        item = {"type": blocks[0], "nextContentId": next_id}
        if feedback:
            item["feedback"] = feedback
        content.append(item)
    bs = {"title": title or "Scénario", "content": content,
          "startScreen": {"startScreenTitle": title or "Scénario", "startScreenSubtitle": "\n".join(intro)},
          "endScreens": [{"endScreenTitle": "Fin", "endScreenScore": 0, "contentId": -1}]}
    if start_image:
        bs["startScreen"]["startScreenImage"] = {"src": start_image.group(2)}
        bs["startScreen"]["startScreenAltText"] = start_image.group(1)
    out = {"branchingScenario": bs}
    if scored:
        bs["scoringOptionGroup"] = {"scoringOption": "static-end-score"}
    return out


_ = join
