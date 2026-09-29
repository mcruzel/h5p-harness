"""Sugar for question types: QCM, vrai/faux, trous, glisser/marquer les mots, choix unique, quiz, résumé."""
import re

from . import adapter, parse_sugar
from .common import (CHECK, IMAGE, join, lines_of, media_library, paragraphs, parse_choices, split_headings)

SUGAR_BLANK = re.compile(r"\{\{.+?\}\}|(?<!\*)\*(?!\*)[^*\n]+\*")
TRUE_WORDS = {"vrai", "true", "oui", "yes", "juste", "correct"}
FALSE_WORDS = {"faux", "false", "non", "no", "incorrect"}


@adapter("H5P.MultiChoice")
def multichoice(text, s, arg=None):
    q = parse_choices(lines_of(text), s)
    if not q["answers"]:
        s.error(None, "aucune réponse: écrire des lignes « - [x] bonne réponse » / « - [ ] distracteur »")
    answers = []
    for a in q["answers"]:
        item = {"text": a["text"], "correct": a["correct"]}
        tf = {}
        if a.get("feedback"):
            tf["chosenFeedback"] = a["feedback"]
        if a.get("not_chosen"):
            tf["notChosenFeedback"] = a["not_chosen"]
        if a.get("tip"):
            tf["tip"] = a["tip"]
        if tf:
            item["tipsAndFeedback"] = tf
        answers.append(item)
    out = {"question": join(q["question"]), "answers": answers}
    if q["media"]:
        out["media"] = {"type": q["media"]}
    return out


@adapter("H5P.TrueFalse")
def truefalse(text, s, arg=None):
    q = parse_choices(lines_of(text), s)
    body = q["question"]
    correct, fb_ok, fb_ko = None, None, None
    rest = []
    for ln, line in body:
        m = re.match(r"^\s*(réponse|reponse|answer)\s*:\s*(\w+)\s*$", line, re.I)
        if m:
            arg = m.group(2)
        else:
            rest.append((ln, line))
    if arg:
        w = arg.strip().lower()
        correct = "true" if w in TRUE_WORDS else "false" if w in FALSE_WORDS else None
        if correct is None:
            s.error(None, f"réponse « {arg} »: écrire vrai ou faux")
    for a in q["answers"]:
        w = re.sub(r"[^\w]", "", a["text"].lower())
        value = "true" if w in TRUE_WORDS else "false" if w in FALSE_WORDS else None
        if value is None:
            s.error(a["line"], "options possibles: « - [x] Vrai » et « - [ ] Faux »")
            continue
        if a["correct"]:
            correct = value
            fb_ok = a.get("feedback") or fb_ok
        else:
            fb_ko = a.get("feedback") or fb_ko
    if correct is None:
        s.error(None, "bonne réponse inconnue: cocher « - [x] Vrai » ou « - [x] Faux » (ou « réponse: faux »)")
    out = {"question": join(rest), "correct": correct or "true"}
    behaviour = {}
    if fb_ok:
        behaviour["feedbackOnCorrect"] = fb_ok
    if fb_ko:
        behaviour["feedbackOnWrong"] = fb_ko
    if behaviour:
        out["behaviour"] = behaviour
    if q["media"]:
        out["media"] = {"type": q["media"]}
    return out


def _intro_and_body(text, s, marker=SUGAR_BLANK):
    """Paragraphs before the first one holding a marker = task description; image line = media."""
    intro, body, media, started = [], [], None, False
    for start, para in paragraphs(lines_of(text)):
        if not started and len(para) == 1 and IMAGE.match(para[0]):
            im = IMAGE.match(para[0])
            media = media_library(im.group(1), im.group(2), im.group(3))
            continue
        if not started and not any(marker.search(l) for l in para):
            intro.append("\n".join(para))
            continue
        started = True
        body.append((start, para))
    return "\n\n".join(intro), body, media


@adapter("H5P.Blanks")
def blanks(text, s, arg=None):
    intro, body, media = _intro_and_body(text, s)
    if not body:
        s.error(None, "aucun trou: écrire {{réponse}} dans le texte ({{réponse|variante::indice}})")
    out = {"questions": ["\n".join(p) for _, p in body]}
    if intro:
        out["text"] = intro
    if media:
        out["media"] = {"type": media}
    return out


@adapter("H5P.DragText")
def dragtext(text, s, arg=None):
    distractors = []
    kept = []
    for ln, line in lines_of(text):
        m = re.match(r"^\s*(distracteurs?|distractors?)\s*:\s*(.*)$", line, re.I)
        if m:
            distractors += [w.strip() for w in re.split(r"[,;]", m.group(2)) if w.strip()]
        else:
            kept.append(line)
    intro, body, media = _intro_and_body("\n".join(kept), s)
    if not body:
        s.error(None, "aucun mot à glisser: écrire {{mot}} dans le texte ({{mot::indice}})")
    out = {"textField": "\n\n".join("\n".join(p) for _, p in body)}
    out["taskDescription"] = intro or "Glisse les mots dans les cases."
    if distractors:
        out["distractors"] = " ".join(f"*{d.strip('*')}*" for d in distractors)
    if media:
        out["media"] = {"type": media}
    return out


@adapter("H5P.MarkTheWords")
def markthewords(text, s, arg=None):
    intro, body, media = _intro_and_body(text, s)
    if not body:
        s.error(None, "aucun mot à marquer: écrire {{mot}} autour de chaque mot correct")
    out = {"textField": "\n\n".join("\n".join(p) for _, p in body),
           "taskDescription": intro or "Clique sur les mots demandés."}
    if media:
        out["media"] = {"type": media}
    return out


@adapter("H5P.SingleChoiceSet")
def singlechoiceset(text, s, arg=None):
    pre, sections = split_headings(lines_of(text), 2)
    if not sections:
        sections = [(None, 0, lines_of(text))]
    choices = []
    for heading, hl, body in sections:
        q = parse_choices(body, s, allow_media=False)
        question = "\n".join(x for x in [heading or "", join(q["question"])] if x).strip()
        answers = q["answers"]
        good = [a for a in answers if a["correct"]]
        if len(good) != 1:
            s.error(hl, f"« {question[:40]} »: exactement une réponse [x] attendue ({len(good)} trouvée(s))")
        ordered = good[:1] + [a for a in answers if not a["correct"]]  # H5P: the first answer is the right one
        choices.append({"question": question, "answers": [a["text"] for a in ordered]})
    return {"choices": choices}


@adapter("H5P.Summary")
def summary(text, s, arg=None):
    pre, sections = split_headings(lines_of(text), 2)
    groups = sections or [(None, 0, [])]
    if not sections:
        # sets separated by blank lines between lists
        groups, cur = [], []
        for ln, line in lines_of(text):
            if CHECK.match(line) or (cur and line.strip().startswith("?")):
                cur.append((ln, line))
            elif not line.strip() and cur:
                groups.append((None, cur[0][0], cur))
                cur = []
            elif line.strip():
                pre.append((ln, line))
        if cur:
            groups.append((None, cur[0][0], cur))
    summaries = []
    for heading, hl, body in groups:
        q = parse_choices(body, s, allow_media=False)
        good = [a for a in q["answers"] if a["correct"]]
        if len(good) != 1:
            s.error(hl, f"chaque série d'affirmations: une seule [x] (trouvé {len(good)})")
            continue
        ordered = good + [a for a in q["answers"] if not a["correct"]]
        item = {"summary": [a["text"] for a in ordered]}
        tip = next((a.get("tip") for a in q["answers"] if a.get("tip")), None)
        if tip:
            item["tip"] = tip
        summaries.append(item)
    out = {"summaries": summaries}
    intro = join(pre)
    if intro:
        out["intro"] = intro
    return out


@adapter("H5P.AdvancedText")
def advancedtext(text, s, arg=None):
    return {"text": text.strip("\n")}


@adapter("H5P.Essay")
def essay(text, s, arg=None):
    """Consigne, then '- mot-clé | variante (points)' lines, optional 'Exemple:' paragraph."""
    task, keywords, sample, media = [], [], [], None
    mode = "task"
    for ln, line in lines_of(text):
        m = re.match(r"^\s*[-*+]\s+(.+?)\s*(?:\((\d+(?:[.,]\d+)?)\s*pts?\))?\s*$", line)
        if re.match(r"^\s*(exemple|réponse attendue|solution)\s*:\s*$", line, re.I):
            mode = "sample"
            continue
        if mode == "task" and m:
            words = [w.strip() for w in m.group(1).split("|") if w.strip()]
            kw = {"keyword": words[0], "alternatives": words[1:]}
            if m.group(2):
                kw["options"] = {"points": float(m.group(2).replace(",", "."))}
            keywords.append(kw)
            continue
        im = IMAGE.match(line)
        if im and media is None and mode == "task":
            media = media_library(im.group(1), im.group(2), im.group(3))
            continue
        (task if mode == "task" else sample).append(line)
    if not keywords:
        s.error(None, "aucun mot-clé: lignes « - mot-clé | variante (2 pts) »")
    out = {"taskDescription": "\n".join(task).strip(), "keywords": keywords}
    if sample:
        out["solution"] = {"sample": "\n".join(sample).strip()}
    if media:
        out["media"] = {"type": media}
    return out


QUIZ_TYPES = ("H5P.MultiChoice", "H5P.TrueFalse", "H5P.Blanks", "H5P.DragText", "H5P.MarkTheWords",
              "H5P.Essay", "H5P.SingleChoiceSet")


@adapter("H5P.QuestionSet")
def questionset(text, s, arg=None):
    pre, sections = split_headings(lines_of(text), 2)
    if not sections:
        s.error(None, "aucune question: une section « ## qcm » (ou vf, trous, glisser-mots…) par question")
    questions = []
    for heading, hl, body in sections:
        kind, _, qarg = heading.partition(":")
        try:
            machine, _, _ = s.ctx.registry.machine_of(kind.strip())
        except KeyError:
            s.error(hl, f"type de question « {kind.strip()} » inconnu")
            continue
        sub = parse_sugar(machine, join(body), s.ctx, s.path, line_offset=s.line_offset + hl + 1,
                          arg=qarg.strip() or None)
        questions.append({"library": machine, **sub})
    out = {"questions": questions}
    intro = join(pre)
    if intro:
        first = intro.split("\n", 1)
        title = first[0].lstrip("# ").strip() if first[0].startswith("#") else None
        out["introPage"] = {"showIntroPage": True, "introduction": first[1] if title and len(first) > 1 else intro}
        if title:
            out["introPage"]["title"] = title
    return out
