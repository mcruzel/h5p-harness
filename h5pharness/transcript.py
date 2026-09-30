"""Timestamped transcripts (WebVTT or SRT) of a video.

An interactive video only gets H5P interactions when they are written from what the video says:
the source declares the transcript (`transcript:`), the harness checks the interactions against it
and adds it to the video as subtitles. `python -m h5pharness transcript <file>` prints a compact
version for the agent that writes the questions.
"""
import html
import re
import unicodedata
from dataclasses import dataclass

TIMESTAMP = r"(?:(\d+):)?(\d{1,2}):(\d{2})[.,](\d{1,3})"
CUE = re.compile(rf"^\s*{TIMESTAMP}\s*-->\s*{TIMESTAMP}")
TAG = re.compile(r"<[^>]+>")


class TranscriptError(Exception):
    pass


@dataclass
class Cue:
    start: float
    end: float
    text: str


def _seconds(h, m, s, ms):
    return int(h or 0) * 3600 + int(m) * 60 + int(s) + int(ms.ljust(3, "0")) / 1000


def parse(data):
    """WebVTT or SRT text -> cues (start, end in seconds; text without tags)."""
    text = data.decode("utf-8-sig", errors="replace") if isinstance(data, bytes) else str(data)
    blocks = re.split(r"\n\s*\n", text.replace("\r\n", "\n").replace("\r", "\n").strip())
    cues = []
    for block in blocks:
        lines = block.split("\n")
        i = next((k for k, line in enumerate(lines) if CUE.match(line)), None)
        if i is None:
            continue  # WEBVTT header, NOTE, STYLE, REGION
        m = CUE.match(lines[i])
        start, end = _seconds(*m.groups()[:4]), _seconds(*m.groups()[4:])
        words = html.unescape(TAG.sub("", " ".join(lines[i + 1:]))).split()
        if words:
            cues.append(Cue(start, end, " ".join(words)))
    if not cues:
        raise TranscriptError("aucune réplique horodatée (format WebVTT ou SRT attendu : « 00:01.000 --> 00:04.000 »)")
    for a, b in zip(cues, cues[1:]):
        if b.start + 0.5 < a.start:
            raise TranscriptError(f"horodatage non chronologique vers {clock(b.start)}")
    return cues


def clock(t):
    t = int(t)
    return f"{t // 3600}:{t % 3600 // 60:02d}:{t % 60:02d}" if t >= 3600 else f"{t // 60}:{t % 60:02d}"


def _vtt_time(t):
    ms = round(t * 1000)
    return f"{ms // 3600000:02d}:{ms // 60000 % 60:02d}:{ms // 1000 % 60:02d}.{ms % 1000:03d}"


def to_vtt(cues):
    return "WEBVTT\n\n" + "\n\n".join(f"{_vtt_time(c.start)} --> {_vtt_time(c.end)}\n{c.text}" for c in cues) + "\n"


def compact(cues, step=30):
    """One line per ~step seconds: 'm:ss texte…' (times usable as-is in « ## m:ss qcm »)."""
    lines, cur, start = [], [], None
    for c in cues:
        if start is None:
            start = c.start
        if cur and c.start - start >= step:
            lines.append(f"{clock(start)} {' '.join(cur)}")
            cur, start = [], c.start
        cur.append(c.text)
    if cur:
        lines.append(f"{clock(start)} {' '.join(cur)}")
    return lines


STOP = set("""quelle quelles quel quels laquelle lesquelles lequel lesquels parmi suivante suivantes suivant
reponse reponses vrai faux cette cette ceux celle celles comme leurs entre alors aussi avant apres
encore toujours jamais pourquoi comment combien quand autre autres chaque selon depuis pendant
correct correcte bonne bonnes mauvaise affirmation affirmations propose proposes video""".split())


def content_words(text):
    """Words of 5+ letters without accents or common question words (for a rough overlap test)."""
    plain = unicodedata.normalize("NFKD", text.lower())
    plain = "".join(ch for ch in plain if not unicodedata.combining(ch))
    return {w for w in re.findall(r"[a-z]{5,}", plain) if w not in STOP}


def window_text(cues, t, before=120, after=5):
    return " ".join(c.text for c in cues if c.end >= t - before and c.start <= t + after)
