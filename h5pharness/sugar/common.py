"""Shared parsing helpers for the Markdown sugar."""
import re

CHECK = re.compile(r"^(\s*)[-*+]\s+\[( |x|X)\]\s*(.*)$")
BULLET = re.compile(r"^(\s*)(?:[-*+]|\d+[.)])\s+(.*)$")
IMAGE = re.compile(r"^\s*!\[([^\]]*)\]\(\s*<?([^)\s>]+)>?(?:\s+\"([^\"]*)\")?\s*\)\s*$")
HEADING = re.compile(r"^(#{1,6})\s+(.*?)\s*#*\s*$")
DIRECTIVE = re.compile(r"^:::\s*([\w.@-]+)\s*(.*?)\s*$")
VIDEO_EXT = {"mp4", "webm", "ogv", "mov"}
AUDIO_EXT = {"mp3", "m4a", "ogg", "oga", "wav"}
STREAMING = re.compile(r"^https?://([^/]*\.)?(youtube\.com|youtu\.be|vimeo\.com|panopto\.|echo360\.)", re.I)


def lines_of(text):
    return list(enumerate(text.split("\n")))


def paragraphs(numbered):
    """[(line, text)] -> [(first_line, [lines])] separated by blank lines."""
    out, cur, start = [], [], None
    for ln, line in numbered:
        if line.strip():
            if not cur:
                start = ln
            cur.append(line)
        elif cur:
            out.append((start, cur))
            cur = []
    if cur:
        out.append((start, cur))
    return out


def ext_of(src):
    tail = src.split("?")[0].split("#")[0].rsplit("/", 1)[-1]
    return tail.rsplit(".", 1)[-1].lower() if "." in tail else ""


def media_library(alt, src, title=None):
    """![alt](src) -> raw sub-content for H5P.Image / H5P.Video / H5P.Audio."""
    ext = ext_of(src)
    if STREAMING.match(src) or ext in VIDEO_EXT:
        value = {"library": "H5P.Video", "sources": [src]}
        if alt:
            value["metadata"] = {"title": alt}
        return value
    if ext in AUDIO_EXT:
        value = {"library": "H5P.Audio", "files": [src]}
        if alt:
            value["metadata"] = {"title": alt}
        return value
    value = {"library": "H5P.Image", "file": {"src": src}}
    if alt.strip():
        value["alt"] = alt.strip()
    else:
        value["decorative"] = True
    if title:
        value["title"] = title
    return value


def image_field(alt, src, title=None):
    """For plain image fields (not sub-content): {src, title?}."""
    value = {"src": src}
    if title:
        value["title"] = title
    return value


def split_headings(numbered, level):
    """-> preamble [(ln, line)], [(heading_text, heading_line, [(ln, line)])] for headings of `level`."""
    marker = re.compile(r"^" + "#" * level + r"(?!#)\s+(.*?)\s*#*\s*$")
    pre, sections = [], []
    for ln, line in numbered:
        m = marker.match(line)
        if m:
            sections.append((m.group(1).strip(), ln, []))
        elif sections:
            sections[-1][2].append((ln, line))
        else:
            pre.append((ln, line))
    return pre, sections


def join(numbered):
    return "\n".join(l for _, l in numbered).strip("\n")


def parse_choices(numbered, s, allow_media=True):
    """Question text + '- [x] answer' lines (+ indented '> feedback', '? tip', '< not-chosen feedback').

    Returns dict(question=[(ln, line)], answers=[{text, correct, line, feedback, tip, not_chosen}], media)."""
    question, answers, media = [], [], None
    for ln, line in numbered:
        m = CHECK.match(line)
        if m:
            answers.append({"text": m.group(3).strip(), "correct": m.group(2) != " ", "line": ln})
            continue
        stripped = line.strip()
        if answers:
            if not stripped:
                continue
            key = {">": "feedback", "?": "tip", "<": "not_chosen"}.get(stripped[0])
            if key and line[:1] in (" ", "\t"):
                prev = answers[-1].get(key)
                answers[-1][key] = (prev + "\n" if prev else "") + stripped[1:].strip()
                continue
            if line[:1] in (" ", "\t"):
                answers[-1]["text"] += " " + stripped
                continue
            s.error(ln, "texte après les réponses: le placer avant la liste - [x]/- [ ]")
            continue
        im = IMAGE.match(line)
        if im and allow_media and media is None:
            media = media_library(im.group(1), im.group(2), im.group(3))
            continue
        question.append((ln, line))
    return {"question": question, "answers": answers, "media": media}
