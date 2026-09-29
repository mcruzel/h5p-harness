"""Content-type rules that semantics.json cannot express (the H5P editor or runtime enforces them)."""
import re

from .markdown import html_to_text

RULES = {}
FIXUPS = {}

# Values applied under the author's own values (the content type misbehaves without them).
PATCH_DEFAULTS = {
    "H5P.MarkTheLetters": {"solution": ""},            # letter.js crashes on an absent solution
    "H5P.Timeline": {"timeline": {"language": "fr"}},  # TimelineJS interface language
}


def rule(machine):
    def deco(fn):
        RULES[machine] = fn
        return fn
    return deco


def check(machine, params, ctx, path):
    fix = FIXUPS.get(machine)
    if fix and isinstance(params, dict):
        fix(params)
    fn = RULES.get(machine)
    if fn and isinstance(params, dict):
        fn(params, ctx, path)


def fixup(machine):
    def deco(fn):
        FIXUPS[machine] = fn
        return fn
    return deco


PALETTE = ["#1f77b4", "#ff7f0e", "#2ca02c", "#d62728", "#9467bd", "#8c564b", "#e377c2", "#7f7f7f", "#bcbd22", "#17becf"]


@fixup("H5P.Chart")
def _chart_palette(p):
    """The semantics default colour is black for every item: give a readable palette instead."""
    for i, item in enumerate(p.get("listOfTypes") or []):
        if isinstance(item, dict) and item.get("color") in (None, "#000", "#000000"):
            item["color"] = PALETTE[i % len(PALETTE)]


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


@rule("H5P.ImageHotspots")
def _imagehotspots(p, ctx, path):
    for i, h in enumerate(p.get("hotspots") or []):
        pos = (h or {}).get("position") or {}
        for axis in ("x", "y"):
            v = pos.get(axis)
            if isinstance(v, (int, float)) and not 0 <= v <= 100:
                ctx.error(path + ["hotspots", i, "position", axis], f"{v} : position en % de l'image (0 à 100)")


@rule("H5P.ImageHotspotQuestion")
def _findhotspot(p, ctx, path):
    settings = (p.get("imageHotspotQuestion") or {}).get("hotspotSettings") or {}
    for i, h in enumerate(settings.get("hotspot") or []):
        cs = (h or {}).get("computedSettings") or {}
        where = path + ["imageHotspotQuestion", "hotspotSettings", "hotspot", i, "computedSettings"]
        if cs.get("figure") not in (None, "rectangle", "circle"):
            ctx.error(where + ["figure"], f"« {cs.get('figure')} » : rectangle ou circle")
        for k in ("x", "y", "width", "height"):
            v = cs.get(k)
            if isinstance(v, (int, float)) and not 0 <= v <= 100:
                ctx.error(where + [k], f"{v} : en % de l'image (0 à 100)")


@rule("H5P.ThreeDModel")
def _threedmodel(p, ctx, path):
    def walk(v, where):
        if isinstance(v, dict):
            annotation = "text" in v and ("surface" in v or "id" in v or where[-2:-1] == ["annotations"])
            if annotation and not v.get("surface"):
                ctx.warn(where, "annotation sans « surface » : elle ne sera pas affichée par le modèle 3D")
            for k, x in v.items():
                walk(x, where + [k])
        elif isinstance(v, list):
            for i, x in enumerate(v):
                walk(x, where + [i])
    walk(p, path)


@rule("H5P.Collage")
def _collage(p, ctx, path):
    col = p.get("collage") or {}
    template = str(col.get("template") or "")
    if re.fullmatch(r"\d+(-\d+)*", template):
        needed = sum(int(x) for x in template.split("-"))
        have = len(col.get("clips") or [])
        if have != needed:
            ctx.warn(path + ["collage", "clips"],
                     f"la mise en page « {template} » attend {needed} image(s), {have} fournie(s)")


@rule("H5P.MarkTheLetters")
def _markletters(p, ctx, path):
    text = html_to_text(p.get("textField") or "")
    if re.search(r"[^\x00-\x7f]", text):
        ctx.warn(path + ["textField"],
                 "lettres accentuées ou non latines : ce type ne garde que a-z (elles disparaîtront)")
