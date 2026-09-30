"""Deposit into a real local Moodle: only when H5P_MOODLE_TEST_COURSE names a disposable course
(and H5P_MOODLE_DIR the Moodle folder), e.g. H5P_MOODLE_TEST_COURSE=tous-types python -m pytest tests/test_moodle.py"""
import os
from pathlib import Path

import pytest

from h5pharness.build import build_one
from h5pharness.library import Registry
from h5pharness.moodle import deploy

COURSE = os.environ.get("H5P_MOODLE_TEST_COURSE")
pytestmark = pytest.mark.skipif(not COURSE, reason="pas de Moodle de test (H5P_MOODLE_TEST_COURSE)")
EXAMPLE = Path(__file__).parents[1] / "sources" / "exemples" / "vf.md"


def test_activity_then_page_are_created_then_updated(tmp_path):
    res = build_one(EXAMPLE, Registry(), out_dir=tmp_path, offline=True)
    assert res.ok
    for as_ in ("activity", "page"):
        first = deploy(res.out, key="tests/moodle-vf.md", name="Test du harnais", course=COURSE, as_=as_)
        again = deploy(res.out, key="tests/moodle-vf.md", name="Test du harnais", course=COURSE, as_=as_)
        assert again["cmid"] == first["cmid"] and again["action"] == "updated"
        assert again["url"].endswith(f"id={first['cmid']}")
