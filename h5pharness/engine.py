"""Semantics-driven engine: author values (YAML / md sugar) -> content.json params.

Everything that is invariant comes from the libraries themselves (semantics.json, language files)
plus the harness' translation overrides and pedagogical presets. The engine fills defaults,
converts Markdown to the HTML each field accepts, ingests media, generates sub-content ids and
reports every problem the platform would otherwise silently "fix" (H5P filters, never rejects).
"""
import difflib
import re
import uuid
from dataclasses import dataclass, field as dfield

from . import markdown
from .library import Library, Registry, UnknownLibrary
from .media import Media, MediaError

MISSING = object()
NAMESPACE = uuid.UUID("6c1f5f4e-0b8a-4d0e-9a57-5b3c2a1d7e10")
RESERVED = {"library", "params", "metadata", "subContentId", "md"}
MEDIA_NAMES = {"image": "image", "audio": "fichier audio", "video": "vidéo", "file": "fichier"}
REQUIRED_MEDIA = {("H5P.Image", "file"), ("H5P.Video", "sources"), ("H5P.Audio", "files"), ("H5P.MemoryGame", "image"),
                  ("H5P.ImageHotspots", "image"), ("H5P.ImageHotspotQuestion", "backgroundImage"),
                  ("H5P.ImageJuxtaposition", "image"), ("H5P.ThreeImage", "scenesrc"), ("H5P.Dictation", "sample")}


@dataclass
class Ctx:
    registry: Registry
    lang: str
    media: Media
    seed: str
    preset: dict = dfield(default_factory=dict)
    errors: list = dfield(default_factory=list)
    warnings: list = dfield(default_factory=list)
    stack: list = dfield(default_factory=list)   # library machine names (innermost last)
    used: set = dfield(default_factory=set)      # Library objects used by the content
    quiet: bool = False                          # probing defaults: do not report

    def error(self, path, msg):
        if not self.quiet:
            self.errors.append(f"{fmt(path)}: {msg}" if path else msg)

    def warn(self, path, msg):
        if not self.quiet:
            line = f"{fmt(path)}: {msg}" if path else msg
            if line not in self.warnings:
                self.warnings.append(line)


def fmt(path):
    out = ""
    for seg in path:
        if isinstance(seg, int):
            out += f"[{seg + 1}]"
        else:
            out += ("." if out else "") + seg
    return out


def is_flat_group(field):
    return field.get("type") == "group" and len(field.get("fields", [])) == 1 and not field.get("isSubContent")


# --------------------------------------------------------------------------------------------------
# entry point

def build_content(lib: Library, values, ctx: Ctx):
    ctx.used.add(lib)
    ctx.stack.append(lib.machine)
    try:
        fields = lib.localized_semantics(ctx.lang)
        params = build_group({"type": "group", "fields": fields}, values, ctx, [], top=True)
        from .rules import check
        check(lib.machine, params, ctx, [])
        return params
    finally:
        ctx.stack.pop()


def build_field(field, value, ctx, path, siblings, hidden=False):
    t = field.get("type")
    if value is None:
        value = MISSING
    handler = HANDLERS.get(t)
    if handler is None:
        ctx.error(path, f"type de champ H5P inconnu: {t}")
        return MISSING
    return handler(field, value, ctx, path, siblings, hidden)


# --------------------------------------------------------------------------------------------------
# groups and lists

def build_group(field, value, ctx, path, siblings=None, hidden=False, top=False):
    fields = field.get("fields", [])
    if not top and is_flat_group(field):
        child = fields[0]
        # accept both the H5P flattened form and {child_name: value}
        if isinstance(value, dict) and set(value) == {child["name"]} and not (
                child.get("type") == "group" and child["name"] in {f["name"] for f in child.get("fields", [])}):
            value = value[child["name"]]
        return build_field(child, value, ctx, path, siblings or {}, hidden)
    if value is MISSING:
        value = {}
        if field.get("optional"):
            hidden = True  # optional group left out by the author: defaults only, nothing is required inside
    if not isinstance(value, dict):
        ctx.error(path, f"objet attendu (clés possibles: {', '.join(f['name'] for f in fields)})")
        value = {}
    known = {f["name"]: f for f in fields}
    for k in value:
        if k not in known and not (field.get("isSubContent") and k == "subContentId"):
            hint = difflib.get_close_matches(str(k), list(known), 1, 0.6)
            ctx.error(path + [str(k)], "champ inconnu" + (f" (vouliez-vous « {hint[0]} » ?)" if hint else
                                                          f" (possibles: {', '.join(list(known)[:12])})"))
    out = {}
    for f in fields:
        name = f["name"]
        v = value.get(name, MISSING)
        visible = is_visible(f, out, value, ctx)
        if not visible and f.get("showWhen", {}).get("nullWhenHidden"):
            continue
        r = build_field(f, v, ctx, path + [name], out, hidden=hidden or not visible)
        if r is not MISSING:
            out[name] = r
    if field.get("isSubContent"):
        out["subContentId"] = sub_id(ctx, path)
    return out


def build_list(field, value, ctx, path, siblings, hidden):
    item = field["field"]
    label = field.get("entity") or item.get("label") or "élément"
    if value is MISSING:
        # same rule as H5PEditor.List: defaultNum, else min, else 1 item
        n = field.get("defaultNum", field.get("min", 1))
        n = int(n or 0)
        if n == 0:
            return MISSING  # H5P drops empty lists anyway
        probe = Ctx(ctx.registry, ctx.lang, ctx.media, ctx.seed, ctx.preset, quiet=True, stack=list(ctx.stack))
        items = [build_field(item, MISSING, probe, path + [i], {}) for i in range(n)]
        if not probe.errors and all(x is not MISSING for x in items):
            return items
        if not (field.get("optional") or hidden or int(field.get("min", 0) or 0) == 0):
            ctx.error(path, f"au moins {field.get('min', 1)} {label}(s) requis")
        return MISSING
    if not isinstance(value, list):
        value = [value]
    if "min" in field and len(value) < int(field["min"]) and not hidden:
        ctx.error(path, f"au moins {field['min']} {label}(s) requis, {len(value)} fourni(s)")
    if "max" in field and len(value) > int(field["max"]):
        ctx.error(path, f"au plus {field['max']} {label}(s), {len(value)} fourni(s)")
    out = []
    for i, v in enumerate(value):
        r = build_field(item, v, ctx, path + [i], {}, hidden)
        if r is not MISSING:
            out.append(r)
    return out or MISSING


# --------------------------------------------------------------------------------------------------
# visibility (H5PEditor.ShowWhen)

def is_visible(field, out, raw, ctx):
    rules_cfg = field.get("showWhen")
    if field.get("widget") != "showWhen" or not isinstance(rules_cfg, dict):
        return True
    rules = rules_cfg.get("rules", [])
    if not rules:
        return True
    results = []
    for rule in rules:
        name = str(rule.get("field", "")).split("/")[-1]
        current = out.get(name, raw.get(name, MISSING))
        if isinstance(current, dict) and "library" in current:
            current = current["library"]
        expected = rule.get("equals")
        expected = expected if isinstance(expected, list) else [expected]
        if current is MISSING:
            results.append(False)
        else:
            results.append(any(_same(current, e) for e in expected))
    return all(results) if rules_cfg.get("type") == "and" else any(results)


def _same(a, b):
    if isinstance(a, str) and isinstance(b, str) and " " in b and " " in a:
        return a.split(" ")[0] == b.split(" ")[0]  # library name, any version
    return a == b


# --------------------------------------------------------------------------------------------------
# scalars

def default_or_missing(field, ctx, path, hidden, kind):
    name = field.get("name")
    if name in ctx.preset and _compatible(field, ctx.preset[name]):
        return ctx.preset[name]
    if "default" in field:
        # a null default means "no value": omit it (H5P would turn it into "")
        return MISSING if field["default"] is None else field["default"]
    if kind == "boolean":
        return False
    if not field.get("optional") and not hidden and field.get("widget") != "none":
        ctx.error(path, "champ requis manquant")
    return MISSING


def _compatible(field, value):
    t = field.get("type")
    return (t == "boolean" and isinstance(value, bool)) or (t == "number" and isinstance(value, (int, float))) \
        or (t in ("text", "select") and isinstance(value, str))


TEXT_HOOKS = {}   # (machine, field name) -> callable(text, field, ctx, path) -> html


def build_text(field, value, ctx, path, siblings, hidden):
    if value is MISSING:
        return default_or_missing(field, ctx, path, hidden, "text")
    if isinstance(value, bool) or not isinstance(value, (str, int, float)):
        ctx.error(path, "texte attendu")
        return MISSING
    text = str(value)
    hook = TEXT_HOOKS.get((ctx.stack[-1] if ctx.stack else None, field.get("name")))
    if hook:
        text = hook(text, field, ctx, path)
        if text is MISSING:
            return MISSING
    elif markdown.is_html_field(field):
        html, errors, warnings = markdown.to_html(text, field)
        for e in errors:
            ctx.error(path, e)
        for w in warnings:
            ctx.warn(path, w)
        text = html
    else:
        text = text.strip() if "\n" not in text.strip() else text.strip("\n")
    if not text.strip() and not field.get("optional") and "default" not in field and not hidden:
        ctx.error(path, "texte vide")
    if "maxLength" in field and len(text) > int(field["maxLength"]):
        ctx.error(path, f"{len(text)} caractères, maximum {field['maxLength']}")
    rx = field.get("regexp")
    if isinstance(rx, dict) and rx.get("pattern") and text:
        flags = re.I if "i" in rx.get("modifiers", "") else 0
        try:
            if not re.search(rx["pattern"], text, flags):
                ctx.error(path, f"format invalide (motif {rx['pattern']})")
        except re.error:
            pass
    return text


def build_number(field, value, ctx, path, siblings, hidden):
    if value is MISSING:
        return default_or_missing(field, ctx, path, hidden, "number")
    if isinstance(value, str):
        try:
            value = float(value.replace(",", ".")) if re.search(r"[.,]", value) else int(value)
        except ValueError:
            ctx.error(path, f"nombre attendu, reçu « {value} »")
            return MISSING
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        ctx.error(path, "nombre attendu")
        return MISSING
    if "min" in field and value < float(field["min"]):
        ctx.error(path, f"{value} < minimum {field['min']}")
    if "max" in field and value > float(field["max"]):
        ctx.error(path, f"{value} > maximum {field['max']}")
    if isinstance(value, float):
        if field.get("decimals") is not None:
            value = round(value, int(field["decimals"]))
        if value == int(value) and not field.get("decimals"):
            value = int(value)
    return value


def build_boolean(field, value, ctx, path, siblings, hidden):
    if value is MISSING:
        return default_or_missing(field, ctx, path, hidden, "boolean")
    if isinstance(value, str) and value.strip().lower() in ("true", "vrai", "oui", "yes", "1", "false", "faux",
                                                            "non", "no", "0"):
        return value.strip().lower() in ("true", "vrai", "oui", "yes", "1")
    if not isinstance(value, bool):
        ctx.error(path, "booléen attendu (true/false)")
        return MISSING
    return value


def build_select(field, value, ctx, path, siblings, hidden):
    if value is MISSING:
        return default_or_missing(field, ctx, path, hidden, "select")
    options = field.get("options", [])
    if not options:  # dynamic options filled by the editor at runtime (e.g. drop zone indexes)
        vals = value if isinstance(value, list) else [value]
        vals = [str(v) if isinstance(v, (int, float)) and not isinstance(v, bool) else v for v in vals]
        return vals if field.get("multiple") else vals[0]
    by_value = {str(o.get("value")): o.get("value") for o in options}
    by_label = {str(o.get("label", "")).strip().lower(): o.get("value") for o in options}

    def one(v):
        if str(v) in by_value:
            return by_value[str(v)]
        if isinstance(v, bool) and str(v).lower() in by_value:
            return by_value[str(v).lower()]
        if str(v).strip().lower() in by_label:
            return by_label[str(v).strip().lower()]
        ctx.error(path, f"valeur « {v} » hors liste ({', '.join(map(str, by_value))})")
        return MISSING

    if field.get("multiple"):
        vals = value if isinstance(value, list) else [value]
        res = [one(v) for v in vals]
        return [r for r in res if r is not MISSING]
    return one(value)


# --------------------------------------------------------------------------------------------------
# media

def build_media(field, value, ctx, path, siblings, hidden):
    kind = field["type"]
    if value is MISSING:
        # the H5P editor never enforces media fields; only the content types that break without them do
        if (ctx.stack[-1] if ctx.stack else None, field.get("name")) in REQUIRED_MEDIA and not hidden:
            ctx.error(path, f"{MEDIA_NAMES[kind]} requis")
        return MISSING
    many = kind in ("audio", "video")
    items = value if isinstance(value, list) else [value]
    out = []
    for i, it in enumerate(items):
        try:
            out.append(ctx.media.ingest(it, kind))
        except MediaError as e:
            ctx.error(path + ([i] if len(items) > 1 else []), str(e))
    if not out:
        return MISSING
    if many:
        return out
    if len(out) > 1:
        ctx.error(path, "une seule image/fichier attendu")
    return out[0]


# --------------------------------------------------------------------------------------------------
# sub-content

def sub_id(ctx, path):
    return str(uuid.uuid5(NAMESPACE, f"{ctx.seed}:{fmt(path)}"))


def build_library(field, value, ctx, path, siblings, hidden):
    if value is MISSING and isinstance(field.get("default"), dict) and field["default"].get("library"):
        # semantics default sub-content (e.g. the summary of an interactive video): built like the editor
        # does, with nothing required inside since the author did not ask for it
        value, hidden = dict(field["default"]), True
    if value is MISSING:
        if not field.get("optional") and not hidden:
            ctx.error(path, "sous-contenu requis (clé library)")
        return MISSING
    if isinstance(value, str):
        value = {"library": value}
    if not isinstance(value, dict):
        ctx.error(path, "sous-contenu attendu: objet avec « library: <type> »")
        return MISSING
    options = [o if isinstance(o, str) else o.get("name") for o in field.get("options", [])]
    reserved = set(RESERVED)
    name = value.get("library")
    if not name and isinstance(value.get("type"), str):  # tolerated synonym, unless the type has a 'type' field
        name = value["type"]
        reserved.add("type")
    if not name:
        ctx.error(path, f"clé « library » manquante (choix: {choices(ctx.registry, options)})")
        return MISSING
    try:
        lib = ctx.registry.resolve(name, allowed=options)
    except UnknownLibrary:
        ctx.error(path, f"« {name} » non accepté ici (choix: {choices(ctx.registry, options)})")
        return MISSING
    if "type" in reserved and any(f.get("name") == "type" for f in lib.semantics):
        ctx.error(path, "utiliser « library: » (ce type a lui-même un champ « type »)")
        return MISSING
    raw = value.get("params") if isinstance(value.get("params"), dict) else {
        k: v for k, v in value.items() if k not in reserved}
    if "md" in value:
        from .sugar import parse_sugar
        sugar = parse_sugar(lib.machine, str(value["md"]), ctx, path)
        raw = deep_merge(sugar, raw)
    ctx.used.add(lib)
    ctx.stack.append(lib.machine)
    try:
        params = build_group({"type": "group", "fields": lib.localized_semantics(ctx.lang)}, raw, ctx,
                             path, top=True, hidden=hidden)
        if not hidden:
            from .rules import check
            check(lib.machine, params, ctx, path)
    finally:
        ctx.stack.pop()
    meta = value.get("metadata") if isinstance(value.get("metadata"), dict) else {}
    title = meta.get("title") or value.get("title") or auto_title(params) or lib.title
    metadata = {"contentType": lib.title, "license": "U", "title": title[:255]}
    for k in ("license", "licenseVersion", "authors", "source", "yearFrom", "yearTo", "authorComments"):
        if k in meta:
            metadata[k] = meta[k]
    return {"library": lib.uber, "params": params, "subContentId": sub_id(ctx, path), "metadata": metadata}


def choices(registry, options):
    names = []
    for o in options:
        machine = o.split(" ")[0]
        aliases = registry.aliases_of(machine)
        names.append(aliases[0] if aliases else machine)
    return ", ".join(dict.fromkeys(names))


TITLE_KEYS = ("question", "text", "title", "taskDescription", "introduction", "statement", "headline", "label")


def auto_title(params):
    for key in TITLE_KEYS:
        v = params.get(key) if isinstance(params, dict) else None
        if isinstance(v, str) and v.strip():
            t = markdown.html_to_text(v)
            if t:
                return t[:80] + ("…" if len(t) > 80 else "")
    return None


def deep_merge(base, extra):
    if not isinstance(base, dict) or not isinstance(extra, dict):
        return extra
    out = dict(base)
    for k, v in extra.items():
        out[k] = deep_merge(out[k], v) if k in out else v
    return out


HANDLERS = {
    "group": lambda f, v, c, p, s, h: build_group(f, v, c, p, s, h),
    "list": build_list,
    "text": build_text,
    "number": build_number,
    "boolean": build_boolean,
    "select": build_select,
    "library": build_library,
    "image": build_media,
    "audio": build_media,
    "video": build_media,
    "file": build_media,
}
