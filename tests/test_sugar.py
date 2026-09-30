"""Markdown shortcuts: each one must produce valid content (built end to end, offline)."""
import json
import textwrap
import zipfile

import pytest

from h5pharness.build import build_one
from h5pharness.library import Registry

REG = Registry()


def build(tmp_path, type_, body, name="doc"):
    src = tmp_path / f"{name}.md"
    src.write_text(f"---\ntype: {type_}\ntitle: Test\n---\n" + textwrap.dedent(body).strip() + "\n", encoding="utf-8")
    res = build_one(src, REG, out_dir=tmp_path / "out", offline=True)
    assert res.ok, "\n".join(res.errors)
    with zipfile.ZipFile(res.out) as z:
        return json.loads(z.read("content/content.json")), res


def test_qcm_feedback_and_tip(tmp_path):
    c, _ = build(tmp_path, "qcm", """
        Question ?
        - [x] Bonne
        - [ ] Mauvaise
          > retour
          ? indice
    """)
    assert c["answers"][1]["tipsAndFeedback"]["chosenFeedback"] == "<p>retour</p>"
    assert c["answers"][1]["tipsAndFeedback"]["tip"] == "<p>indice</p>"


def test_vf_checkbox(tmp_path):
    c, _ = build(tmp_path, "vf", """
        Le ciel est vert.
        - [ ] Vrai
        - [x] Faux
    """)
    assert c["correct"] == "false"


def test_choix_unique_puts_correct_answer_first(tmp_path):
    c, _ = build(tmp_path, "choix-unique", """
        ## 2 + 2 ?
        - [ ] 3
        - [x] 4
    """)
    assert c["choices"][0]["answers"][0].endswith("4</p>") or c["choices"][0]["answers"][0] == "4"


def test_resume_first_statement_correct(tmp_path):
    c, _ = build(tmp_path, "resume", """
        Choisis.
        ## A
        - [ ] faux
        - [x] vrai
    """)
    assert "vrai" in c["summaries"][0]["summary"][0]


def test_glisser_mots_distractors(tmp_path):
    c, _ = build(tmp_path, "glisser-mots", """
        Consigne.

        {{Paris}} est en France.
        Distracteurs: Lyon, Milan
    """)
    assert "*Paris*" in c["textField"] and c["distractors"] == "*Lyon* *Milan*"


def test_quiz_sections(tmp_path):
    c, _ = build(tmp_path, "quiz", """
        ## qcm
        Q ?
        - [x] a
        - [ ] b

        ## vf: vrai
        Vrai ?

        ## trous
        Un {{mot}}.
    """)
    assert [q["library"].split(" ")[0] for q in c["questions"]] == ["H5P.MultiChoice", "H5P.TrueFalse", "H5P.Blanks"]


def test_presentation_layout_stays_on_slide(tmp_path):
    c, res = build(tmp_path, "presentation", """
        # Titre
        Du texte.

        ![Image](/sources/exemples/media/paysage.jpg)

        # Questions
        ::: qcm
        Q ?
        - [x] a
        - [ ] b
        :::
        ::: vf: faux
        Faux ?
        :::
    """)
    for slide in c["presentation"]["slides"]:
        for el in slide["elements"]:
            assert 0 <= el["x"] and el["x"] + el["width"] <= 100.5
            assert 0 <= el["y"] and el["y"] + el["height"] <= 100.5


def test_glisser_deposer_indexes(tmp_path):
    c, _ = build(tmp_path, "glisser-deposer", """
        Classe.
        ## A
        - un
        - deux
        ## B
        - trois
    """)
    task = c["question"]["task"]
    assert task["dropZones"][0]["correctElements"] == ["1", "2"]    # element 0 = the static instruction
    assert task["dropZones"][1]["correctElements"] == ["3"]
    assert task["elements"][0]["dropZones"] == [] if "dropZones" in task["elements"][0] else True


def test_video_interactive_times(tmp_path):
    c, _ = build(tmp_path, "video-interactive", """
        ![Vidéo](/sources/exemples/media/clip.webm)
        transcrit: /sources/exemples/media/etats-eau.vtt
        ## 0:01 qcm
        Q ?
        - [x] a
        - [ ] b
        ## 1:05 signet: Partie 2
    """)
    iv = c["interactiveVideo"]
    assert iv["assets"]["interactions"][0]["duration"] == {"from": 1, "to": 11}
    assert iv["assets"]["bookmarks"][0] == {"time": 65, "label": "Partie 2"}


def test_frise_dates(tmp_path):
    c, _ = build(tmp_path, "frise", """
        # Histoire
        ## 14/07/1789 : Bastille
        ## 1939 → 1945 : Guerre
    """)
    dates = c["timeline"]["date"]
    assert dates[0]["startDate"] == "1789,07,14"
    assert (dates[1]["startDate"], dates[1]["endDate"]) == ("1939", "1945")


def test_livre_chapters(tmp_path):
    c, _ = build(tmp_path, "livre", """
        # Chapitre 1
        Texte.
        # Chapitre 2
        ::: vf: vrai
        Oui ?
        :::
    """)
    assert [ch["metadata"]["title"] for ch in c["chapters"]] == ["Chapitre 1", "Chapitre 2"]


@pytest.mark.parametrize("bad, message", [
    ("## 12 Titre\ntexte", "## x,y Titre"),
])
def test_image_interactive_error_message(tmp_path, bad, message):
    src = tmp_path / "x.md"
    src.write_text(f"---\ntype: image-interactive\ntitle: T\n---\n![f](/sources/exemples/media/paysage.jpg)\n{bad}\n",
                   encoding="utf-8")
    res = build_one(src, REG, out_dir=tmp_path / "out", offline=True)
    assert not res.ok and any(message in e for e in res.errors)


def test_personality_quiz(tmp_path):
    c, _ = build(tmp_path, "quiz-personnalite", """
        # Qui es-tu ?
        ## Profil : Chat
        Tu dors beaucoup.
        ## Profil : Chien
        Tu joues beaucoup.
        ## Le matin ?
        - je dors → Chat
        - je cours → Chien,Chat
    """)
    assert [p["name"] for p in c["personalities"]] == ["Chat", "Chien"]
    assert c["questions"][0]["answers"][1]["personality"] == "Chien, Chat"
    assert c["titleScreen"]["image"] == {} and c["questions"][0]["image"] == {}   # the player reads image.file


def test_personality_quiz_unknown_profile(tmp_path):
    src = tmp_path / "q.md"
    src.write_text("---\ntype: quiz-personnalite\ntitle: T\n---\n## Profil : A\nx\n## Profil : B\ny\n"
                   "## Q ?\n- a → A\n- c → C\n", encoding="utf-8")
    res = build_one(src, REG, out_dir=tmp_path / "out", offline=True)
    assert not res.ok and any("profil « C » inconnu" in e for e in res.errors)


def test_bingo_words(tmp_path):
    c, res = build(tmp_path, "bingo", """
        Coche les mots.
        - nuage
        - pluie
    """)
    assert c["mode"] == "words" and c["words"] == "nuage\npluie"
    assert any("se répéteront" in w for w in res.warnings)
