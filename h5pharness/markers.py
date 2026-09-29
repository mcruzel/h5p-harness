"""Text fields whose content carries H5P micro-syntax (no escaping exists in H5P).

Authors may write the harness syntax `{{réponse|variante::indice}}` (recommended) or the raw
H5P syntax `*réponse/variante:indice*`. In these fields `*` is reserved: use _italique_.
"""
import re

from . import markdown
from .engine import TEXT_HOOKS

SUGAR = re.compile(r"\{\{(.+?)\}\}", re.S)
STAR = re.compile(r"\*(?!\*)([^*\n]+?)\*")
UNDERSCORES = re.compile(r"_{3,}")


def _split_sugar(body):
    body, _, tip = body.partition("::")
    return [a.strip() for a in body.split("|")], tip.strip()


def _sugar_to_star(text, ctx, path, allow_alternatives=True, allow_tip=True, single_word=False, what="réponse"):
    forbidden = "*" + ("/" if allow_alternatives else "") + (":" if allow_tip else "")

    def repl(m):
        answers, tip = _split_sugar(m.group(1))
        for a in answers:
            if not a:
                ctx.error(path, f"{what} vide dans {{{{…}}}}")
            elif any(c in a for c in forbidden):
                bad = "".join(sorted({c for c in a if c in forbidden}))
                ctx.error(path, f"{what} « {a} »: « {bad} » est interprété par H5P (aucun échappement possible)")
            if single_word and re.search(r"\s", a):
                ctx.error(path, f"« {a} »: un seul mot par marque (H5P ne marque pas les expressions)")
        if len(answers) > 1 and not allow_alternatives:
            ctx.error(path, f"« {m.group(1)} »: une seule réponse possible ici (pas de |)")
        if tip and not allow_tip:
            ctx.error(path, f"« {m.group(1)} »: pas d'indice (::) possible ici")
        if ":" in tip or "*" in tip:
            ctx.error(path, f"indice « {tip} »: caractères * et : interdits")
        inner = "/".join(answers) + (f":{tip}" if tip else "")
        return f"*{inner}*"

    return SUGAR.sub(repl, text)


def _count(text):
    return len(STAR.findall(text))


def blanks_question(text, field, ctx, path):
    """H5P.Blanks line of text: *answer/alternative:tip*."""
    text = _sugar_to_star(text, ctx, path)
    if _count(text) == 0:
        ctx.error(path, "aucun trou: écrire {{réponse}} (ou *réponse*)")
    out, errors, warnings = markdown.to_html(text, field, protect=STAR)
    for e in errors:
        ctx.error(path, e)
    for w in warnings:
        ctx.warn(path, w)
    return out


def dragtext_text(text, field, ctx, path):
    """H5P.DragText textarea: *answer:tip*, feedback with \\+ and \\- ; one answer per gap."""
    text = _sugar_to_star(text, ctx, path, allow_alternatives=False)
    if _count(text) == 0:
        ctx.error(path, "aucun mot à glisser: écrire {{mot}} (ou *mot*)")
    return text.strip("\n")


def dragtext_distractors(text, field, ctx, path):
    words = [w.strip() for w in re.split(r"[\n,;]+", text) if w.strip()]
    out = []
    for w in words:
        if w.startswith("*") and w.endswith("*"):
            out.append(w)
        elif SUGAR.fullmatch(w):
            out.append(_sugar_to_star(w, ctx, path, allow_alternatives=False, allow_tip=False))
        else:
            out.extend(f"*{x}*" for x in w.split() if x)
    return " ".join(out)


def markthewords_text(text, field, ctx, path):
    """H5P.MarkTheWords: *word* marks single words; literal asterisk: *word***."""
    text = _sugar_to_star(text, ctx, path, allow_alternatives=False, allow_tip=False, single_word=True,
                          what="mot")
    for m in STAR.finditer(text):
        if re.search(r"\s", m.group(1)):
            ctx.error(path, f"« {m.group(1)} »: un seul mot par marque")
    if _count(text) == 0:
        ctx.error(path, "aucun mot à marquer: écrire {{mot}} (ou *mot*)")
    out, errors, warnings = markdown.to_html(text, field, protect=STAR)
    for e in errors:
        ctx.error(path, e)
    for w in warnings:
        ctx.warn(path, w)
    return out


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


TEXT_HOOKS.update({
    ("H5P.Blanks", "question"): blanks_question,
    ("H5P.DragText", "textField"): dragtext_text,
    ("H5P.DragText", "distractors"): dragtext_distractors,
    ("H5P.MarkTheWords", "textField"): markthewords_text,
    ("H5P.AdvancedBlanks", "blanksText"): advancedblanks_text,
})

