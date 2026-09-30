"""Sugar for Interactive Video: one video + timed interactions, bookmarks and end screens."""
import re

from . import adapter, parse_sugar
from .common import IMAGE, join, lines_of, split_headings

TIME = re.compile(r"^(?:(\d+):)?(\d{1,2}):(\d{2}(?:[.,]\d+)?)$|^(\d+(?:[.,]\d+)?)\s*s?$")
TEXT_TYPES = {"H5P.Text", "H5P.Nil", "H5P.Image", "H5P.Link", "H5P.Table"}
# x, y in % of the video; width, height in em
POSTER_BOX = {"x": 12.5, "y": 8, "width": 30, "height": 19}     # centred card the student answers directly
BUTTON_BOX = {"x": 47.8, "y": 46.1, "width": 10, "height": 10}  # button opening the content


def seconds(text):
    m = TIME.match(text.strip())
    if not m:
        return None
    if m.group(4):
        return float(m.group(4).replace(",", "."))
    h = int(m.group(1) or 0)
    return h * 3600 + int(m.group(2)) * 60 + float(m.group(3).replace(",", "."))


@adapter("H5P.Text")
def text(text, s, arg=None):
    return {"text": text.strip("\n")}


@adapter("H5P.InteractiveVideo")
def interactive_video(text, s, arg=None):
    """![titre](vidéo)  description…  ## 0:30 qcm … ## 1:10 texte … ## 2:00 signet: Partie 2"""
    pre, sections = split_headings(lines_of(text), 2)
    video, desc, transcript = None, [], None
    for ln, line in pre:
        im = IMAGE.match(line)
        tr = re.match(r"^\s*transcri(?:t|pt)\s*:\s*(\S.*?)\s*$", line, re.I)
        if im and video is None:
            video = im
        elif tr:
            transcript = tr.group(1)
        elif line.strip():
            desc.append(line.strip())
    if video is None:
        s.error(None, "vidéo manquante : une ligne « ![titre](vidéo ou URL YouTube) » avant les interactions")
        return {}
    start = {"title": video.group(1) or "Vidéo interactive"}
    if desc:
        start["shortStartDescription"] = " ".join(desc)[:120]
    interactions, bookmarks, endscreens = [], [], []
    for heading, hl, body in sections:
        m = re.match(r"^(\S+)\s+([\w.@-]+)\s*(?::\s*(.*))?$", heading)
        t = seconds(m.group(1)) if m else None
        if t is None:
            s.error(hl, "titre attendu : « ## <temps> <type> » (ex. « ## 1:30 qcm », « ## 2:00 signet: Partie 2 »)")
            continue
        kind, rest = m.group(2).lower(), (m.group(3) or "").strip()
        if kind in ("signet", "bookmark", "chapitre"):
            bookmarks.append({"time": t, "label": rest or join(body) or f"{m.group(1)}"})
            continue
        if kind in ("fin", "endscreen", "ecran-fin"):
            endscreens.append({"time": t, "label": rest or "Fin"})
            continue
        try:
            machine, _, _ = s.ctx.registry.machine_of(kind)
        except KeyError:
            s.error(hl, f"type d'interaction « {kind} » inconnu")
            continue
        if machine == "H5P.AdvancedText":
            machine = "H5P.Text"  # the video accepts H5P.Text, not AdvancedText
        sub = parse_sugar(machine, join(body), s.ctx, s.path, line_offset=s.line_offset + hl + 1, arg=rest or None)
        question = machine not in TEXT_TYPES
        item = {"duration": {"from": t, "to": t + 10}, "pause": question,
                "displayType": "poster" if question else "button",
                "action": {"library": machine, **sub}}
        item.update(POSTER_BOX if question else BUTTON_BOX)
        interactions.append(item)
    starts = sorted({it["duration"]["from"] for it in interactions})
    for it in interactions:   # shown 10 s, but gone when the next one appears (same place on screen)
        t = it["duration"]["from"]
        later = [x for x in starts if x > t]
        if later:
            it["duration"]["to"] = min(it["duration"]["to"], later[0])
    for t in starts:
        if sum(1 for it in interactions if it["duration"]["from"] == t) > 1:
            s.warn(None, f"plusieurs interactions à {t:g} s : elles se superposent à l'écran (les décaler)")
    out = {"interactiveVideo": {"video": {"files": [video.group(2)], "startScreenOptions": start},
                                "assets": {"interactions": interactions}}}
    if bookmarks:
        out["interactiveVideo"]["assets"]["bookmarks"] = bookmarks
    if endscreens:
        out["interactiveVideo"]["assets"]["endscreens"] = endscreens
    if transcript:
        out["transcript"] = transcript
    return out
