"""Text fields whose content carries H5P micro-syntax (no escaping exists in H5P).

Two ways to write them:
- harness syntax `{{réponse|variante::indice}}` (recommended): the rest of the text is ordinary
  Markdown, `**gras**` / `*italique*` included, because H5P markers are only produced from `{{…}}`;
- raw H5P syntax `*réponse/variante:indice*` (when the text has no `{{…}}`): then every `*` is a
  marker and emphasis must be written `_italique_` / `__gras__`.
"""
import html
import re

from . import markdown
from .engine import TEXT_HOOKS

SUGAR = re.compile(r"\{\{(.+?)\}\}", re.S)
STAR = re.compile(r"\*(?!\*)([^*\n]+?)\*")
UNDERSCORES = re.compile(r"_{3,}")
TOKEN = re.compile("(\\d+)")
EMPHASIS = re.compile(r"(\*\*|__)(?=\S)(.+?)(?<=\S)\1|(?<![\w*])([*_])(?=\S)(.+?)(?<=\S)\3(?![\w*])")


def _split_sugar(body):
    body, _, tip = body.partition("::")
    return [a.strip() for a in body.split("|")], tip.strip()


def _marker(body, ctx, path, allow_alternatives=True, allow_tip=True, single_word=False, what="réponse"):
    """{{…}} body -> H5P marker '*a/b:tip*' with the checks H5P cannot do."""
    answers, tip = _split_sugar(body)
    forbidden = "*" + ("/" if allow_alternatives else "") + (":" if allow_tip else "")
    for a in answers:
        if not a:
            ctx.error(path, f"{what} vide dans {{{{…}}}}")
        elif any(c in a for c in forbidden):
            bad = "".join(sorted({c for c in a if c in forbidden}))
            ctx.error(path, f"{what} « {a} »: « {bad} » est interprété par H5P (aucun échappement possible)")
        if single_word and re.search(r"\s", a):
            ctx.error(path, f"« {a} »: un seul mot par marque (H5P ne marque pas les expressions)")
    if len(answers) > 1 and not allow_alternatives:
        ctx.error(path, f"« {body} »: une seule réponse possible ici (pas de |)")
    if tip and not allow_tip:
        ctx.error(path, f"« {body} »: pas d'indice (::) possible ici")
    if ":" in tip or "*" in tip:
        ctx.error(path, f"indice « {tip} »: caractères * et : interdits")
    return "*" + "/".join(answers) + (f":{tip}" if tip else "") + "*"


def _rich(text, field, ctx, path, count_what, **opts):
    """Markdown field with markers. Returns HTML (markers kept verbatim, HTML-escaped)."""
    if SUGAR.search(text):
        markers = []

        def keep(m):
            markers.append(_marker(m.group(1), ctx, path, **opts))
            return f"{len(markers) - 1}"

        source = SUGAR.sub(keep, text)
        out, errors, warnings = markdown.to_html(source, field)
        out = TOKEN.sub(lambda m: html.escape(markers[int(m.group(1))], quote=False), out)
    else:
        if not STAR.search(text):
            ctx.error(path, f"aucun {count_what}: écrire {{{{…}}}} autour de la réponse")
            return text
        out, errors, warnings = markdown.to_html(text, field, protect=STAR)
    for e in errors:
        ctx.error(path, e)
    for w in warnings:
        ctx.warn(path, w)
    return out


def blanks_question(text, field, ctx, path):
    """H5P.Blanks line of text: *answer/alternative:tip* (a block may also hold no blank)."""
    if not SUGAR.search(text) and not STAR.search(text):
        out, errors, warnings = markdown.to_html(text, field)
        for e in errors:
            ctx.error(path, e)
        return out
    return _rich(text, field, ctx, path, "trou")


def markthewords_text(text, field, ctx, path):
    """H5P.MarkTheWords: *word* marks single words."""
    if not SUGAR.search(text):
        for m in STAR.finditer(text):
            if re.search(r"\s", m.group(1)):
                ctx.error(path, f"« {m.group(1)} »: un seul mot par marque")
    return _rich(text, field, ctx, path, "mot à marquer", allow_alternatives=False, allow_tip=False,
                 single_word=True, what="mot")


def dragtext_text(text, field, ctx, path):
    """H5P.DragText (plain textarea): *answer:tip*; one answer per gap; no formatting possible."""
    if SUGAR.search(text):
        plain = EMPHASIS.sub(lambda m: m.group(2) or m.group(4), SUGAR.sub(lambda m: "", text))
        if plain != SUGAR.sub(lambda m: "", text):
            ctx.warn(path, "gras/italique impossibles dans ce texte (retirés)")
        parts = iter(SUGAR.findall(text))
        text = re.sub("", lambda _m: _marker(next(parts), ctx, path, allow_alternatives=False), plain)
    elif not STAR.search(text):
        ctx.error(path, "aucun mot à glisser: écrire {{mot}} (ou *mot*)")
    return text.strip("\n")


def dragtext_distractors(text, field, ctx, path):
    words = [w.strip() for w in re.split(r"[\n,;]+", text) if w.strip()]
    out = []
    for w in words:
        if w.startswith("*") and w.endswith("*"):
            out.append(w)
        elif SUGAR.fullmatch(w):
            out.append(_marker(SUGAR.fullmatch(w).group(1), ctx, path, allow_alternatives=False, allow_tip=False))
        else:
            out.extend(f"*{x}*" for x in w.split() if x)
    return " ".join(out)


def advancedblanks_text(text, field, ctx, path):
    """H5P.AdvancedBlanks: blanks are ___ (3+ underscores), solutions go in blanksList."""
    if not UNDERSCORES.search(text):
        ctx.error(path, "aucun trou: écrire ___ (au moins trois tirets bas) à chaque trou")
    out, errors, warnings = markdown.to_html(text, field, protect=UNDERSCORES)
    for e in errors:
        ctx.error(path, e)
    for w in warnings:
        ctx.warn(path, w)
    return out


def marktheletters_text(text, field, ctx, path):
    """H5P.MarkTheLetters: correct letters are *x* (single characters); {{x}} also accepted."""
    text = text.replace("\\*", "*")  # authors often escape the asterisks to protect them from Markdown
    if SUGAR.search(text):
        for body in SUGAR.findall(text):
            if len(body.strip()) != 1:
                ctx.error(path, f"« {body} » : une seule lettre par marque")
        text = SUGAR.sub(lambda m: f"*{m.group(1).strip()}*", text)
    if not STAR.search(text):
        ctx.error(path, "aucune lettre marquée : écrire *x* (ou {{x}}) autour de chaque lettre à trouver")
    out, errors, warnings = markdown.to_html(text, field, protect=STAR)
    for e in errors:
        ctx.error(path, e)
    for w in warnings:
        ctx.warn(path, w)
    return out


DATE_ISO = re.compile(r"^(-?\d{1,4})(?:-(\d{1,2})(?:-(\d{1,2}))?)?$")
DATE_FR = re.compile(r"^(\d{1,2})/(\d{1,2})/(-?\d{1,4})$")


def timeline_date(text, field, ctx, path):
    """TimelineJS wants 'AAAA,MM,JJ'; accept ISO (1789-07-14), JJ/MM/AAAA and years."""
    t = str(text).strip()
    m = DATE_ISO.match(t)
    if m:
        return ",".join([m.group(1)] + [f"{int(x):02d}" for x in m.groups()[1:] if x])
    m = DATE_FR.match(t)
    if m:
        return f"{m.group(3)},{int(m.group(2)):02d},{int(m.group(1)):02d}"
    return t


TEXT_HOOKS.update({
    ("H5P.MarkTheLetters", "textField"): marktheletters_text,
    ("H5P.Timeline", "startDate"): timeline_date,
    ("H5P.Timeline", "endDate"): timeline_date,
    ("H5P.Blanks", "question"): blanks_question,
    ("H5P.DragText", "textField"): dragtext_text,
    ("H5P.DragText", "distractors"): dragtext_distractors,
    ("H5P.MarkTheWords", "textField"): markthewords_text,
    ("H5P.AdvancedBlanks", "blanksText"): advancedblanks_text,
})
