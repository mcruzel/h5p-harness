"""Content-type rules that semantics.json cannot express (the H5P editor or runtime enforces them)."""
import re

from .markdown import html_to_text

RULES = {}


def rule(machine):
    def deco(fn):
        RULES[machine] = fn
        return fn
    return deco


def check(machine, params, ctx, path):
    fn = RULES.get(machine)
    if fn and isinstance(params, dict):
        fn(params, ctx, path)


@rule("H5P.MultiChoice")
def _multichoice(p, ctx, path):
    answers = p.get("answers") or []
    correct = sum(1 for a in answers if isinstance(a, dict) and a.get("correct"))
    if answers and correct == 0:
        ctx.error(path + ["answers"], "aucune réponse correcte")
    if (p.get("behaviour") or {}).get("type") == "single" and correct > 1:
        ctx.error(path + ["behaviour", "type"], "type « single » mais plusieurs réponses correctes")
    if len(answers) < 2:
        ctx.warn(path + ["answers"], "une seule réponse proposée")


@rule("H5P.SingleChoiceSet")
def _singlechoiceset(p, ctx, path):
    for i, c in enumerate(p.get("choices") or []):
        if len((c or {}).get("answers") or []) < 2:
            ctx.error(path + ["choices", i, "answers"], "au moins 2 réponses (la 1re est la bonne)")


@rule("H5P.Summary")
def _summary(p, ctx, path):
    for i, s in enumerate(p.get("summaries") or []):
        if len((s or {}).get("summary") or []) < 2:
            ctx.error(path + ["summaries", i, "summary"], "au moins 2 affirmations (la 1re est la bonne)")


@rule("H5P.Crossword")
def _crossword(p, ctx, path):
    words = [w for w in (p.get("words") or []) if isinstance(w, dict) and w.get("answer")]
    for i, w in enumerate(words):
        ans = html_to_text(w["answer"])
        if not re.fullmatch(r"[^\W\d_]+(?:[ '-][^\W\d_]+)*", ans):
            ctx.error(path + ["words", i, "answer"], f"« {ans} »: lettres uniquement (espaces tolérés)")
    letters = [set(html_to_text(w["answer"]).upper()) - {" ", "-", "'"} for w in words]
    for i, w in enumerate(words):
        if not w.get("fixWord") and not any(letters[i] & letters[j] for j in range(len(words)) if j != i):
            ctx.error(path + ["words", i, "answer"],
                      f"« {html_to_text(w['answer'])} » ne partage aucune lettre avec les autres mots "
                      "(la grille ne pourra pas se construire)")


@rule("H5P.QuestionSet")
def _questionset(p, ctx, path):
    if p.get("poolSize") and p["poolSize"] > len(p.get("questions") or []):
        ctx.error(path + ["poolSize"], "plus grand que le nombre de questions")


@rule("H5P.DragQuestion")
def _dragquestion(p, ctx, path):
    task = (p.get("question") or {}).get("task") or {}
    elements = task.get("elements") or []
    zones = task.get("dropZones") or []
    for zi, z in enumerate(zones):
        for ref in (z or {}).get("correctElements") or []:
            if not str(ref).isdigit() or int(ref) >= len(elements):
                ctx.error(path + ["question", "task", "dropZones", zi, "correctElements"],
                          f"élément n°{ref} inexistant (indices à partir de 0, {len(elements)} élément(s))")
    for ei, e in enumerate(elements):
        for ref in (e or {}).get("dropZones") or []:
            if not str(ref).isdigit() or int(ref) >= len(zones):
                ctx.error(path + ["question", "task", "elements", ei, "dropZones"],
                          f"zone n°{ref} inexistante (indices à partir de 0, {len(zones)} zone(s))")


@rule("H5P.FindTheWords")
def _findthewords(p, ctx, path):
    words = p.get("wordList")
    if isinstance(words, str):
        items = [w.strip() for w in words.split(",") if w.strip()]
        if not items:
            ctx.error(path + ["wordList"], "liste de mots vide (mots séparés par des virgules)")
        for w in items:
            if not re.fullmatch(r"[^\W\d_]+", w):
                ctx.error(path + ["wordList"], f"« {w} »: lettres uniquement, sans espace")
