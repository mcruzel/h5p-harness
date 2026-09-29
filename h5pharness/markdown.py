"""Markdown -> HTML restricted to the tags an H5P field accepts (mirrors H5PContentValidator)."""
import html
import re
from html.parser import HTMLParser

from markdown_it import MarkdownIt

_MD = MarkdownIt("commonmark", {"html": True, "breaks": True, "typographer": False}).enable(
    ["table", "strikethrough"])

BASE_TAGS = {"div", "span", "p", "br"}
VOID = {"br", "hr", "img", "col"}
HEADINGS = ["h1", "h2", "h3", "h4", "h5", "h6"]
TABLE_TAGS = {"table", "thead", "tbody", "tfoot", "tr", "td", "th", "colgroup", "col"}
INLINE_FORMAT = {"strong", "em", "b", "i", "u", "s", "del", "strike", "sub", "sup", "code", "span", "mark", "small"}
SAFE_URL = re.compile(r"^(https?:|mailto:|ftp:|#|/|\.)", re.I)


def allowed_tags(field):
    """Same expansion rules as H5PContentValidator::validateText."""
    tags = BASE_TAGS | set(field.get("tags", []))
    if "table" in tags:
        tags |= {"tr", "td", "th", "colgroup", "col", "thead", "tbody", "tfoot", "figure", "figcaption"}
    if "b" in tags:
        tags.add("strong")
    if "i" in tags:
        tags.add("em")
    if "ul" in tags or "ol" in tags:
        tags.add("li")
    if "del" in tags or "strike" in tags:
        tags.add("s")
    return tags


def is_html_field(field):
    return field.get("type") == "text" and (field.get("widget") == "html" or "tags" in field)


class _Node:
    __slots__ = ("tag", "attrs", "children")

    def __init__(self, tag, attrs=None):
        self.tag, self.attrs, self.children = tag, attrs or [], []


class _Builder(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.root = _Node(None)
        self.stack = [self.root]

    def handle_starttag(self, tag, attrs):
        node = _Node(tag, attrs)
        self.stack[-1].children.append(node)
        if tag not in VOID:
            self.stack.append(node)

    def handle_startendtag(self, tag, attrs):
        self.stack[-1].children.append(_Node(tag, attrs))

    def handle_endtag(self, tag):
        for i in range(len(self.stack) - 1, 0, -1):
            if self.stack[i].tag == tag:
                del self.stack[i:]
                break

    def handle_data(self, data):
        self.stack[-1].children.append(data)


def _parse(fragment):
    b = _Builder()
    b.feed(fragment)
    b.close()
    return b.root


def _serialize(nodes):
    out = []
    for n in nodes:
        if isinstance(n, str):
            out.append(html.escape(n, quote=False))
            continue
        attrs = "".join(f' {k}="{html.escape(v or "", quote=True)}"' for k, v in n.attrs)
        if n.tag in VOID:
            out.append(f"<{n.tag}{attrs}>" if n.tag != "br" else "<br>")
        else:
            out.append(f"<{n.tag}{attrs}>{_serialize(n.children)}</{n.tag}>")
    return "".join(out)


def _text_of(node):
    if isinstance(node, str):
        return node
    return "".join(_text_of(c) for c in node.children)


class Converter:
    """One conversion = one field; collects errors/warnings as short French messages."""

    def __init__(self, field):
        self.field = field
        self.allowed = allowed_tags(field)
        self.errors, self.warnings = [], []
        self.heading_map = {}

    def _plan_headings(self, nodes):
        """Shift heading levels so the author's top level lands on the field's top allowed level."""
        levels = [h for h in HEADINGS if h in self.allowed]
        used = set()

        def walk(ns):
            for n in ns:
                if not isinstance(n, str):
                    if n.tag in HEADINGS:
                        used.add(HEADINGS.index(n.tag))
                    walk(n.children)

        walk(nodes)
        if not levels or not used:
            return
        allowed_idx = [HEADINGS.index(h) for h in levels]
        offset = max(0, allowed_idx[0] - min(used))
        for i in used:
            target = i + offset
            fits = [a for a in allowed_idx if a >= target]
            self.heading_map[HEADINGS[i]] = HEADINGS[fits[0] if fits else allowed_idx[-1]]

    def _clean(self, nodes):
        out = []
        for n in nodes:
            if isinstance(n, str):
                out.append(n)
                continue
            tag = n.tag
            if tag in TABLE_TAGS and "table" not in self.allowed:
                self._error("tableau non autorisé dans ce champ")
                continue
            if tag == "img":
                self._error("image dans un texte: utiliser un champ image ou un sous-contenu image")
                continue
            n.children = self._clean(n.children)
            if tag in HEADINGS:
                if self.heading_map:
                    n.tag = self.heading_map[tag]
                else:
                    self._warn("titres non autorisés dans ce champ (convertis en texte)")
                    wrap = _Node("strong") if "strong" in self.allowed else None
                    para = _Node("p")
                    if wrap:
                        wrap.children = n.children
                        para.children = [wrap]
                    else:
                        para.children = n.children
                    out.append(para)
                    continue
            elif tag not in self.allowed:
                if tag in INLINE_FORMAT or tag == "a":
                    self._warn(f"mise en forme <{tag}> non autorisée dans ce champ (retirée)")
                    out.extend(n.children)
                    continue
                if tag in ("ul", "ol"):
                    self._warn("listes non autorisées dans ce champ (converties en lignes)")
                    lines = []
                    for i, li in enumerate(c for c in n.children if not isinstance(c, str)):
                        prefix = f"{i + 1}. " if tag == "ol" else "• "
                        if lines:
                            lines.append(_Node("br"))
                        lines.append(prefix)
                        lines.extend(self._unwrap_p(li.children))
                    para = _Node("p")
                    para.children = lines
                    out.append(para)
                    continue
                if tag in ("blockquote", "pre"):
                    self._warn(f"bloc <{tag}> non autorisé dans ce champ (retiré)")
                    out.extend(n.children)
                    continue
                if tag == "hr":
                    self._warn("séparateur --- non autorisé dans ce champ (retiré)")
                    continue
                self._error(f"balise <{tag}> interdite dans ce champ "
                            f"(autorisées: {', '.join(sorted(self.allowed - BASE_TAGS)) or 'aucune'})")
                continue
            n.attrs = self._attrs(n)
            out.append(n)
        return out

    def _unwrap_p(self, children):
        out = []
        for c in children:
            if not isinstance(c, str) and c.tag == "p":
                out.extend(c.children)
            else:
                out.append(c)
        return out

    def _attrs(self, n):
        keep = []
        for k, v in n.attrs:
            if n.tag == "a" and k == "href":
                if v and SAFE_URL.match(v):
                    keep.append((k, v))
                    if "target" not in dict(n.attrs):
                        keep.append(("target", "_blank"))
            elif n.tag == "a" and k == "target":
                keep.append((k, v))
            elif n.tag in ("td", "th") and k in ("colspan", "rowspan"):
                keep.append((k, v))
            elif k == "style" and v and re.fullmatch(r"\s*text-align:\s*(left|right|center)\s*;?\s*", v):
                keep.append((k, v))
        return keep

    def _error(self, msg):
        if msg not in self.errors:
            self.errors.append(msg)

    def _warn(self, msg):
        if msg not in self.warnings:
            self.warnings.append(msg)

    def convert(self, text, protect=None):
        """Return HTML; `protect` is a compiled regex whose matches are copied verbatim (H5P markers)."""
        text = str(text).replace("\r\n", "\n").strip("\n")
        saved = []
        if protect is not None:
            def keep(m):
                saved.append(m.group(0))
                return f"{len(saved) - 1}"
            text = protect.sub(keep, text)
        rendered = _MD.render(text)
        root = _parse(rendered)
        nodes = [c for c in root.children if not (isinstance(c, str) and not c.strip())]
        self._plan_headings(nodes)
        nodes = self._clean(nodes)
        enter = self.field.get("enterMode", "p")
        if enter == "div":
            for n in nodes:
                if not isinstance(n, str) and n.tag == "p":
                    n.tag = "div"
        out = _serialize(nodes)
        if saved:
            out = re.sub("(\\d+)", lambda m: html.escape(saved[int(m.group(1))], quote=False), out)
        return out


def to_html(text, field, protect=None):
    conv = Converter(field)
    return conv.convert(text, protect=protect), conv.errors, conv.warnings


def html_to_text(fragment):
    return re.sub(r"\s+", " ", _text_of(_parse(str(fragment)))).strip()
