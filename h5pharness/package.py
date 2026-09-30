"""Assemble the .h5p archive (reproducible zip) and run the structural checks of H5PValidator."""
import json
import re
import zipfile
from pathlib import Path

from .library import Library, Registry

ZIP_DATE = (1980, 1, 1, 0, 0, 0)
CONTENT_EXT = set("json png jpg jpeg gif bmp tif tiff eot ttf woff woff2 otf webm mp4 ogg mp3 m4a wav txt pdf rtf "
                  "doc docx xls xlsx ppt pptx odt ods odp csv diff patch swf md textile vtt webvtt gltf glb".split())
LIBRARY_EXT = CONTENT_EXT | {"js", "css", "svg", "xml"}
LICENSE_RE = re.compile(r"^(CC BY|CC BY-SA|CC BY-ND|CC BY-NC|CC BY-NC-SA|CC BY-NC-ND|CC0 1\.0|GNU GPL|PD|ODC PDDL|"
                        r"CC PDM|U|C)$")
ALL_KINDS = ("preloadedDependencies", "dynamicDependencies", "editorDependencies")
RUNTIME_KINDS = ("preloadedDependencies", "dynamicDependencies")


def h5p_json(meta, main: Library, runtime):
    from .media import MediaError, parse_license
    data = {
        "title": str(meta["title"])[:255],
        "language": str(meta.get("language", "fr")),
        "mainLibrary": main.machine,
        "embedTypes": list(main.meta.get("embedTypes") or ["iframe"]),
        "license": "U",
        "defaultLanguage": str(meta.get("language", "fr")),
        "preloadedDependencies": [
            {"machineName": l.machine, "majorVersion": l.major, "minorVersion": l.minor} for l in runtime],
    }
    if meta.get("license"):
        try:
            lic, version = parse_license(meta["license"])
            data["license"] = lic
            if version:
                data["licenseVersion"] = version
        except MediaError as e:
            raise ValueError(f"en-tête license: {e}") from None
    authors = meta.get("authors")
    if authors:
        names = authors if isinstance(authors, list) else [a.strip() for a in str(authors).split(",")]
        data["authors"] = [{"name": str(n)[:255], "role": "Author"} for n in names if str(n).strip()]
    if meta.get("source"):
        data["source"] = str(meta["source"])
    if meta.get("year"):
        data["yearFrom"] = str(meta["year"])
    return data


def libraries_for(registry: Registry, used, full=True):
    """(runtime libraries for h5p.json, libraries to embed, missing 'M x.y')."""
    main_first = list(used)
    runtime, missing_rt = registry.closure(main_first, RUNTIME_KINDS)
    if not full:
        return runtime, [], missing_rt
    embedded, missing = registry.closure(main_first, ALL_KINDS)
    return runtime, embedded, missing | missing_rt


def library_files(lib: Library):
    for f in sorted(lib.path.rglob("*")):
        if f.is_file():
            rel = f.relative_to(lib.path).as_posix()
            if any(part.startswith((".", "_")) for part in rel.split("/")):
                continue
            if f.suffix.lower().lstrip(".") in LIBRARY_EXT:
                yield f, rel


def _info(name):
    zi = zipfile.ZipInfo(name, ZIP_DATE)
    zi.compress_type = zipfile.ZIP_DEFLATED
    zi.external_attr = 0o644 << 16
    return zi


def write(out: Path, h5p: dict, params: dict, media_files: dict, embedded):
    out.parent.mkdir(parents=True, exist_ok=True)
    tmp = out.with_name(out.name + ".tmp")
    with zipfile.ZipFile(tmp, "w", zipfile.ZIP_DEFLATED, compresslevel=6) as z:
        z.writestr(_info("h5p.json"), json.dumps(h5p, ensure_ascii=False, indent=None))
        z.writestr(_info("content/content.json"), json.dumps(params, ensure_ascii=False))
        for arc in sorted(media_files):
            z.writestr(_info(f"content/{arc}"), media_files[arc])
        for lib in sorted(embedded, key=lambda l: l.folder):
            for f, rel in library_files(lib):
                z.writestr(_info(f"{lib.folder}/{rel}"), f.read_bytes())
    tmp.replace(out)


# ---- structural checks (subset of H5PValidator::isValidPackage) ------------------------------------

H5P_REQUIRED = {
    "title": re.compile(r"^.{1,255}$"),
    "language": re.compile(r"^[-a-zA-Z]{1,10}$"),
    "mainLibrary": re.compile(r"^[$a-z_][0-9a-z_.$]{1,254}$", re.I),
}


def check_archive(path: Path, installed=None):
    """Return a list of problems; `installed` = set of 'M x.y' assumed present on the platform."""
    problems = []
    with zipfile.ZipFile(path) as z:
        names = [n for n in z.namelist() if not re.search(r"(^|/)[._]", n)]
        if "h5p.json" not in names:
            return ["h5p.json absent"]
        if "content/content.json" not in names:
            problems.append("content/content.json absent")
        h5p = json.loads(z.read("h5p.json"))
        for k, rx in H5P_REQUIRED.items():
            if not isinstance(h5p.get(k), str) or not rx.match(h5p[k]):
                problems.append(f"h5p.json: {k} invalide")
        if not h5p.get("preloadedDependencies"):
            problems.append("h5p.json: preloadedDependencies vide")
        if not set(h5p.get("embedTypes", [])) <= {"iframe", "div"} or not h5p.get("embedTypes"):
            problems.append("h5p.json: embedTypes invalide")
        if not LICENSE_RE.match(h5p.get("license", "U")):
            problems.append("h5p.json: licence invalide")
        libs = {}
        for n in names:
            ext = n.rsplit(".", 1)[-1].lower() if "." in n.split("/")[-1] else ""
            if n.startswith("content/"):
                if n.endswith("/"):
                    continue
                if ext not in CONTENT_EXT:
                    problems.append(f"{n}: extension refusée par H5P")
            elif "/" in n and not n.endswith("/"):
                if ext not in LIBRARY_EXT:
                    problems.append(f"{n}: extension refusée par H5P")
                folder = n.split("/")[0]
                if n == f"{folder}/library.json":
                    libs[folder] = json.loads(z.read(n))
        present = set(installed or ())
        for folder, lj in libs.items():
            present.add(f"{lj['machineName']} {lj['majorVersion']}.{lj['minorVersion']}")
            for key in ("preloadedJs", "preloadedCss"):
                for item in lj.get(key, []):
                    if f"{folder}/{item['path']}" not in names:
                        problems.append(f"{folder}: fichier déclaré absent {item['path']}")
        wanted = [(d, "h5p.json") for d in h5p.get("preloadedDependencies", [])]
        for folder, lj in libs.items():
            for kind in ALL_KINDS:
                wanted += [(d, folder) for d in lj.get(kind, [])]
        for d, who in wanted:
            key = f"{d['machineName']} {d['majorVersion']}.{d['minorVersion']}"
            if key not in present:
                problems.append(f"bibliothèque manquante {key} (requise par {who})")
    return sorted(set(problems))
