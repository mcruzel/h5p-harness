"""Unit and end-to-end tests of the harness (no network, no PHP/Node needed)."""
import hashlib
import json
import zipfile
from pathlib import Path

import pytest

from h5pharness import markers  # noqa: F401  (registers text hooks)
from h5pharness.build import build_one
from h5pharness.engine import Ctx, build_content
from h5pharness.library import Registry
from h5pharness.markdown import to_html
from h5pharness.media import Media

ROOT = Path(__file__).resolve().parent.parent
REG = Registry()


def ctx(**kw):
    return Ctx(registry=REG, lang="fr", media=Media(ROOT), seed="test", **kw)


def build(machine, values, **kw):
    c = ctx(**kw)
    params = build_content(REG.resolve(machine), values, c)
    return params, c


# ---- Markdown ----------------------------------------------------------------------------------

def test_markdown_keeps_allowed_tags_and_shifts_headings():
    field = {"type": "text", "widget": "html", "tags": ["strong", "em", "h2", "h3"]}
    html, errors, warnings = to_html("# Titre\n\nTexte **gras**", field)
    assert html == "<h2>Titre</h2><p>Texte <strong>gras</strong></p>"
    assert not errors and not warnings


def test_markdown_rejects_table_and_strips_disallowed_inline():
    field = {"type": "text", "widget": "html", "tags": ["strong"]}
    _, errors, _ = to_html("| a | b |\n|---|---|\n| 1 | 2 |", field)
    assert errors == ["tableau non autorisé dans ce champ"]
    html, errors, warnings = to_html("`code` et *italique*", field)
    assert html == "<p>code et italique</p>" and not errors and len(warnings) == 2


def test_enter_mode_div():
    html, _, _ = to_html("un\n\ndeux", {"type": "text", "widget": "html", "enterMode": "div"})
    assert html == "<div>un</div><div>deux</div>"


# ---- Engine -------------------------------------------------------------------------------------

def test_defaults_are_french_and_single_field_groups_flattened():
    params, c = build("H5P.MultiChoice", {"question": "Q ?", "answers": [
        {"text": "A", "correct": True}, {"text": "B", "correct": False}]})
    assert not c.errors
    assert params["UI"]["checkAnswerButton"] == "Vérifier"
    assert params["overallFeedback"] == [{"from": 0, "to": 100}]      # H5P flattens 1-field groups
    assert params["question"] == "<p>Q ?</p>"


def test_business_rule_no_correct_answer():
    _, c = build("H5P.MultiChoice", {"question": "Q", "answers": [{"text": "A"}, {"text": "B"}]})
    assert any("aucune réponse correcte" in e for e in c.errors)


def test_unknown_field_is_reported_with_suggestion():
    _, c = build("H5P.MultiChoice", {"question": "Q", "answer": [], "answers": [{"text": "A", "correct": True}]})
    assert any("champ inconnu" in e and "answers" in e for e in c.errors)


def test_subcontent_ids_are_deterministic_and_library_versions_pinned():
    values = {"questions": [{"library": "vf", "question": "Q", "correct": "false"}]}
    p1, c1 = build("H5P.QuestionSet", values)
    p2, _ = build("H5P.QuestionSet", values)
    assert not c1.errors
    q = p1["questions"][0]
    assert q["library"] == "H5P.TrueFalse 1.8"
    assert q["subContentId"] == p2["questions"][0]["subContentId"]


def test_subcontent_not_allowed_here():
    _, c = build("H5P.QuestionSet", {"questions": [{"library": "mots-croises", "words": []}]})
    assert any("non accepté ici" in e for e in c.errors)


def test_select_accepts_label_and_boolean_strings():
    params, c = build("H5P.MultiChoice", {"question": "Q", "answers": [{"text": "A", "correct": "oui"}],
                                          "behaviour": {"type": "multi"}})
    assert not c.errors and params["answers"][0]["correct"] is True


def test_preset_applies_only_when_author_is_silent():
    params, _ = build("H5P.MultiChoice", {"question": "Q", "answers": [{"text": "A", "correct": True}],
                                          "behaviour": {"enableRetry": True}},
                      preset={"enableRetry": False, "enableSolutionsButton": False})
    assert params["behaviour"]["enableRetry"] is True
    assert params["behaviour"]["enableSolutionsButton"] is False


# ---- Micro-syntax ---------------------------------------------------------------------------------

def test_blanks_sugar_conversion_and_forbidden_characters():
    params, c = build("H5P.Blanks", {"questions": ["Un {{chat|matou::félin}} dort."]})
    assert not c.errors
    assert "*chat/matou:félin*" in params["questions"][0]
    _, c = build("H5P.Blanks", {"questions": ["Il est {{10:30}}."]})
    assert any("interprété par H5P" in e for e in c.errors)


def test_mark_the_words_single_word():
    _, c = build("H5P.MarkTheWords", {"taskDescription": "x", "textField": "Le {{chat noir}} dort."})
    assert any("un seul mot" in e for e in c.errors)


# ---- End to end ---------------------------------------------------------------------------------

SOURCES = sorted((ROOT / "sources").rglob("*.md")) + sorted((ROOT / "tests" / "examples").glob("*.md"))


@pytest.mark.parametrize("src", SOURCES, ids=lambda p: p.stem)
def test_sources_build(src, tmp_path):
    res = build_one(src, REG, out_dir=tmp_path, offline=True)
    assert res.ok, "\n".join(res.errors)
    with zipfile.ZipFile(res.out) as z:
        h5p = json.loads(z.read("h5p.json"))
        assert h5p["mainLibrary"] == res.machine
        json.loads(z.read("content/content.json"))


def test_build_is_reproducible(tmp_path):
    src = ROOT / "sources" / "exemples" / "quiz-cellule.md"
    a = build_one(src, REG, out_dir=tmp_path / "a", offline=True)
    b = build_one(src, REG, out_dir=tmp_path / "b", offline=True)
    digest = [hashlib.sha256(r.out.read_bytes()).hexdigest() for r in (a, b)]
    assert digest[0] == digest[1]
