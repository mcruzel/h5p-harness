"""Markdown sugar: friendly syntaxes that produce the same raw params as the generic ```yaml form.

Each adapter receives the Markdown body and returns a dict of raw values (semantics field names),
which the engine then completes (defaults, translations), converts and validates.
"""
ADAPTERS = {}


def adapter(*machines):
    def deco(fn):
        for m in machines:
            ADAPTERS[m] = fn
        return fn
    return deco


class Sugar:
    """Passed to adapters: line-aware error reporting (lines are 0-based within the adapter text)."""

    def __init__(self, ctx, path, line_offset=1):
        self.ctx, self.path, self.line_offset = ctx, list(path), line_offset

    def _where(self, line):
        return f"l.{self.line_offset + line}" if line is not None else None

    def error(self, line, msg):
        where = self._where(line)
        self.ctx.error(self.path, f"{where}: {msg}" if where else msg)

    def warn(self, line, msg):
        where = self._where(line)
        self.ctx.warn(self.path, f"{where}: {msg}" if where else msg)


def has_adapter(machine):
    _load()
    return machine in ADAPTERS


def parse_sugar(machine, text, ctx, path, line_offset=1, arg=None):
    _load()
    fn = ADAPTERS.get(machine)
    if fn is None:
        ctx.error(path, f"{machine}: pas de syntaxe Markdown simplifiée; écrire les champs dans un bloc ```yaml "
                        "(voir la fiche du type dans specs/)")
        return {}
    return fn(text, Sugar(ctx, path, line_offset), arg=arg) or {}


_loaded = False


def _load():
    global _loaded
    if not _loaded:
        _loaded = True
        from . import questions, games, cards, containers, media_types, presentation, video, dragdrop  # noqa: F401
