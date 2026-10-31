"""Mesure de la hauteur des glisser-déposer (tools/dnd_measure.py, tools/measure_dnd.mjs, tools/qa.py --render).

Le plan de dépôt, les lignes de sortie et le seuil se testent sans navigateur ; la mesure elle-même joue un exemple
dans Chromium : elle est ignorée si node, unzip, playwright, h5p-standalone ou Chromium manquent (docs/INTEGRATION.md).
"""
import json
import shutil
import sys
import zipfile

import pytest

from h5pharness.build import build_one
from h5pharness.library import ROOT, Registry

sys.path.insert(0, str(ROOT / "tools"))
import dnd_measure as dm  # noqa: E402
import qa  # noqa: E402


def _content(elements, zones):
    return {"question": {"task": {"elements": elements, "dropZones": zones}}}


def _text(*zones):
    return {"type": {"library": "H5P.AdvancedText 1.1"}, "dropZones": [], "multiple": False}


def _label(*zones, multiple=False):
    return {"type": {"library": "H5P.AdvancedText 1.1"}, "dropZones": [str(z) for z in zones], "multiple": multiple}


def _zone(*correct):
    return {"correctElements": [str(c) for c in correct]}


def test_plans_follow_the_correct_answers_and_skip_decoration():
    # 0 = consigne (décor) ; 1, 2 = étiquettes de la zone 0 ; 3 = étiquette de la zone 1 ; 4 = distracteur
    c = _content([_text(), _label(0, 1), _label(0, 1), _label(0, 1), _label(0, 1)], [_zone(1, 2), _zone(3)])
    p = dm.plans(c)
    assert p["juste"] == [(0, 0), (1, 0), (2, 1)]  # rang = ordre parmi les étiquettes déplaçables (sans le décor)
    assert p["faux"] == [(0, 1), (1, 1), (2, 0), (3, 1)]  # tout faux ; le distracteur va dans sa première zone


def test_plans_drop_a_multiple_label_once_per_correct_zone_and_a_plain_one_once():
    multiple = _content([_label(0, 1), _label(0, 1)], [_zone(0, 1), _zone(0, 1)])
    assert dm.plans(multiple)["juste"] == [(0, 0), (1, 0)]  # étiquettes simples : une seule zone
    multiple["question"]["task"]["elements"][0]["multiple"] = True
    assert dm.plans(multiple)["juste"] == [(0, 0), (0, 1), (1, 0)]


def test_plans_have_no_wrong_drop_for_a_label_with_a_single_possible_zone():
    c = _content([_label(0), _label(0, 1)], [_zone(0, 1), _zone()])
    assert dm.plans(c) == {"juste": [(0, 0), (1, 0)], "faux": [(1, 1)]}


def test_only_drag_questions_are_measured(tmp_path):
    other = tmp_path / "x.h5p"
    with zipfile.ZipFile(other, "w") as z:
        z.writestr("h5p.json", json.dumps({"mainLibrary": "H5P.MultiChoice"}))
        z.writestr("content/content.json", "{}")
    assert dm.content_of(other) is None
    assert dm.measure(other, {}) is None
    assert dm.content_of(tmp_path / "absent.h5p") is None


def _run(width, plan, before, after, deposes=3, attendus=3, verifie=True, erreur=None):
    return {"largeur": width, "plan": plan, "attendus": attendus, "deposes": deposes, "verifie": verifie,
            "erreur": erreur, "avant": {"iframe": before, "doc": before},
            "apres": None if after is None else {"iframe": after, "doc": after}}


def test_summary_is_short_and_numeric():
    m = {"initError": None, "runs": [_run(400, "juste", 905, 1180), _run(400, "faux", 905, 1342),
                                     _run(760, "juste", 731, 891), _run(760, "faux", 731, 1020)]}
    assert dm.summary(m) == ["400 px : avant 905 · juste 1180 (+275) · tout faux 1342 (+437)",
                             "760 px : avant 731 · juste 891 (+160) · tout faux 1020 (+289)"]
    assert dm.worst(m) == 1342
    assert dm.summary(None) == [] and dm.worst(None) is None and dm.problems(None) == []


def test_threshold_and_untrustworthy_measures_are_reported():
    ok = {"initError": None, "runs": [_run(760, "juste", 731, 891), _run(760, "faux", 731, 1020)]}
    assert dm.problems(ok) == []  # aucun seuil par défaut : la mesure est rendue, rien n'échoue
    assert dm.problems(ok, 1020) == []
    assert dm.problems(ok, 1000) == ["760 px, tout faux : 1020 px après « Vérifier », au-delà de 1000 px"]
    bad = {"initError": None, "runs": [_run(400, "juste", 905, None, verifie=False),
                                       _run(400, "faux", 905, 950, deposes=1),
                                       _run(760, "juste", 731, None, erreur="Timeout")]}
    assert dm.problems(bad) == ["400 px, juste : pas de bouton « Vérifier »",
                                "400 px, tout faux : 1 étiquette(s) déposée(s) sur 3, mesure incomplète",
                                "760 px, juste : Timeout"]
    assert dm.problems({"initError": "mesure impossible : x", "runs": []}) == ["mesure impossible : x"]


def _browser_modules():
    """node_modules du rendu s'il est installé (playwright et h5p-standalone) ; sinon on saute, sans réseau ni npm."""
    mods = qa.RENDER / "node_modules"
    for tool in ("node", "unzip"):
        if not shutil.which(tool):
            pytest.skip(tool + " absent")
    if not ((mods / "h5p-standalone").exists() and (mods / "playwright").exists()):
        pytest.skip(f"playwright ou h5p-standalone absents de {mods} (lancer une fois tools/qa.py --render)")
    return mods


def test_measure_plays_a_drag_and_drop_in_chromium(tmp_path, capsys):
    _browser_modules()
    src = ROOT / "sources" / "exemples" / "glisser-deposer.md"
    res = build_one(src, Registry(), out_dir=tmp_path, offline=True)
    assert res.ok, "\n".join(res.errors)
    m = dm.measure(res.out, qa.render_env(), (760,))
    if m["initError"] and "xecutable" in m["initError"]:
        pytest.skip("Chromium introuvable : " + m["initError"])
    assert m["initError"] is None, m["initError"]
    assert [(r["largeur"], r["plan"]) for r in m["runs"]] == [(760, "juste"), (760, "faux")]
    for r in m["runs"]:
        assert r["erreur"] is None and r["verifie"] and r["deposes"] == r["attendus"] == 5, r
        assert r["avant"]["iframe"] > 100 and r["apres"]["iframe"] >= r["avant"]["iframe"], r
    assert dm.problems(m) == []

    # le contrôle de rendu : une ligne par largeur, et le seuil fait échouer l'activité
    assert qa.main([str(res.out), "--no-php", "--render", "--largeurs", "760", "--hauteur-max", "1"]) == 1
    out = capsys.readouterr().out
    assert "hauteur 760 px : avant " in out and "tout faux" in out and "au-delà de 1 px" in out
    assert qa.main([str(res.out), "--no-php", "--render", "--no-mesure"]) == 0
    assert "hauteur" not in capsys.readouterr().out
