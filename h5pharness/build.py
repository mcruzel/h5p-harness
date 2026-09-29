"""Build one Markdown source into a .h5p package (no network except media downloads)."""
import difflib
import time
from dataclasses import dataclass, field
from pathlib import Path

import yaml

from . import document, markers, package  # noqa: F401  (markers registers text hooks)
from .engine import Ctx, build_content, deep_merge
from .library import PKG, ROOT, Registry, UnknownLibrary
from .media import Media

SOURCES = ROOT / "sources"
DIST = ROOT / "dist"
TARGET_CORE_API = (1, 28)   # Moodle 4.5 / 5.x ship h5plib_v128


@dataclass
class Result:
    source: Path
    ok: bool = False
    out: Path = None
    errors: list = field(default_factory=list)
    warnings: list = field(default_factory=list)
    touched: set = field(default_factory=set)
    size: int = 0
    ms: int = 0
    title: str = ""
    machine: str = ""


_PRESETS = None


def presets():
    global _PRESETS
    if _PRESETS is None:
        _PRESETS = yaml.safe_load((PKG / "presets.yaml").read_text(encoding="utf-8")) or {}
    return _PRESETS


def output_path(src: Path, out_dir: Path):
    src = src.resolve()
    try:
        rel = src.relative_to(SOURCES.resolve())
    except ValueError:
        rel = Path(src.name)
    return out_dir / rel.with_suffix(".h5p")


def seed_for(src: Path):
    try:
        return src.resolve().relative_to(ROOT).as_posix()
    except ValueError:
        return src.name


def build_one(src: Path, registry: Registry, out_dir: Path = DIST, full=True, offline=False, write=True):
    t0 = time.perf_counter()
    res = Result(source=src)
    try:
        doc = document.load(src)
    except document.DocumentError as e:
        res.errors = e.messages
        return res
    except OSError as e:
        res.errors = [f"lecture impossible: {e}"]
        return res
    meta = doc.meta
    res.title = str(meta.get("title", ""))
    try:
        lib = registry.resolve(meta["type"])
    except UnknownLibrary:
        hint = difflib.get_close_matches(str(meta["type"]).lower(), list(registry.aliases), 3, 0.5)
        res.errors = [f"en-tête: type « {meta['type']} » inconnu" + (f" (proches: {', '.join(hint)})" if hint else
                                                                     " (liste: python -m h5pharness types)")]
        return res
    res.machine = lib.machine
    if not lib.runnable:
        res.errors = [f"en-tête: {lib.machine} n'est pas autonome; l'insérer dans une colonne, un livre, "
                      "une présentation…"]
        return res
    preset = {}
    if meta.get("preset"):
        preset = presets().get(str(meta["preset"]))
        if preset is None:
            res.errors = [f"en-tête: preset « {meta['preset']} » inconnu ({', '.join(presets())})"]
            return res
    media = Media(src.resolve().parent, offline=offline)
    ctx = Ctx(registry=registry, lang=str(meta.get("language", "fr")), media=media, seed=seed_for(src),
              preset=dict(preset or {}))
    raw = {}
    if doc.has_sugar:
        from .sugar import parse_sugar
        raw = parse_sugar(lib.machine, doc.body, ctx, [], line_offset=doc.body_line)
    for _line, block in doc.yaml_blocks:
        raw = deep_merge(raw, block)
    params = build_content(lib, raw, ctx)
    used = [lib] + sorted(ctx.used - {lib}, key=lambda l: l.folder)
    runtime, embedded, missing = package.libraries_for(registry, used, full=full)
    for m in sorted(missing):
        ctx.errors.append(f"bibliothèque {m} absente de vendor/libraries (python tools/vendor_libraries.py)")
    for l in (embedded or runtime):
        api = l.meta.get("coreApi")
        if api and (int(api["majorVersion"]), int(api["minorVersion"])) > TARGET_CORE_API:
            ctx.errors.append(f"{l.uber} exige l'API H5P {api['majorVersion']}.{api['minorVersion']} "
                              f"(cible: {TARGET_CORE_API[0]}.{TARGET_CORE_API[1]})")
    res.warnings = ctx.warnings
    if ctx.errors:
        res.errors = ctx.errors
        return res
    try:
        h5p = package.h5p_json(meta, lib, runtime)
    except ValueError as e:
        res.errors = [str(e)]
        return res
    res.touched = {src.resolve()} | media.touched
    if write:
        out = output_path(src, out_dir)
        package.write(out, h5p, params, media.files, embedded)
        installed = None if full else {l.uber for l in runtime}
        problems = package.check_archive(out, installed=installed)
        if problems:
            res.errors = [f"paquet: {p}" for p in problems[:10]]
            return res
        media.save_lock()
        res.touched |= media.touched
        res.out = out
        res.size = out.stat().st_size
    res.ok = True
    res.ms = int((time.perf_counter() - t0) * 1000)
    return res
