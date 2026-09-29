"""Command line: python -m h5pharness <build|check|types|spec|specs|libs> ...

Output contract (kept tiny for AI agents):
  exit 0  OK            -> "OK <paquet> (...)" [+ avertissements]
  exit 1  source à corriger -> "ERREUR <fichier>: n problème(s)" + au plus 8 lignes "- …"
  exit 2  environnement (git, réseau, disque) -> ne pas régénérer le contenu, signaler à l'humain
  exit 3  bogue du harnais -> trace dans dist/.harness-error.log
"""
import argparse
import json
import traceback
from pathlib import Path

MAX_LINES = 8


def _files(targets):
    out = []
    for t in targets:
        p = Path(t)
        if p.is_dir():
            out += sorted(x for x in p.rglob("*.md") if not any(part.startswith(".") for part in x.parts))
        else:
            out.append(p)
    return out


def _rel(p):
    try:
        return Path(p).resolve().relative_to(Path.cwd().resolve())
    except ValueError:
        return p


def _size(n):
    return f"{n / 1024:.0f} Ko" if n < 1024 * 1024 else f"{n / 1024 / 1024:.1f} Mo".replace(".", ",")


def cmd_build(args, write=True):
    from .build import DIST, build_one
    from .library import Registry
    registry = Registry()
    files = _files(args.sources)
    if not files:
        print("ERREUR aucun fichier .md trouvé")
        return 1
    results, code = [], 0
    for f in files:
        if not f.exists():
            print(f"ERREUR {f}: fichier introuvable")
            code = max(code, 1)
            continue
        r = build_one(f, registry, out_dir=Path(args.out) if args.out else DIST,
                      full=not args.content_only, offline=args.offline, write=write)
        results.append(r)
        if args.json:
            continue
        if r.ok:
            where = f"{_rel(r.out)} ({_size(r.size)}, {r.ms} ms)" if r.out else f"{f} valide"
            print(f"OK {where}")
        else:
            code = max(code, 1)
            print(f"ERREUR {f}: {len(r.errors)} problème(s)")
            for e in r.errors[:MAX_LINES]:
                print(f"- {e}")
            if len(r.errors) > MAX_LINES:
                print(f"- … et {len(r.errors) - MAX_LINES} autre(s)")
        if r.warnings and not args.quiet:
            print("  avertissement(s): " + " | ".join(r.warnings[:3]) +
                  (f" (+{len(r.warnings) - 3})" if len(r.warnings) > 3 else ""))
    if args.json:
        print(json.dumps([{"source": str(r.source), "ok": r.ok, "package": str(r.out) if r.out else None,
                           "errors": r.errors, "warnings": r.warnings, "bytes": r.size} for r in results],
                         ensure_ascii=False, indent=1))
    if code == 0 and write and getattr(args, "publish", False):
        from .publish import PublishError, publish
        touched = set().union(*(r.touched for r in results))
        titles = ", ".join(r.title for r in results[:3]) + ("…" if len(results) > 3 else "")
        try:
            print("PUBLIÉ " + publish(touched, f"h5p: {titles}"))
        except PublishError as e:
            print(f"ECHEC_PUBLICATION {e} (paquet(s) construit(s) localement; ne pas régénérer le contenu)")
            return 2
    return code


def cmd_types(args):
    from .library import Registry
    from .sugar import has_adapter
    reg = Registry()
    rows = []
    for lib in reg.runnable_types():
        aliases = reg.aliases_of(lib.machine)
        rows.append((aliases[0] if aliases else lib.machine, lib.machine, f"{lib.major}.{lib.minor}",
                     "md" if has_adapter(lib.machine) else "yaml", lib.title))
    if args.json:
        print(json.dumps([dict(zip(("alias", "machine", "version", "syntaxe", "titre"), r)) for r in rows],
                         ensure_ascii=False, indent=1))
    else:
        for r in rows:
            print(f"{r[0]:<22} {r[1]:<34} {r[2]:<6} {r[3]:<5} {r[4]}")
    return 0


def cmd_spec(args):
    from .library import Registry, UnknownLibrary
    from .specs import render_spec
    reg = Registry()
    try:
        lib = reg.resolve(args.type)
    except UnknownLibrary:
        print(f"ERREUR type « {args.type} » inconnu")
        return 1
    print(render_spec(reg, lib))
    return 0


def cmd_specs(args):
    from .specs import write_all
    n = write_all()
    print(f"OK {n} fiches écrites dans specs/")
    return 0


def cmd_libs(args):
    from .library import Registry
    reg = Registry()
    for folder, lib in sorted(reg.by_folder.items()):
        print(f"{lib.machine} {lib.major}.{lib.minor}.{lib.patch}")
    return 0


def main(argv=None):
    ap = argparse.ArgumentParser(prog="python -m h5pharness", description="Markdown -> paquets H5P (Moodle)")
    sub = ap.add_subparsers(dest="cmd", required=True)
    for name in ("build", "check"):
        p = sub.add_parser(name, help="construire" if name == "build" else "valider sans écrire de paquet")
        p.add_argument("sources", nargs="+", help="fichier(s) .md ou dossier(s)")
        p.add_argument("-o", "--out", help="dossier de sortie (défaut: dist/)")
        p.add_argument("--content-only", action="store_true", help="paquet sans bibliothèques (plateforme équipée)")
        p.add_argument("--offline", action="store_true", help="aucun téléchargement de média")
        p.add_argument("--json", action="store_true")
        p.add_argument("-q", "--quiet", action="store_true", help="masquer les avertissements")
        if name == "build":
            p.add_argument("--publish", action="store_true", help="git add + commit + push des sources")
    p = sub.add_parser("types", help="lister les types de contenu")
    p.add_argument("--json", action="store_true")
    p = sub.add_parser("spec", help="afficher la fiche d'un type")
    p.add_argument("type")
    sub.add_parser("specs", help="régénérer specs/")
    sub.add_parser("libs", help="versions des bibliothèques embarquées")
    args = ap.parse_args(argv)
    try:
        if args.cmd == "build":
            return cmd_build(args)
        if args.cmd == "check":
            return cmd_build(args, write=False)
        return {"types": cmd_types, "spec": cmd_spec, "specs": cmd_specs, "libs": cmd_libs}[args.cmd](args)
    except KeyboardInterrupt:
        return 2
    except OSError as e:
        print(f"ECHEC_ENVIRONNEMENT {e}")
        return 2
    except Exception:  # harness bug: keep stdout short, full trace in a log file
        from .build import DIST
        DIST.mkdir(parents=True, exist_ok=True)
        log = DIST / ".harness-error.log"
        log.write_text(traceback.format_exc(), encoding="utf-8")
        print(f"ECHEC_HARNAIS {traceback.format_exc().strip().splitlines()[-1]} (détails: {log})")
        return 3
