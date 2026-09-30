"""Media ingestion: a URL or a path (relative to the md file, then to the repo) becomes a file in the
package plus the H5P file object ({path, mime, copyright, width, height}).

Remote files are downloaded once into sources/.media/ and recorded in sources/.media/lock.json, so
that a rebuild (CI, another agent) is deterministic and needs no network.
"""
import hashlib
import io
import json
import mimetypes
import re
import urllib.parse
import urllib.request
from pathlib import Path

from .library import ROOT

STORE = ROOT / "sources" / ".media"
LOCK = STORE / "lock.json"
USER_AGENT = "h5p-harness/0.1 (+https://github.com/mcruzel/h5p-harness)"
MAX_DOWNLOAD = 150 * 1024 * 1024
MAX_IMAGE_PX = 1920          # longest side after ingestion
REENCODE_ABOVE = 800 * 1024  # re-encode images heavier than this

# default H5P content whitelist, per field kind (H5PCore::$defaultContentWhitelist)
KINDS = {
    "image": {"png": "image/png", "jpg": "image/jpeg", "jpeg": "image/jpeg", "gif": "image/gif"},
    "audio": {"mp3": "audio/mpeg", "m4a": "audio/mp4", "ogg": "audio/ogg", "wav": "audio/wav", "webm": "audio/webm"},
    "video": {"mp4": "video/mp4", "webm": "video/webm", "ogg": "video/ogg"},
    "file": {e: mimetypes.types_map.get("." + e, "application/octet-stream") for e in (
        "pdf rtf doc docx xls xlsx ppt pptx odt ods odp csv txt md vtt webvtt gltf glb json png jpg jpeg gif "
        "mp3 m4a ogg wav mp4 webm").split()},
}
KINDS["file"].update({"vtt": "text/vtt", "webvtt": "text/vtt", "glb": "model/gltf-binary",
                      "gltf": "model/gltf+json", "md": "text/markdown"})
FOLDER = {"image": "images", "audio": "audios", "video": "videos", "file": "files"}
STREAMING = [
    (re.compile(r"^https?://(www\.|m\.)?(youtube\.com|youtu\.be|youtube-nocookie\.com)/", re.I), "video/YouTube"),
    (re.compile(r"^https?://(www\.|player\.)?vimeo\.com/", re.I), "video/Vimeo"),
    (re.compile(r"^https?://[^/]*panopto\.(com|eu)/", re.I), "video/Panopto"),
    (re.compile(r"^https?://[^/]*echo360\.", re.I), "video/Echo360"),
]
LICENSES = ["CC BY-NC-SA", "CC BY-NC-ND", "CC BY-SA", "CC BY-ND", "CC BY-NC", "CC BY", "CC0 1.0", "CC PDM",
            "GNU GPL", "ODC PDDL", "PD", "U", "C"]
LICENSE_ALIASES = {"cc0": "CC0 1.0", "domaine public": "PD", "public domain": "PD", "pdm": "CC PDM",
                   "gpl": "GNU GPL", "copyright": "C", "tous droits réservés": "C", "inconnue": "U",
                   "undisclosed": "U"}


class MediaError(Exception):
    pass


def parse_license(text):
    """'CC BY-SA 4.0' -> ('CC BY-SA', '4.0'); unknown -> error."""
    t = str(text).strip()
    low = t.lower()
    if low in LICENSE_ALIASES:
        return LICENSE_ALIASES[low], None
    norm = re.sub(r"\s+", " ", t.upper().replace("CC-", "CC ").replace("_", " "))
    for lic in LICENSES:
        if norm.startswith(lic.upper()):
            rest = norm[len(lic):].strip()
            version = rest if re.fullmatch(r"\d\.\d", rest) else None
            if lic.startswith("CC B") and version is None:
                version = "4.0"
            return lic, version
    raise MediaError(f"licence '{t}' inconnue (ex.: CC BY-SA 4.0, CC0, PD, C, U)")


def slug(text, n=40):
    s = re.sub(r"[^a-zA-Z0-9]+", "-", text).strip("-").lower()
    return (s or "media")[:n]


class Media:
    def __init__(self, doc_dir: Path, offline=False):
        self.doc_dir = doc_dir
        self.offline = offline
        self.files = {}           # arcname -> bytes
        self.touched = set()      # repo files read or created (to commit with the source)
        self._lock = json.loads(LOCK.read_text(encoding="utf-8")) if LOCK.exists() else {}
        self._lock_dirty = False

    # ---- public -------------------------------------------------------------------------------
    def ingest(self, value, kind):
        """value: 'src' or {src, alt?, license, author, title, source, year}; kind: image|audio|video|file."""
        spec = {"src": value} if isinstance(value, str) else dict(value or {})
        src = str(spec.get("src") or spec.get("path") or spec.get("url") or "").strip()
        if not src:
            raise MediaError("source manquante (src: chemin ou URL)")
        copyright = self._copyright(spec)
        if kind == "video":
            for rx, mime in STREAMING:
                if rx.match(src):
                    return {"path": src, "mime": mime, "copyright": copyright}
        data, name = self._read(src)
        ext = Path(name).suffix.lower().lstrip(".")
        extra = {}
        if kind == "image":
            data, ext, extra = self._image(data, ext, src)
        allowed = KINDS[kind]
        if ext not in allowed:
            raise MediaError(f"format .{ext or '?'} refusé pour un champ {kind} "
                             f"(accepté: {', '.join(sorted(set(allowed)))})")
        digest = hashlib.sha256(data).hexdigest()[:10]
        arcname = f"{FOLDER[kind]}/{slug(Path(name).stem)}-{digest}.{ext}"
        self.files[arcname] = data
        obj = {"path": arcname, "mime": allowed[ext], "copyright": copyright}
        obj.update(extra)
        return obj

    def save_lock(self):
        if self._lock_dirty:
            STORE.mkdir(parents=True, exist_ok=True)
            LOCK.write_text(json.dumps(dict(sorted(self._lock.items())), indent=1, ensure_ascii=False) + "\n",
                            encoding="utf-8")
            self.touched.add(LOCK)

    # ---- internals -----------------------------------------------------------------------------
    def _copyright(self, spec):
        c = {"license": "U"}
        if spec.get("license") or spec.get("licence"):
            lic, version = parse_license(spec.get("license") or spec.get("licence"))
            c["license"] = lic
            if version:
                c["version"] = version
        for src_key, dst in (("author", "author"), ("auteur", "author"), ("title", "title"), ("titre", "title"),
                             ("source", "source"), ("year", "year"), ("annee", "year")):
            if spec.get(src_key):
                c[dst] = str(spec[src_key])
        return c

    def _read(self, src):
        if re.match(r"^https?://", src, re.I):
            return self._download(src), urllib.parse.unquote(Path(urllib.parse.urlparse(src).path).name or "media")
        path = Path(src)
        # "/x/y.png" = relative to the repository root; otherwise relative to the .md, then to the root
        candidates = [ROOT / src.lstrip("/"), path] if path.is_absolute() else [self.doc_dir / path, ROOT / src]
        for c in candidates:
            c = c.resolve()
            if c.is_file():
                if ROOT not in c.parents:
                    raise MediaError(f"{src}: fichier hors du dépôt")
                self.touched.add(c)
                return c.read_bytes(), c.name
        raise MediaError(f"{src}: fichier introuvable (relatif au .md puis à la racine du dépôt)")

    def _download(self, url):
        entry = self._lock.get(url)
        if entry:
            f = STORE / entry["file"]
            if f.is_file() and hashlib.sha256(f.read_bytes()).hexdigest() == entry["sha256"]:
                self.touched.add(f)
                return f.read_bytes()
        if self.offline:
            raise MediaError(f"{url}: absent du cache sources/.media et mode hors ligne")
        req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
        try:
            with urllib.request.urlopen(req, timeout=60) as resp:
                data = resp.read(MAX_DOWNLOAD + 1)
        except Exception as e:  # network, 403, 404...
            raise MediaError(f"{url}: téléchargement impossible ({e})") from None
        if len(data) > MAX_DOWNLOAD:
            raise MediaError(f"{url}: fichier trop lourd (> {MAX_DOWNLOAD // 2**20} Mo)")
        sha = hashlib.sha256(data).hexdigest()
        name = urllib.parse.unquote(Path(urllib.parse.urlparse(url).path).name) or "media"
        fname = f"{sha[:16]}-{slug(Path(name).stem, 30)}{Path(name).suffix.lower()[:6]}"
        STORE.mkdir(parents=True, exist_ok=True)
        (STORE / fname).write_bytes(data)
        self.touched.add(STORE / fname)
        self._lock[url] = {"file": fname, "sha256": sha, "bytes": len(data)}
        self._lock_dirty = True
        return data

    def _image(self, data, ext, src):
        try:
            from PIL import Image
        except ImportError:  # dimensions only, no conversion
            raise MediaError("Pillow n'est pas installé (pip install -r requirements.txt)") from None
        if ext == "svg" or data.lstrip()[:5] in (b"<?xml", b"<svg ") or b"<svg" in data[:300]:
            return self._svg(data, src)
        try:
            img = Image.open(io.BytesIO(data))
            img.load()
        except Exception:
            raise MediaError(f"{src}: image illisible") from None
        fmt = (img.format or "").upper()
        w, h = img.size
        convert = fmt not in ("PNG", "JPEG", "GIF")
        too_big = max(w, h) > MAX_IMAGE_PX or len(data) > REENCODE_ABOVE
        if fmt == "GIF" and getattr(img, "is_animated", False):
            convert = too_big = False  # keep animations untouched
        if convert or too_big:
            if max(w, h) > MAX_IMAGE_PX:
                ratio = MAX_IMAGE_PX / max(w, h)
                img = img.resize((max(1, round(w * ratio)), max(1, round(h * ratio))), Image.LANCZOS)
            has_alpha = img.mode in ("RGBA", "LA", "P") and (img.mode != "P" or "transparency" in img.info)
            buf = io.BytesIO()
            if has_alpha:
                img.convert("RGBA").save(buf, "PNG", optimize=True)
                ext = "png"
            else:
                img.convert("RGB").save(buf, "JPEG", quality=85, optimize=True, progressive=True)
                ext = "jpg"
            data = buf.getvalue()
            w, h = img.size
        else:
            ext = {"PNG": "png", "JPEG": "jpg", "GIF": "gif"}[fmt]
        return data, ext, {"width": w, "height": h}

    def _svg(self, data, src):
        try:
            import cairosvg  # optional
        except ImportError:
            raise MediaError(f"{src}: SVG refusé par H5P/Moodle; fournir un PNG/JPG "
                             "(ou installer cairosvg pour la conversion automatique)") from None
        png = cairosvg.svg2png(bytestring=data, output_width=MAX_IMAGE_PX)
        return self._image(png, "png", src)
