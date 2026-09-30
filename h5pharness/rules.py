"""Content-type rules that semantics.json cannot express (the H5P editor or runtime enforces them).

FIXUPS complete the built params the way the type's editor widget would (positions, links, ids…);
RULES report what would silently break at runtime.
"""
import hashlib
import io
import math
import re
import uuid

from .markdown import html_to_text

RULES = {}
FIXUPS = {}
DEPRECATED = {
    "H5P.TwitterUserFeed": "type obsolète : X (Twitter) a fermé l'intégration des fils, le contenu n'affichera "
                           "qu'un message d'obsolescence (en anglais)",
}
SPEECH_LOCALES = {"fr": "fr-FR", "en": "en-US", "de": "de-DE", "es": "es-ES", "it": "it-IT", "pt": "pt-PT",
                  "nl": "nl-NL", "ca": "ca-ES", "sv": "sv-SE", "nb": "nb-NO", "da": "da-DK", "fi": "fi-FI",
                  "pl": "pl-PL", "ru": "ru-RU", "ar": "ar-SA", "zh": "zh-CN", "ja": "ja-JP", "ko": "ko-KR"}
LANG_DEFAULTS = {("H5P.SpeakTheWords", "inputLanguage"): SPEECH_LOCALES}   # follow the document language


def lang_default(machine, field, lang):
    table = LANG_DEFAULTS.get((machine, field.get("name")))
    if not table or not lang:
        return None
    value = table.get(lang) or table.get(str(lang).split("-")[0])
    return value if value in {o.get("value") for o in field.get("options", [])} else None

# Values applied under the author's own values (the content type misbehaves without them).
PATCH_DEFAULTS = {
    "H5P.MarkTheLetters": {"solution": ""},            # letter.js crashes on an absent solution
    "H5P.Timeline": {"timeline": {"language": "fr"}},  # TimelineJS interface language
}


PREPARE = {}   # machine -> fn(raw author values, ctx, path) -> raw values, before the build


def prepare(machine):
    def deco(fn):
        PREPARE[machine] = fn
        return fn
    return deco


def prepare_raw(machine, raw, ctx, path):
    fn = PREPARE.get(machine)
    return fn(raw, ctx, path) if fn and isinstance(raw, dict) else raw


def rule(machine):
    def deco(fn):
        RULES[machine] = fn
        return fn
    return deco


def check(machine, params, ctx, path):
    if machine in DEPRECATED:
        ctx.warn(path, DEPRECATED[machine])
    fix = FIXUPS.get(machine)
    if fix and isinstance(params, dict):
        fix(params, ctx, path)
    fn = RULES.get(machine)
    if fn and isinstance(params, dict):
        fn(params, ctx, path)


def fixup(machine):
    def deco(fn):
        FIXUPS[machine] = fn
        return fn
    return deco


PALETTE = ["#1f77b4", "#ff7f0e", "#2ca02c", "#d62728", "#9467bd", "#8c564b", "#e377c2", "#7f7f7f", "#bcbd22", "#17becf"]


@fixup("H5P.Chart")
def _chart_palette(p, ctx, path):
    """The semantics default colour is black for every item: give a readable palette instead."""
    for i, item in enumerate(p.get("listOfTypes") or []):
        if isinstance(item, dict) and item.get("color") in (None, "#000", "#000000"):
            item["color"] = PALETTE[i % len(PALETTE)]


@rule("H5P.MultiChoice")
def _multichoice(p, ctx, path):
    answers = p.get("answers") or []
    correct = sum(1 for a in answers if isinstance(a, dict) and a.get("correct"))
    if answers and correct == 0:
        ctx.error(path + ["answers"], "aucune réponse correcte")
    if (p.get("behaviour") or {}).get("type") == "single" and correct > 1:
        ctx.error(path + ["behaviour", "type"], "type « single » mais plusieurs réponses correctes")
    if len(answers) < 2:
        ctx.warn(path + ["answers"], "une seule réponse proposée")


@rule("H5P.SingleChoiceSet")
def _singlechoiceset(p, ctx, path):
    for i, c in enumerate(p.get("choices") or []):
        if len((c or {}).get("answers") or []) < 2:
            ctx.error(path + ["choices", i, "answers"], "au moins 2 réponses (la 1re est la bonne)")


@rule("H5P.Summary")
def _summary(p, ctx, path):
    for i, s in enumerate(p.get("summaries") or []):
        if len((s or {}).get("summary") or []) < 2:
            ctx.error(path + ["summaries", i, "summary"], "au moins 2 affirmations (la 1re est la bonne)")


@rule("H5P.Crossword")
def _crossword(p, ctx, path):
    words = [w for w in (p.get("words") or []) if isinstance(w, dict) and w.get("answer")]
    for i, w in enumerate(words):
        ans = html_to_text(w["answer"])
        if not re.fullmatch(r"[^\W\d_]+(?:[ '-][^\W\d_]+)*", ans):
            ctx.error(path + ["words", i, "answer"], f"« {ans} »: lettres uniquement (espaces tolérés)")
    letters = [set(html_to_text(w["answer"]).upper()) - {" ", "-", "'"} for w in words]
    for i, w in enumerate(words):
        if not w.get("fixWord") and not any(letters[i] & letters[j] for j in range(len(words)) if j != i):
            ctx.error(path + ["words", i, "answer"],
                      f"« {html_to_text(w['answer'])} » ne partage aucune lettre avec les autres mots "
                      "(la grille ne pourra pas se construire)")


@rule("H5P.QuestionSet")
def _questionset(p, ctx, path):
    if p.get("poolSize") and p["poolSize"] > len(p.get("questions") or []):
        ctx.error(path + ["poolSize"], "plus grand que le nombre de questions")


@rule("H5P.DragQuestion")
def _dragquestion(p, ctx, path):
    task = (p.get("question") or {}).get("task") or {}
    elements = task.get("elements") or []
    zones = task.get("dropZones") or []
    for zi, z in enumerate(zones):
        for ref in (z or {}).get("correctElements") or []:
            if not str(ref).isdigit() or int(ref) >= len(elements):
                ctx.error(path + ["question", "task", "dropZones", zi, "correctElements"],
                          f"élément n°{ref} inexistant (indices à partir de 0, {len(elements)} élément(s))")
    for ei, e in enumerate(elements):
        for ref in (e or {}).get("dropZones") or []:
            if not str(ref).isdigit() or int(ref) >= len(zones):
                ctx.error(path + ["question", "task", "elements", ei, "dropZones"],
                          f"zone n°{ref} inexistante (indices à partir de 0, {len(zones)} zone(s))")


@rule("H5P.FindTheWords")
def _findthewords(p, ctx, path):
    words = p.get("wordList")
    if isinstance(words, str):
        items = [w.strip() for w in words.split(",") if w.strip()]
        if not items:
            ctx.error(path + ["wordList"], "liste de mots vide (mots séparés par des virgules)")
        for w in items:
            if not re.fullmatch(r"[^\W\d_]+", w):
                ctx.error(path + ["wordList"], f"« {w} »: lettres uniquement, sans espace")


@rule("H5P.ImageHotspots")
def _imagehotspots(p, ctx, path):
    for i, h in enumerate(p.get("hotspots") or []):
        pos = (h or {}).get("position") or {}
        for axis in ("x", "y"):
            v = pos.get(axis)
            if isinstance(v, (int, float)) and not 0 <= v <= 100:
                ctx.error(path + ["hotspots", i, "position", axis], f"{v} : position en % de l'image (0 à 100)")


@rule("H5P.ImageHotspotQuestion")
def _findhotspot(p, ctx, path):
    settings = (p.get("imageHotspotQuestion") or {}).get("hotspotSettings") or {}
    for i, h in enumerate(settings.get("hotspot") or []):
        cs = (h or {}).get("computedSettings") or {}
        where = path + ["imageHotspotQuestion", "hotspotSettings", "hotspot", i, "computedSettings"]
        if cs.get("figure") not in (None, "rectangle", "circle"):
            ctx.error(where + ["figure"], f"« {cs.get('figure')} » : rectangle ou circle")
        for k in ("x", "y", "width", "height"):
            v = cs.get(k)
            if isinstance(v, (int, float)) and not 0 <= v <= 100:
                ctx.error(where + [k], f"{v} : en % de l'image (0 à 100)")


@rule("H5P.ThreeDModel")
def _threedmodel(p, ctx, path):
    def walk(v, where):
        if isinstance(v, dict):
            annotation = "text" in v and ("surface" in v or "id" in v or where[-2:-1] == ["annotations"])
            if annotation and not v.get("surface"):
                ctx.warn(where, "annotation sans « surface » : elle ne sera pas affichée par le modèle 3D")
            for k, x in v.items():
                walk(x, where + [k])
        elif isinstance(v, list):
            for i, x in enumerate(v):
                walk(x, where + [i])
    walk(p, path)


@rule("H5P.Collage")
def _collage(p, ctx, path):
    col = p.get("collage") or {}
    template = str(col.get("template") or "")
    if re.fullmatch(r"\d+(-\d+)*", template):
        needed = sum(int(x) for x in template.split("-"))
        have = len(col.get("clips") or [])
        if have != needed:
            ctx.warn(path + ["collage", "clips"],
                     f"la mise en page « {template} » attend {needed} image(s), {have} fournie(s)")


@rule("H5P.MarkTheLetters")
def _markletters(p, ctx, path):
    text = html_to_text(p.get("textField") or "")
    if re.search(r"[^\x00-\x7f]", text):
        ctx.warn(path + ["textField"],
                 "lettres accentuées ou non latines : ce type ne garde que a-z (elles disparaîtront)")


# --------------------------------------------------------------------------------------------------
# what the editor widgets would have filled in


def _machine(sub):
    return str((sub or {}).get("library", "")).split(" ")[0] if isinstance(sub, dict) else ""


@fixup("H5P.BranchingScenario")
def _scenario_links(p, ctx, path):
    """Each content goes on to the next one unless told otherwise (the last one to the end screen)."""
    bs = p.get("branchingScenario") or {}
    content = bs.get("content") or []
    n = len(content)
    for i, item in enumerate(content):
        if not isinstance(item, dict):
            continue
        where = path + ["branchingScenario", "content", i]
        if _machine(item.get("type")) == "H5P.BranchingQuestion":
            alts = ((item["type"].get("params") or {}).get("branchingQuestion") or {}).get("alternatives") or []
            for j, a in enumerate(alts):
                target = (a or {}).get("nextContentId")
                if isinstance(target, (int, float)) and not -1 <= target < n:
                    ctx.error(where + ["type", "branchingQuestion", "alternatives", j, "nextContentId"],
                              f"nœud {target} inexistant (0 à {n - 1}, ou -1 pour l'écran de fin)")
            if alts and all((a or {}).get("nextContentId", -1) == -1 for a in alts):
                ctx.warn(where, "toutes les réponses mènent à la fin du scénario (nextContentId absent ou -1)")
            continue
        if "nextContentId" not in item:
            item["nextContentId"] = i + 1 if i + 1 < n else -1
        elif not -1 <= item["nextContentId"] < n:
            ctx.error(where + ["nextContentId"],
                      f"nœud {item['nextContentId']} inexistant (0 à {n - 1}, ou -1 pour l'écran de fin)")
    for es in bs.get("endScreens") or []:
        if isinstance(es, dict):
            es.setdefault("contentId", -1)


def _map_ratio(gm):
    img = ((gm.get("mapOptions") or {}).get("backgroundSettings") or {}).get("backgroundImage") or {}
    if img.get("width") and img.get("height"):
        return img["width"] / img["height"]
    return 16 / 9


def _stage_positions(n, ratio):
    """Stages along a winding path (rows walked alternately left-right, right-left), in % of the map."""
    w = 4.375                      # size given by the GameMap editor to a new stage
    h = w * ratio
    cols = min(n, 5)
    rows = math.ceil(n / cols)
    band = 80 / rows
    out = []
    for k in range(n):
        r, c = divmod(k, cols)
        if r % 2:
            c = cols - 1 - c
        x = 8 + c * (84 - w) / max(cols - 1, 1)
        wave = (band * 0.18) * (1 if c % 2 else -1) if cols > 1 else 0
        y = min(max(10 + r * band + band / 2 - h / 2 + wave, 1), 99 - h)
        out.append({"x": f"{x:.2f}", "y": f"{y:.2f}", "width": f"{w:.3f}", "height": f"{h:.3f}"})
    return out


@fixup("H5P.GameMap")
def _gamemap(p, ctx, path):
    """ids, stage types, positions, neighbours and paths: what the map editor stores for each stage."""
    from .engine import NAMESPACE
    for gi, gm in enumerate(p.get("gamemaps") or []):
        if not isinstance(gm, dict):
            continue
        where = path + ["gamemaps", gi]
        els = [e for e in gm.get("elements") or [] if isinstance(e, dict)]
        n = len(els)
        for i, e in enumerate(els):
            e.setdefault("id", str(uuid.uuid5(NAMESPACE, f"{ctx.seed}:gamemap:{gi}:{i}")))
            e["type"] = "special-stage" if e.get("specialStageType") else "stage"
        seen = {}
        for i, e in enumerate(els):
            if e["id"] in seen:
                ctx.error(where + ["elements", i, "id"],
                          f"identifiant « {e['id']} » déjà utilisé (étape {seen[e['id']]})")
            seen.setdefault(e["id"], i)
        if not any(e.get("neighbors") for e in els):   # default: a linear path through the stages
            for i, e in enumerate(els):
                e["neighbors"] = [str(j) for j in (i - 1, i + 1) if 0 <= j < n]
        else:
            for i, e in enumerate(els):
                kept = []
                for t in e.get("neighbors") or []:
                    if not str(t).isdigit() or int(t) >= n or int(t) == i:
                        ctx.error(where + ["elements", i, "neighbors"],
                                  f"voisine « {t} » : indice d'une autre étape (0 à {n - 1}, 0 = première étape)")
                    else:
                        kept.append(str(int(t)))
                e["neighbors"] = kept
            for i, e in enumerate(els):        # the editor keeps neighbourhood symmetric
                for t in e["neighbors"]:
                    other = els[int(t)]
                    if str(i) not in other["neighbors"]:
                        other["neighbors"].append(str(i))
        for e in els:
            e["neighbors"] = sorted(set(e.get("neighbors") or []), key=int)
        if els and not any((e.get("stageBehaviour") or {}).get("canBeStartStage") for e in els):
            first = next((e for e in els if not e.get("specialStageType")), els[0])
            first.setdefault("stageBehaviour", {})["canBeStartStage"] = True
        missing = [i for i, e in enumerate(els) if not (e.get("telemetry") or {}).get("x")]
        if missing:
            spots = _stage_positions(n, _map_ratio(gm))
            for i in missing:
                e = els[i]
                e["telemetry"] = {**spots[i], **{k: v for k, v in (e.get("telemetry") or {}).items() if v}}
        # paths are stored from the neighbourhood; a path item without from/to crashes the player
        default = {"visualsType": "global"}
        custom = {}
        for q in gm.get("paths") or []:
            if not isinstance(q, dict):
                continue
            if "from" in q and "to" in q:
                custom[(int(q["from"]), int(q["to"]))] = q
            else:
                default = {k: v for k, v in q.items() if k not in ("from", "to")} or default
        paths, done = [], set()
        for i, e in enumerate(els):
            for t in e["neighbors"]:
                j = int(t)
                if (i, j) in done or (j, i) in done:
                    continue
                done.add((i, j))
                q = custom.get((i, j)) or custom.get((j, i)) or default
                paths.append({**q, "from": i, "to": j})
        extra = set(custom) - done - {(j, i) for i, j in done}
        for a, b in sorted(extra):
            ctx.error(where + ["paths"], f"chemin {a}→{b} entre deux étapes non voisines (voir neighbors)")
        if paths:
            gm["paths"] = paths
        else:
            gm.pop("paths", None)


@fixup("H5P.CoursePresentation")
def _slides_layout(p, ctx, path):
    """Slides written in YAML without positions get the automatic layout of the Markdown shortcut."""
    from .sugar.presentation import MEDIA, arrange
    for si, slide in enumerate((p.get("presentation") or {}).get("slides") or []):
        els = [e for e in (slide or {}).get("elements") or [] if isinstance(e, dict)]
        unplaced = [e for e in els if "x" not in e or "y" not in e]
        if not unplaced:
            continue
        where = path + ["presentation", "slides", si, "elements"]
        if len(unplaced) < len(els):
            ctx.error(where, "positions partielles : donner x, y (en %) à tous les éléments de la diapo, "
                             "ou à aucun (placement automatique)")
            continue
        texts = [e for e in els if _machine(e.get("action")) == "H5P.AdvancedText"]
        media = [e for e in els if _machine(e.get("action")) in MEDIA]
        others = [e for e in els if e not in texts and e not in media]
        ratios = []
        for e in media:
            f = (e["action"].get("params") or {}).get("file") or {}
            ratios.append(f["height"] / f["width"] if f.get("width") and f.get("height") else 9 / 16)
        geo = arrange(None, [html_to_text((e["action"].get("params") or {}).get("text", "")) for e in texts],
                      ratios, len(others), lambda msg, si=si: ctx.warn(where, f"diapo {si} : {msg}"))
        for e, box in zip(texts + media, geo["texts"] + geo["media"]):
            e.update(zip(("x", "y", "width", "height"), (round(v, 2) for v in box)))
        for i, (e, (box, as_button)) in enumerate(zip(others, geo["interactions"])):
            e.update(zip(("x", "y", "width", "height"), (round(v, 2) for v in box)))
            if as_button:
                e.setdefault("displayAsButton", True)
                e.setdefault("buttonSize", "big")
                e.setdefault("title", ((e.get("action") or {}).get("metadata") or {}).get("title")
                             or f"Question {i + 1}")


@prepare("H5P.DragQuestion")
def _dragdrop_labels(raw, ctx, path):
    """Automatic layout (nothing positioned): zones are anonymous columns unless their label shows."""
    q = raw.get("question")
    task = q.get("task") if isinstance(q, dict) else None
    if not isinstance(task, dict) or not isinstance(task.get("dropZones"), list):
        return raw
    elements = task.get("elements") if isinstance(task.get("elements"), list) else []
    items = [x for x in task["dropZones"] + elements if isinstance(x, dict)]
    if items and not any("x" in x or "y" in x for x in items):
        for z in task["dropZones"]:
            if isinstance(z, dict):
                z.setdefault("showLabel", True)
    return raw


@fixup("H5P.DragQuestion")
def _dragdrop_layout(p, ctx, path):
    """Drag and drop written in YAML without positions: automatic layout (items on top, zones below)."""
    from .sugar.dragdrop import WIDTH_PX, _text_width, geometry
    q = p.get("question") or {}
    task = q.get("task") or {}
    els = [e for e in task.get("elements") or [] if isinstance(e, dict)]
    zones = [z for z in task.get("dropZones") or [] if isinstance(z, dict)]
    unplaced = [e for e in els + zones if "x" not in e or "y" not in e]
    if not unplaced:
        return
    where = path + ["question", "task"]
    if len(unplaced) < len(els) + len(zones):
        ctx.error(where, "positions partielles : donner x, y (en %) et width, height (en em) à tous les "
                         "éléments et zones, ou à aucun (placement automatique)")
        return
    if (q.get("settings") or {}).get("background"):
        ctx.error(where, "avec une image de fond, placer chaque zone et élément : x, y en % ; width, height en em")
        return
    statics = [e for e in els if not e.get("dropZones")]
    items = [e for e in els if e.get("dropZones")]
    sizes = []
    for e in items:
        if _machine(e.get("type")) == "H5P.AdvancedText":
            sizes.append((_text_width(html_to_text((e["type"].get("params") or {}).get("text", ""))), 2.25))
        else:
            sizes.append((5.0, 5.0))
    position = {id(e): k for k, e in enumerate(items)}           # element index -> index among the items
    members = [[position[id(els[int(i)])] for i in z.get("correctElements") or []
                if str(i).isdigit() and int(i) < len(els) and id(els[int(i)]) in position] for z in zones]
    geo = geometry([html_to_text(((e.get("type") or {}).get("params") or {}).get("text", "")) for e in statics],
                   sizes, members, False, [])
    for e, box in zip(statics + items, geo["statics"] + geo["items"]):
        e.update(box)
    for z, box in zip(zones, geo["zones"]):
        z.update(box)
    q.setdefault("settings", {})["size"] = {"width": WIDTH_PX, "height": geo["height"]}


@fixup("H5P.InteractiveVideo")
def _video_positions(p, ctx, path):
    from .sugar.video import BUTTON_BOX, POSTER_BOX
    for it in ((p.get("interactiveVideo") or {}).get("assets") or {}).get("interactions") or []:
        if isinstance(it, dict) and ("x" not in it or "y" not in it):
            for k, v in (POSTER_BOX if it.get("displayType") == "poster" else BUTTON_BOX).items():
                it.setdefault(k, v)


def ar_pattern(data):
    """ARToolKit pattern of a marker image, computed like H5PEditor.ARMarkerGenerator (AR.js studio):
    16×16 image on white, 4 orientations (0, -90, -180, -270°), channels B, G, R."""
    from PIL import Image
    img = Image.open(io.BytesIO(data)).convert("RGBA")
    base = Image.new("RGBA", img.size, (255, 255, 255, 255))
    base.alpha_composite(img)
    small = base.convert("RGB").resize((16, 16), Image.BILINEAR)
    blocks = []
    for turn in range(4):
        px = small.rotate(90 * turn).load()   # canvas rotate(-90°·turn) = 90°·turn counter-clockwise
        lines = []
        for channel in (2, 1, 0):
            for y in range(16):
                lines.append(" ".join(f"{px[x, y][channel]:>3}" for x in range(16)))
        blocks.append("\n".join(lines) + "\n")
    return "\n".join(blocks)


@fixup("H5P.ARScavenger")
def _ar_markers(p, ctx, path):
    """The player ignores a marker without its pattern file, which only the H5P editor generates."""
    for i, m in enumerate(p.get("markers") or []):
        if not isinstance(m, dict) or m.get("markerPattern"):
            continue
        image = (m.get("markerImage") or {}).get("path")
        data = ctx.media.files.get(image) if image else None
        if not data:
            ctx.error(path + ["markers", i, "markerImage"], "image du marqueur requise (le motif est calculé à partir "
                                                            "d'elle ; une image différente par marqueur)")
            continue
        try:
            pattern = ar_pattern(data).encode()
        except Exception as e:  # unreadable image: reported by the media ingestion already
            ctx.error(path + ["markers", i, "markerImage"], f"motif impossible à calculer ({e})")
            continue
        name = f"files/pattern-{hashlib.sha256(pattern).hexdigest()[:12]}.txt"
        ctx.media.files[name] = pattern
        m["markerPattern"] = {"path": name, "mime": "text/plain"}


@fixup("H5P.InfoWall")
def _infowall_titles(p, ctx, path):
    for i, panel in enumerate((p.get("infoWall") or {}).get("panels") or []):
        if isinstance(panel, dict) and not panel.get("panelTitle"):
            first = next((html_to_text(v) for v in panel.get("entries") or [] if html_to_text(str(v))), "")
            panel["panelTitle"] = first[:60] or f"Panneau {i + 1}"


@rule("H5P.IFrameEmbed")
def _iframe(p, ctx, path):
    for k in ("width", "height"):
        v = str(p.get(k) or "")
        if v and not re.fullmatch(r"\d+(\.\d+)?px", v.strip()):
            ctx.error(path + [k], f"« {v} » : en pixels (ex. 800px) ; H5P en déduit le rapport hauteur/largeur, "
                                  "un % ou une autre unité déforme le cadre")


@rule("H5P.ARScavenger")
def _ar_distinct(p, ctx, path):
    seen = {}
    for i, m in enumerate(p.get("markers") or []):
        pat = ((m or {}).get("markerPattern") or {}).get("path")
        if pat and pat in seen:
            ctx.error(path + ["markers", i, "markerImage"], f"même image que le marqueur {seen[pat]} : "
                                                            "la caméra ne pourrait pas les distinguer")
        seen.setdefault(pat, i)
