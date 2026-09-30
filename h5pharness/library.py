"""Vendored H5P libraries: lookup by alias/name/version, localisation, dependency closure."""
import copy
import json
import re
from functools import cached_property
from pathlib import Path

import yaml

PKG = Path(__file__).resolve().parent
ROOT = PKG.parent
LIBRARIES = ROOT / "vendor" / "libraries"
L10N = PKG / "l10n"


def _special(kind):
    return {"widget": "showWhen", "showWhen": {"rules": [{"field": "specialStageType", "equals": kind}],
                                               "nullWhenHidden": True}}


# What the H5P editor enforces differently from semantics.json (custom widgets decide what is shown/required).
FIELD_PATCHES = {
    "H5P.GameMap": {
        # a stage is "special" as soon as specialStageType has a value (its exercises are then ignored)
        "specialStageType": {"optional": True},
        "specialStageExtraLives": _special("extra-life"),
        "specialStageExtraTime": _special("extra-time"),
        "specialStageLinkURL": _special("link"),
        "specialStageLinkTarget": _special("link"),
        "specialStageTeleportTarget": _special("teleport"),
        "neighbors": {"optional": True},        # default: a linear path (see rules.py)
    },
    "H5P.InfoWall": {"panelTitle": {"optional": True}},  # editor-only list title, never displayed
    # images are optional (their alt text is checked in rules.py when an image is given)
    "H5P.PersonalityQuiz": {"alt": {"optional": True}},
}


def kebab(machine: str) -> str:
    name = machine.split(".", 1)[-1]
    return re.sub(r"(?<=[a-z0-9])(?=[A-Z])|(?<=[A-Z])(?=[A-Z][a-z])", "-", name).lower()


class Library:
    def __init__(self, path: Path):
        self.path = path
        self.meta = json.loads((path / "library.json").read_text(encoding="utf-8"))
        self.machine = self.meta["machineName"]
        self.major = int(self.meta["majorVersion"])
        self.minor = int(self.meta["minorVersion"])
        self.patch = int(self.meta.get("patchVersion", 0))
        self._localized = {}

    def __repr__(self):
        return f"<{self.uber}>"

    @property
    def uber(self):
        return f"{self.machine} {self.major}.{self.minor}"

    @property
    def folder(self):
        return f"{self.machine}-{self.major}.{self.minor}"

    @property
    def version(self):
        return (self.major, self.minor, self.patch)

    @property
    def title(self):
        return self.meta.get("title", self.machine)

    @property
    def runnable(self):
        return bool(int(self.meta.get("runnable", 0) or 0))

    @cached_property
    def semantics(self):
        f = self.path / "semantics.json"
        return json.loads(f.read_text(encoding="utf-8")) if f.exists() else []

    def language(self, lang):
        f = self.path / "language" / f"{lang}.json"
        if not f.exists():
            return None
        try:
            return json.loads(f.read_text(encoding="utf-8")).get("semantics")
        except json.JSONDecodeError:
            return None

    def deps(self, kinds=("preloadedDependencies",)):
        for kind in kinds:
            for d in self.meta.get(kind, []) or []:
                yield d["machineName"], int(d["majorVersion"]), int(d["minorVersion"])

    def localized_semantics(self, lang, labels=True):
        """semantics.json with defaults (and labels) taken from language/<lang>.json + harness overrides.

        labels=False keeps the English labels/descriptions of semantics.json: upstream translations are
        sometimes stale (a label translated for another field), which misleads a reader of the specs.
        """
        key = (lang, labels)
        if key not in self._localized:
            sem = copy.deepcopy(self.semantics)
            _patch(sem, FIELD_PATCHES.get(self.machine, {}))
            tr = self.language(lang)
            if tr:
                _overlay(sem, tr, labels)
            overrides = load_overrides(lang).get(self.machine, {})
            if overrides:
                _apply_overrides(sem, overrides)
            self._localized[key] = sem
        return self._localized[key]


def _patch(fields, patches):
    if not patches:
        return
    for f in fields:
        if isinstance(f, dict):
            f.update(patches.get(f.get("name"), {}))
            if f.get("type") == "group":
                _patch(f.get("fields", []), patches)
            elif f.get("type") == "list" and isinstance(f.get("field"), dict):
                _patch([f["field"]], patches)


def _overlay(fields, tr_fields, labels=True):
    """language/xx.json mirrors semantics.json by position: copy translated defaults (and labels)."""
    if not isinstance(tr_fields, list):
        return
    for f, t in zip(fields, tr_fields):
        if not isinstance(t, dict) or not isinstance(f, dict):
            continue
        for k in ("label", "description", "entity", "placeholder") if labels else ("entity",):
            if k in t and isinstance(t[k], str) and "\ufffd" not in t[k]:
                f[k] = t[k]
        if "default" in t and _same_kind(f, t["default"]):
            f["default"] = t["default"]
        if labels and "options" in t and isinstance(t["options"], list) and isinstance(f.get("options"), list):
            for fo, to in zip(f["options"], t["options"]):
                if isinstance(fo, dict) and isinstance(to, dict) and "label" in to:
                    fo["label"] = to["label"]
        if f.get("type") == "group" and "fields" in t:
            _overlay(f.get("fields", []), t["fields"], labels)
        if f.get("type") == "list" and isinstance(t.get("field"), dict):
            _overlay([f["field"]], [t["field"]], labels)


def _same_kind(field, value):
    """A translated default must have the field's type (stale language files exist upstream)."""
    t = field.get("type")
    if t in ("text", "select"):
        return isinstance(value, str) or (t == "select" and isinstance(value, (int, float, bool)))
    if t == "boolean":
        return isinstance(value, bool)
    if t == "number":
        return isinstance(value, (int, float)) and not isinstance(value, bool)
    return isinstance(value, (dict, list))


def _apply_overrides(fields, overrides, prefix=""):
    for f in fields:
        path = f"{prefix}{f.get('name')}"
        if path in overrides:
            f["default"] = overrides[path]
        if f.get("type") == "group":
            _apply_overrides(f.get("fields", []), overrides, path + ".")
        elif f.get("type") == "list":
            _apply_overrides([f["field"]], overrides, path + ".")


_OVERRIDES = {}


def load_overrides(lang):
    if lang not in _OVERRIDES:
        f = L10N / f"{lang}.json"
        _OVERRIDES[lang] = json.loads(f.read_text(encoding="utf-8")) if f.exists() else {}
    return _OVERRIDES[lang]


class UnknownLibrary(KeyError):
    pass


class Registry:
    def __init__(self, root: Path = LIBRARIES):
        self.root = root
        self.by_folder = {}
        self.by_machine = {}
        if root.exists():
            for d in sorted(root.iterdir()):
                if (d / "library.json").exists():
                    lib = Library(d)
                    self.by_folder[lib.folder] = lib
                    self.by_machine.setdefault(lib.machine, []).append(lib)
        for libs in self.by_machine.values():
            libs.sort(key=lambda l: l.version, reverse=True)
        self.aliases = self._load_aliases()

    def _load_aliases(self):
        table, self.curated = {}, {}
        for machine in self.by_machine:
            for key in (machine, machine.lower(), kebab(machine), kebab(machine).replace("-", "")):
                table.setdefault(key.lower(), machine)
        data = yaml.safe_load((Path(__file__).parent / "aliases.yaml").read_text(encoding="utf-8")) or {}
        for machine, names in data.items():
            self.curated[machine] = [str(n).lower() for n in names or []]
            for n in self.curated[machine]:
                table[n] = machine
        return table

    def aliases_of(self, machine):
        """Curated French aliases first (aliases.yaml order), then automatic ones."""
        curated = self.curated.get(machine, [])
        auto = sorted({a for a, m in self.aliases.items() if m == machine and not a.startswith("h5p.")} - set(curated),
                      key=lambda a: (len(a), a))
        return curated + auto

    def get(self, machine, major=None, minor=None):
        libs = self.by_machine.get(machine, [])
        for lib in libs:
            if major is None or (lib.major, lib.minor) == (major, minor):
                return lib
        return None

    def machine_of(self, name: str):
        """Friendly name, machine name or 'Machine x.y' -> (machine, major, minor)."""
        name = str(name).strip()
        m = re.match(r"^([\w.-]+?)(?:[ @-](\d+)\.(\d+))?$", name)
        if not m:
            raise UnknownLibrary(name)
        base, major, minor = m.group(1), m.group(2), m.group(3)
        machine = self.aliases.get(base.lower())
        if machine is None:
            raise UnknownLibrary(name)
        return machine, (int(major) if major else None), (int(minor) if minor else None)

    def resolve(self, name, allowed=None):
        """Pick the library for `name`; `allowed` = semantics options ('Machine x.y') restricting versions."""
        machine, major, minor = self.machine_of(name)
        if allowed is not None:
            candidates = []
            for opt in allowed:
                om, ov = opt.split(" ")
                if om == machine:
                    oma, omi = (int(x) for x in ov.split("."))
                    if major is None or (oma, omi) == (major, minor):
                        lib = self.get(om, oma, omi)
                        if lib:
                            candidates.append(lib)
            if not candidates:
                raise UnknownLibrary(name)
            return max(candidates, key=lambda l: l.version)
        lib = self.get(machine, major, minor)
        if lib is None:
            raise UnknownLibrary(name)
        return lib

    def runnable_types(self):
        return [libs[0] for m, libs in sorted(self.by_machine.items()) if libs[0].runnable]

    def closure(self, roots, kinds=("preloadedDependencies", "dynamicDependencies")):
        """Libraries needed by `roots` (Library objects), dependencies first; plus missing 'M x.y'."""
        order, missing, seen = [], set(), set()

        def visit(lib):
            if lib.folder in seen:
                return
            seen.add(lib.folder)
            for m, ma, mi in lib.deps(kinds):
                dep = self.get(m, ma, mi)
                if dep is None:
                    missing.add(f"{m} {ma}.{mi}")
                else:
                    visit(dep)
            order.append(lib)

        for r in roots:
            visit(r)
        return order, missing
