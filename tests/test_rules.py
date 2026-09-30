"""What the H5P editor widgets would have filled in, and the traps H5P does not report."""
import json
import textwrap
import zipfile

from h5pharness.build import build_one
from h5pharness.document import load_yaml
from h5pharness.engine import Ctx, fmt, sub_id
from h5pharness.library import Registry

REG = Registry()


def build(tmp_path, type_, body, ok=True):
    src = tmp_path / "doc.md"
    src.write_text(f"---\ntype: {type_}\ntitle: Test\n---\n```yaml\n{textwrap.dedent(body).strip()}\n```\n",
                   encoding="utf-8")
    res = build_one(src, REG, out_dir=tmp_path / "out", offline=True)
    if not ok:
        assert not res.ok
        return None, res
    assert res.ok, "\n".join(res.errors)
    with zipfile.ZipFile(res.out) as z:
        return json.loads(z.read("content/content.json")), res


def test_yaml_keeps_what_the_author_wrote():
    data = load_yaml("code: 0472\nt: 1:20\nlang: no\nn: 12\nf: 1.5\nb: true\nz: 007")
    assert data == {"code": "0472", "t": "1:20", "lang": "no", "n": 12, "f": 1.5, "b": True, "z": "007"}


def test_padlock_code_with_leading_zero(tmp_path):
    c, _ = build(tmp_path, "cadenas", """
        introduction: Trouve le code.
        solution: 0472
        alphabet: 0123456789
    """)
    assert c["solution"] == "0472"


def test_game_map_filled_like_the_editor(tmp_path):
    c, _ = build(tmp_path, "carte-jeu", """
        gamemaps:
          - elements:
              - label: A
                contentsList: [{contentType: {library: texte, text: a}}]
              - label: B
                contentsList: [{contentType: {library: texte, text: b}}]
              - label: Bonus
                specialStageType: extra-life
    """)
    els = c["gamemaps"][0]["elements"]
    assert [e["type"] for e in els] == ["stage", "stage", "special-stage"]
    assert "specialStageType" not in els[0] and "specialStageLinkURL" not in els[0]
    assert "specialStageExtraLives" in els[2] and "specialStageLinkURL" not in els[2]
    assert [e["neighbors"] for e in els] == [["1"], ["0", "2"], ["1"]]
    assert len({e["id"] for e in els}) == 3
    assert all(set(e["telemetry"]) == {"x", "y", "width", "height"} for e in els)
    assert els[0]["stageBehaviour"]["canBeStartStage"] is True
    assert [(p["from"], p["to"]) for p in c["gamemaps"][0]["paths"]] == [(0, 1), (1, 2)]


def test_game_map_neighbours_made_symmetric_and_checked(tmp_path):
    c, _ = build(tmp_path, "carte-jeu", """
        gamemaps:
          - elements:
              - {label: A, neighbors: ["2"], contentsList: [{contentType: {library: texte, text: a}}]}
              - {label: B, contentsList: [{contentType: {library: texte, text: b}}]}
              - {label: C, contentsList: [{contentType: {library: texte, text: c}}]}
    """)
    els = c["gamemaps"][0]["elements"]
    assert els[2]["neighbors"] == ["0"] and els[1]["neighbors"] == []
    _, res = build(tmp_path, "carte-jeu", """
        gamemaps:
          - elements:
              - {label: A, neighbors: ["5"], contentsList: [{contentType: {library: texte, text: a}}]}
    """, ok=False)
    assert any("gamemaps[0].elements[0].neighbors" in e for e in res.errors)


def test_scenario_goes_on_to_the_next_node(tmp_path):
    c, _ = build(tmp_path, "scenario", """
        branchingScenario:
          title: T
          content:
            - type: {library: texte, text: A}
            - type: {library: texte, text: B}
    """)
    bs = c["branchingScenario"]
    assert [x["nextContentId"] for x in bs["content"]] == [1, -1]
    assert all(e["contentId"] == -1 for e in bs["endScreens"])


def test_slides_without_positions_are_laid_out(tmp_path):
    c, _ = build(tmp_path, "presentation", """
        presentation:
          slides:
            - elements:
                - action: {library: texte, text: Du texte}
                - action: {library: image, file: /tests/media/paysage.jpg, alt: Paysage}
                - action: {library: vf, md: "Vrai ?\\n- [x] Vrai\\n- [ ] Faux"}
    """)
    els = c["presentation"]["slides"][0]["elements"]
    assert all({"x", "y", "width", "height"} <= set(e) for e in els)
    text, image, question = els
    assert text["x"] + text["width"] <= image["x"]            # text on the left, image on the right
    assert question["y"] >= text["y"] + text["height"]        # question underneath


def test_slides_with_partial_positions_are_refused(tmp_path):
    _, res = build(tmp_path, "presentation", """
        presentation:
          slides:
            - elements:
                - {x: 10, y: 10, action: {library: texte, text: A}}
                - action: {library: texte, text: B}
    """, ok=False)
    assert any("positions partielles" in e for e in res.errors)


def test_drag_and_drop_without_positions(tmp_path):
    c, _ = build(tmp_path, "glisser-deposer", """
        question:
          task:
            elements:
              - {type: {library: texte, text: chat}, dropZones: [0]}
              - {type: {library: texte, text: moineau}, dropZones: [1]}
            dropZones:
              - {label: Mammifères, correctElements: [0]}
              - {label: Oiseaux, correctElements: [1]}
    """)
    task = c["question"]["task"]
    assert all({"x", "y", "width", "height"} <= set(x) for x in task["elements"] + task["dropZones"])
    assert all(z["showLabel"] for z in task["dropZones"])
    assert task["dropZones"][0]["y"] > task["elements"][0]["y"]


def test_interactive_video_positions_and_times(tmp_path):
    c, _ = build(tmp_path, "video-interactive", """
        transcript: /tests/media/etats-eau.vtt
        interactiveVideo:
          video: {files: [/tests/media/clip.webm]}
          assets:
            interactions:
              - duration: {from: "0:01", to: "0:03"}
                displayType: poster
                action: {library: vf, md: "Vrai ?\\n- [x] Vrai\\n- [ ] Faux"}
    """)
    it = c["interactiveVideo"]["assets"]["interactions"][0]
    assert it["duration"] == {"from": 1, "to": 3}
    assert (it["x"], it["y"], it["width"], it["height"]) == (12.5, 8, 30, 19)


def test_ar_marker_pattern_generated(tmp_path):
    c, res = build(tmp_path, "chasse-ar", """
        markers:
          - markerImage: /tests/media/triangle-vert.png
            interaction:
              interaction: {library: vf, md: "Vrai ?\\n- [x] Vrai\\n- [ ] Faux"}
    """)
    pattern = c["markers"][0]["markerPattern"]
    assert pattern["mime"] == "text/plain"
    with zipfile.ZipFile(res.out) as z:
        text = z.read("content/" + pattern["path"]).decode()
    assert text.count("\n") == 195 and len(text.split()) == 4 * 3 * 16 * 16


def test_iframe_size_in_pixels(tmp_path):
    _, res = build(tmp_path, "iframe", """
        source: https://example.org
        width: 100%
        minWidth: 300px
        height: 500px
    """, ok=False)
    assert any(e.startswith("width:") for e in res.errors)


def test_speech_language_follows_the_document(tmp_path):
    c, _ = build(tmp_path, "dire-mots", """
        question: Dis bonjour.
        acceptedAnswers: [bonjour]
    """)
    assert c["inputLanguage"] == "fr-FR"


def test_info_wall_panel_titles(tmp_path):
    c, _ = build(tmp_path, "mur-infos", """
        infoWall:
          propertiesGroup:
            properties: [{label: Nom}]
          panels:
            - entries: [Mercure]
    """)
    assert c["infoWall"]["panels"][0]["panelTitle"] == "Mercure"


def test_transcript_chapter_marks_completed(tmp_path):
    c, _ = build(tmp_path, "transcription", """
        mediumGroup:
          medium: {library: video, md: "![Clip](/tests/media/clip.webm)"}
        transcriptFiles:
          - {transcriptFile: /tests/media/transcription.vtt, label: Français}
        chapters:
          chapterMarks: |
            0:00 Début
            1:05.5 Suite
    """)
    assert c["chapters"]["chapterMarks"] == "00:00:00 Début\n00:01:05.5 Suite"


def test_locations_are_zero_based_but_ids_stable():
    assert fmt(["a", 0, "b"]) == "a[0].b"
    ctx = Ctx(REG, "fr", None, "seed")
    # same id as the builds made before locations became 0-based (seed "seed:questions[1]")
    assert sub_id(ctx, ["questions", 0]) == "dea2abaa-b0e4-5f86-95d8-877bbcbef3b0"


def test_video_interactions_need_a_transcript(tmp_path):
    _, res = build(tmp_path, "video-interactive", """
        interactiveVideo:
          video: {files: [/tests/media/clip.webm]}
          assets:
            interactions:
              - duration: {from: 1, to: 2}
                action: {library: vf, md: "La glace est solide.\\n- [x] Vrai\\n- [ ] Faux"}
    """, ok=False)
    assert any("transcrit horodaté" in e for e in res.errors)


def test_video_without_interactions_invites_to_get_the_transcript(tmp_path):
    c, res = build(tmp_path, "video-interactive", """
        interactiveVideo:
          video: {files: [/tests/media/clip.webm]}
    """)
    assert any("transcrit" in h for h in res.hints)


def test_video_checked_against_its_transcript(tmp_path):
    c, res = build(tmp_path, "video-interactive", """
        transcript: /tests/media/etats-eau.vtt
        interactiveVideo:
          video: {files: [/tests/media/clip.webm]}
          assets:
            interactions:
              - duration: {from: 2, to: 3}
                action: {library: vf, md: "La glace est de l'eau solide.\\n- [x] Vrai\\n- [ ] Faux"}
              - duration: {from: 2, to: 3}
                action: {library: vf, md: "Paris est la capitale de la France.\\n- [x] Vrai\\n- [ ] Faux"}
    """)
    track = c["interactiveVideo"]["video"]["textTracks"]["videoTrack"][0]
    assert track["srcLang"] == "fr" and track["track"]["mime"] == "text/vtt"
    assert len([w for w in res.warnings if "sans mot commun" in w]) == 1
    _, res = build(tmp_path, "video-interactive", """
        transcript: /tests/media/etats-eau.vtt
        interactiveVideo:
          video: {files: [/tests/media/clip.webm]}
          assets:
            interactions:
              - duration: {from: 60, to: 70}
                action: {library: texte-simple, text: Trop tard}
    """, ok=False)
    assert any("après la fin du transcrit" in e for e in res.errors)


def test_transcript_formats():
    from h5pharness.transcript import compact, parse
    srt = "1\n00:00:01,500 --> 00:00:03,000\n<i>Bonjour</i> à tous\n\n2\n00:01:02,000 --> 00:01:04,000\nSuite\n"
    cues = parse(srt)
    assert [(c.start, c.text) for c in cues] == [(1.5, "Bonjour à tous"), (62.0, "Suite")]
    assert compact(cues) == ["0:01 Bonjour à tous", "1:02 Suite"]


def test_moodle_target_merges_front_matter_and_options():
    import pytest
    from h5pharness.moodle import MoodleError, target
    t = target({"moodle": {"course": "svt5", "section": 2, "as": "page"}}, {"course": "", "section": None})
    assert (t["course"], t["section"], t["as"]) == ("svt5", 2, "page")
    t = target({}, {"course": "12", "as": "activité", "section": 3})
    assert (t["course"], t["as"], t["section"]) == ("12", "activity", 3)
    assert target({}, {"course": "12", "page": "Cours 1"})["as"] == "page"      # adding to a page
    with pytest.raises(MoodleError):
        target({}, {"course": ""})
