"""Per-type reference cards (specs/<alias>.md), generated from semantics.json + French labels.

They are what an agent reads (on demand) before writing a source file: compact, with the fields
that matter first and the invariant interface strings collapsed.
"""
import re

from .engine import REQUIRED_MEDIA
from .library import PKG, ROOT, Registry
from .markdown import allowed_tags, is_html_field
from .rules import DEPRECATED

SPECS = ROOT / "specs"
SUGAR_DOCS = PKG / "sugar_docs"
EXAMPLES = ROOT / "sources" / "exemples"     # one validated example per type
FIXTURES = ROOT / "tests" / "fixtures"      # the same activities written entirely in YAML
L10N_NAMES = {"l10n", "a11y", "UI", "texts", "i10n", "labels", "localize", "translations", "dictionary"}
KIND = {"text": "texte", "number": "nombre", "boolean": "booléen", "select": "choix", "group": "groupe",
        "list": "liste", "library": "sous-contenu", "image": "image (chemin ou URL)",
        "audio": "audio (chemin ou URL)", "video": "vidéo (URL YouTube/Vimeo, chemin ou URL)",
        "file": "fichier (chemin ou URL)"}
_POS = "x, y en % de la zone de jeu ; width, height en em (1 em = 16 px) ; sans positions nulle part : mise en " \
       "page automatique (sans image de fond)"
# fields hidden by the editor (widget "none") that an author may still give, and what the harness does
HIDDEN_DOCS = {
    "H5P.CoursePresentation": dict.fromkeys(
        ("x", "y", "width", "height"),
        "nombre, facultatif — position et taille en % de la diapo 16:9 ; aucun élément positionné sur une diapo = "
        "mise en page automatique (texte à gauche, image à droite, interactions dessous ou en boutons)"),
    "H5P.DragQuestion": dict.fromkeys(("x", "y", "width", "height"), f"nombre, facultatif — {_POS}"),
    "H5P.InteractiveVideo": dict.fromkeys(
        ("x", "y", "width", "height"),
        "nombre, facultatif — x, y en % de la vidéo ; width, height en em ; défaut : carte centrée (poster) ou "
        "bouton au centre"),
    "H5P.BranchingScenario": {
        "nextContentId": "nombre, facultatif — indice du contenu suivant dans `content` (0 = premier), -1 = écran "
                         "de fin ; défaut : le contenu suivant (-1 pour le dernier)",
        "contentId": "nombre, facultatif — laisser -1 (défaut)"},
    "H5P.GameMap": {
        "id": "texte, facultatif — identifiant unique de l'étape (généré)",
        "telemetry": "groupe facultatif — position de l'étape x, y, width, height (textes, en % de la carte) ; "
                     "défaut : étapes réparties le long d'un chemin sinueux",
        "from": "nombre — indice de l'étape de départ du chemin (0 = première)",
        "to": "nombre — indice de l'étape d'arrivée du chemin"},
}
FIELD_NOTES = {
    ("H5P.DragQuestion", "dropZones"): "indices des zones, à partir de 0",
    ("H5P.DragQuestion", "correctElements"): "indices des éléments, à partir de 0 (dans l'ordre de `elements`)",
    ("H5P.GameMap", "neighbors"): "indices des étapes voisines, à partir de 0 (voisinage rendu symétrique) ; "
                                  "absent partout : parcours linéaire dans l'ordre",
    ("H5P.GameMap", "paths"): "généré à partir de `neighbors` : ne donner (avec from/to) que pour un style de "
                              "chemin particulier",
    ("H5P.GameMap", "specialStageType"): "à omettre pour une étape normale : toute valeur en fait une étape "
                                         "spéciale dont les exercices sont ignorés",
    ("H5P.InfoWall", "panelTitle"): "non affiché (titre dans l'éditeur) ; défaut : la première entrée",
    ("H5P.SpeakTheWords", "inputLanguage"): "défaut : la langue du document (fr → fr-FR)",
    ("H5P.ARScavenger", "markerPattern"): "généré à partir de markerImage (ne pas fournir)",
    ("H5P.IFrameEmbed", "width"): "en px (ex. 800px) : H5P en déduit le rapport hauteur/largeur",
    ("H5P.IFrameEmbed", "height"): "en px (ex. 600px)",
}


def _leaves(field):
    t = field.get("type")
    if t == "group":
        for f in field.get("fields", []):
            yield from _leaves(f)
    elif t == "list":
        yield from _leaves(field["field"])
    else:
        yield field


def _is_l10n(field):
    if field.get("type") not in ("group", "text"):
        return False
    leaves = list(_leaves(field))
    if not leaves or any(l.get("type") not in ("text",) for l in leaves):
        return False
    if any("default" not in l for l in leaves):
        return False
    return field.get("common") or field.get("name") in L10N_NAMES or field.get("type") == "group"


def _is_settings(field):
    if field.get("type") != "group":
        return False
    leaves = list(_leaves(field))
    return leaves and all(l.get("type") in ("boolean", "number", "select") or
                          (l.get("type") == "text" and "default" in l) for l in leaves) and \
        all("default" in l or l.get("type") == "boolean" or l.get("optional") for l in leaves)


def _short(v, n=30):
    s = str(v).lower() if isinstance(v, bool) else str(v)
    s = re.sub(r"<[^>]+>", "", s)
    return s if len(s) <= n else s[:n - 1] + "…"


def _label(f):
    lab = (f.get("label") or "").strip()
    desc = re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", f.get("description") or "")).strip()
    out = f" — {_short(lab, 70)}" if lab else ""
    if desc and desc.lower() != lab.lower():
        out += f" ({_short(desc, 220)})"
    return out


def _describe(f, reg):
    t = f.get("type")
    bits = [KIND.get(t, t)]
    if t == "text" and is_html_field(f):
        tags = sorted(allowed_tags(f) - {"div", "span", "p", "br"})
        bits = [f"texte riche (Markdown{': ' + ' '.join(tags) if tags else ''})"]
    elif t == "text" and f.get("widget") == "textarea":
        bits = ["texte multiligne"]
    elif t == "text" and f.get("widget") == "colorSelector":
        bits = ["couleur #rrggbb"]
    elif t == "select":
        opts = [str(o.get("value")) for o in f.get("options", [])]
        more = "|…" if len(opts) > 10 else ""
        bits = [f"choix {'|'.join(opts[:10])}{more}" + (" (plusieurs)" if f.get("multiple") else "")]
    elif t == "library":
        names = []
        for o in f.get("options", []):
            m = (o if isinstance(o, str) else o.get("name", "")).split(" ")[0]
            al = reg.aliases_of(m)
            names.append(al[0] if al else m)
        bits = [f"sous-contenu, library: {' | '.join(dict.fromkeys(names))}"]
    elif t == "list":
        rng = []
        if "min" in f:
            rng.append(f"min {f['min']}")
        if "max" in f:
            rng.append(f"max {f['max']}")
        bits = [f"liste{' (' + ', '.join(rng) + ')' if rng else ''}"]
    if t == "number":
        rng = [f"{k} {f[k]}" for k in ("min", "max") if k in f]
        if rng:
            bits.append(", ".join(rng))
    if "default" in f and t not in ("group", "list") and f["default"] not in ("", None):
        bits.append(f"défaut {_short(f['default'])}")
    if f.get("widget") == "showWhen":
        conds = []
        for r in (f.get("showWhen") or {}).get("rules", []):
            eq = r.get("equals")
            eq = "|".join(str(e).split(" ")[0] for e in eq) if isinstance(eq, list) else str(eq).split(" ")[0]
            conds.append(f"{str(r.get('field', '')).split('/')[-1]} = {eq}")
        bits.append(f"si {' et '.join(conds)}" if conds else "conditionnel")
    return ", ".join(bits)


def _required(f, machine=None):
    t = f.get("type")
    if t in ("image", "audio", "video", "file"):
        return (machine, f.get("name")) in REQUIRED_MEDIA
    if t in ("group", "boolean") or f.get("optional") or "default" in f or f.get("widget") in ("none", "showWhen"):
        return False
    if t == "list":
        return int(f.get("min", 0) or 0) > 0
    return True


def _render_fields(fields, reg, depth, out, collapsed, machine=None):
    pad = "  " * depth
    for f in fields:
        name, t = f.get("name"), f.get("type")
        if f.get("widget") == "none" and name in HIDDEN_DOCS.get(machine, {}):
            doc = HIDDEN_DOCS[machine][name]
            if out and out[-1].startswith(f"{pad}- ") and out[-1].endswith(f" : {doc}"):  # x, y, width… share it
                out[-1] = out[-1][:-len(f" : {doc}")] + f", {name} : {doc}"
            else:
                out.append(f"{pad}- {name} : {doc}")
            continue
        if f.get("widget") == "none" or f.get("deprecated"):
            continue
        if _is_l10n(f):
            collapsed.append(name)
            continue
        star = "*" if _required(f, machine) else ""
        if _is_settings(f):
            items = []
            for leaf in f.get("fields", []):
                if leaf.get("type") in ("group", "list") or leaf.get("widget") == "none":
                    continue
                d = leaf.get("default", False if leaf.get("type") == "boolean" else "")
                if leaf.get("type") == "select":
                    d = f"{d} ({'|'.join(str(o.get('value')) for o in leaf.get('options', [])[:6])})"
                items.append(f"{leaf['name']}={_short(d, 40) if d != '' else '…'}")
            out.append(f"{pad}- {name} : réglages{_label(f)}")
            out.append(f"{pad}  {', '.join(items)}")
            continue
        note = FIELD_NOTES.get((machine, name))
        out.append(f"{pad}- {name}{star} : {_describe(f, reg)}{_label(f)}" + (f" — **{note}**" if note else ""))
        if t == "group":
            if len(f.get("fields", [])) == 1 and not f.get("isSubContent"):
                out[-1] += " (groupe à un champ: écrire directement la valeur)"
            _render_fields(f.get("fields", []), reg, depth + 1, out, collapsed, machine)
        elif t == "list":
            item = f["field"]
            if item.get("type") == "group":
                sub = item.get("fields", [])
                if len(sub) == 1 and not item.get("isSubContent"):
                    out.append(f"{pad}  chaque élément = {_describe(sub[0], reg)}{_label(sub[0])}")
                    if sub[0].get("type") in ("group", "list"):
                        _render_fields(sub[0].get("fields", []) if sub[0]["type"] == "group" else [sub[0]["field"]],
                                       reg, depth + 2, out, collapsed, machine)
                else:
                    out.append(f"{pad}  chaque élément :")
                    _render_fields(sub, reg, depth + 2, out, collapsed, machine)
            else:
                out.append(f"{pad}  chaque élément = {_describe(item, reg)}{_label(item)}")


_EXAMPLE_OK = {}


def example_ok(path, reg):
    """The embedded example is called 'validé': it must at least build (the CI also runs the official
    validator and the headless player on every example)."""
    if path not in _EXAMPLE_OK:
        from .build import build_one
        _EXAMPLE_OK[path] = path.exists() and build_one(path, reg, offline=True, write=False).ok
    return _EXAMPLE_OK[path]


def render_spec(reg: Registry, lib):
    aliases = reg.aliases_of(lib.machine)
    from .sugar import has_adapter
    sugar = has_adapter(lib.machine)
    lines = [f"# {lib.title} — `{aliases[0] if aliases else lib.machine}`", "",
             f"{lib.machine} {lib.major}.{lib.minor} · alias : {', '.join(aliases) or '—'} · "
             f"syntaxe Markdown simplifiée : {'oui' if sugar else 'non (bloc ```yaml)'}", ""]
    if lib.machine in DEPRECATED:
        lines += [f"> **Attention — {DEPRECATED[lib.machine]}.** À ne pas utiliser pour une nouvelle activité.", ""]
    doc = SUGAR_DOCS / f"{lib.machine}.md"
    if doc.exists():
        lines += ["## Syntaxe Markdown", "", doc.read_text(encoding="utf-8").strip(), ""]
    notes = SUGAR_DOCS / f"{lib.machine}.notes.md"
    if notes.exists():
        lines += ["## Points d'attention", "", notes.read_text(encoding="utf-8").strip(), ""]
    lines += ["## Champs (bloc ```yaml, noms H5P)", "",
              "`*` = obligatoire ; les autres champs ont une valeur par défaut ou sont facultatifs. Libellés et "
              "descriptions : ceux de la bibliothèque (anglais) ; valeurs par défaut : en français.", ""]
    out, collapsed = [], []
    _render_fields(lib.localized_semantics("fr", labels=False), reg, 0, out, collapsed, lib.machine)
    lines += out
    if collapsed:
        lines += ["", f"Textes d'interface pré-remplis en français (ne pas fournir sauf besoin) : "
                      f"{', '.join(collapsed)}."]
    name = aliases[0] if aliases else lib.machine
    example = EXAMPLES / f"{name}.md"
    if example_ok(example, reg):
        body = example.read_text(encoding="utf-8").strip()
        fence = "````" if "```" in body else "```"
        lines += ["", "## Exemple complet (validé : validateur officiel H5P + affichage)", "",
                  f"Fichier `sources/exemples/{example.name}` (médias dans `sources/exemples/media/`).", "",
                  f"{fence}markdown", body, fence]
        variant = FIXTURES / f"{name}.yaml.md"
        if example_ok(variant, reg):
            lines += ["", "Même activité entièrement en YAML (positions explicites) : "
                          f"`tests/fixtures/{variant.name}`."]
    return "\n".join(lines).rstrip() + "\n"


def write_all():
    reg = Registry()
    SPECS.mkdir(exist_ok=True)
    for old in SPECS.glob("*.md"):
        if old.name != "README.md":
            old.unlink()
    index = []
    for lib in reg.runnable_types():
        aliases = reg.aliases_of(lib.machine)
        name = aliases[0] if aliases else lib.machine
        (SPECS / f"{name}.md").write_text(render_spec(reg, lib), encoding="utf-8")
        from .sugar import has_adapter
        index.append((name, lib, has_adapter(lib.machine)))
    extra = ["H5P.AdvancedText", "H5P.Image", "H5P.Video", "H5P.Audio", "H5P.Link", "H5P.Table"]
    for m in extra:
        lib = reg.get(m)
        if lib:
            aliases = reg.aliases_of(m)
            (SPECS / f"{aliases[0] if aliases else m}.md").write_text(render_spec(reg, lib), encoding="utf-8")
    rows = [f"| `{n}` | {l.title}{' ⚠ obsolète' if l.machine in DEPRECATED else ''} | {l.machine} "
            f"{l.major}.{l.minor} | {'Markdown' if s else 'yaml'} | "
            f"{'✓' if example_ok(EXAMPLES / f'{n}.md', reg) else ''} |" for n, l, s in index]
    readme = (SPECS / "README.md")
    head = readme.read_text(encoding="utf-8").split("<!-- index -->")[0] if readme.exists() else ""
    table_head = "| type | nom | bibliothèque | syntaxe | exemple validé |\n|---|---|---|---|---|\n"
    readme.write_text(head.rstrip() + "\n\n<!-- index -->\n" + table_head + "\n".join(rows) + "\n", encoding="utf-8")
    return len(index) + len(extra)
