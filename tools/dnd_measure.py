"""Mesure de la hauteur d'un glisser-déposer H5P (H5P.DragQuestion) avant et après « Vérifier ».

Une activité qui s'allonge après « Vérifier » (retours par zone, score) déborde de l'iframe ou pousse la page.
Cette mesure la joue dans Chromium à plusieurs largeurs, dépose les étiquettes selon un plan déduit des bonnes
réponses du content.json, clique « Vérifier » et rend la hauteur avant et après. Deux plans : `juste` (chaque
étiquette dans sa zone correcte) et `faux` (chaque étiquette dans une zone fausse : le cas où les retours sont les
plus longs). Le navigateur est piloté par tools/measure_dnd.mjs ; tools/qa.py --render appelle ce module pour
chaque glisser-déposer.
"""
import json
import subprocess
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
LARGEURS = (400, 760)  # px : écran étroit, colonne de contenu d'une page de cours
NOMS = {"juste": "juste", "faux": "tout faux"}
MAIN_LIBRARY = "H5P.DragQuestion"


def content_of(pkg):
    """content.json d'un paquet de type H5P.DragQuestion ; None sinon (autre type, paquet illisible)."""
    try:
        with zipfile.ZipFile(pkg) as z:
            if json.loads(z.read("h5p.json")).get("mainLibrary") != MAIN_LIBRARY:
                return None
            return json.loads(z.read("content/content.json"))
    except (OSError, KeyError, ValueError, zipfile.BadZipFile):
        return None


def plans(content):
    """{nom: [(rang, zone), …]} : rang = ordre de l'étiquette déplaçable dans la page, zone = ordre de la zone de dépôt.

    `juste` : chaque étiquette dans la zone où correctElements la range (une fois par zone si elle est multiple ; un
    distracteur, sans zone juste, reste en place). `faux` : chaque étiquette dans une zone qu'elle peut recevoir mais
    où elle ne va pas (les zones fausses se répartissent à tour de rôle) ; un distracteur va dans sa première zone,
    fausse par définition.
    """
    task = content["question"]["task"]
    elements, zones = task["elements"], task["dropZones"]
    draggable = [i for i, e in enumerate(elements) if e.get("dropZones")]  # les autres éléments sont du décor
    rank = {i: r for r, i in enumerate(draggable)}
    correct = {}
    for z, zone in enumerate(zones):
        for e in zone.get("correctElements") or []:
            correct.setdefault(int(e), []).append(z)
    juste, faux, turn = [], [], 0
    for i in draggable:
        good = correct.get(i, [])
        juste += [(rank[i], z) for z in (good if elements[i].get("multiple") else good[:1])]
        wrong = [z for z in map(int, elements[i]["dropZones"]) if z < len(zones) and z not in good]
        if wrong:
            faux.append((rank[i], wrong[turn % len(wrong)]))
            turn += 1
    return {"juste": juste, "faux": faux}


def measure(pkg, env, widths=LARGEURS, shots=None):
    """Mesure un paquet ; None si ce n'est pas un glisser-déposer. Rend :
    {"initError", "runs": [{largeur, plan, attendus, deposes, avant, apres, verifie, erreur}]}.
    `env` pose H5P_RENDER_MODULES (et H5P_CHROMIUM) ; `shots`, s'il est donné, préfixe les captures d'après Vérifier."""
    content = content_of(pkg)
    if content is None:
        return None
    wanted = {name: plan for name, plan in plans(content).items() if plan} or {"juste": []}
    request = json.dumps({"widths": list(widths), "plans": wanted})
    cmd = ["node", str(ROOT / "tools" / "measure_dnd.mjs"), str(pkg), request] + ([str(shots)] if shots else [])
    timeout = 120 * len(widths) * len(wanted) + 60
    try:
        res = subprocess.run(cmd, capture_output=True, text=True, env=env, timeout=timeout)
    except (subprocess.TimeoutExpired, OSError) as e:
        return {"initError": f"mesure impossible : {e}", "runs": []}
    try:
        return json.loads(res.stdout.strip().splitlines()[-1])
    except (json.JSONDecodeError, IndexError):
        return {"initError": "mesure impossible : " + (res.stderr or res.stdout).strip()[-300:], "runs": []}


def _heights(run):
    """(avant, après) en px : hauteur de l'iframe ; None si la mesure manque."""
    return (run["avant"] or {}).get("iframe"), (run["apres"] or {}).get("iframe")


def summary(mesure):
    """Une ligne par largeur : « 760 px : avant 731 · juste 891 (+160) · tout faux 1020 (+289) »."""
    lines = []
    for width in dict.fromkeys(r["largeur"] for r in (mesure or {}).get("runs", [])):
        runs = [r for r in mesure["runs"] if r["largeur"] == width]
        before = next((b for b, _ in map(_heights, runs) if b is not None), None)
        parts = ["avant " + ("?" if before is None else str(before))]
        for r in runs:
            b, a = _heights(r)
            if a is None:
                parts.append(f"{NOMS[r['plan']]} : pas de mesure")
            else:
                parts.append(f"{NOMS[r['plan']]} {a} ({a - (b if b is not None else a):+d})")
        lines.append(f"{width} px : " + " · ".join(parts))
    return lines


def worst(mesure):
    """Plus grande hauteur après « Vérifier », en px (None si aucune)."""
    after = [a for r in (mesure or {}).get("runs", []) for a in [_heights(r)[1]] if a is not None]
    return max(after) if after else None


def problems(mesure, hauteur_max=None):
    """Raisons de ne pas se fier à la mesure ; si `hauteur_max` (px) est donné, hauteur dépassée après « Vérifier »."""
    if not mesure:
        return []
    out = [mesure["initError"]] if mesure.get("initError") else []
    for r in mesure["runs"]:
        where = f"{r['largeur']} px, {NOMS[r['plan']]}"
        if r["erreur"]:
            out.append(f"{where} : {r['erreur']}")
        elif not r["verifie"]:
            out.append(f"{where} : pas de bouton « Vérifier »")
        elif r["deposes"] < r["attendus"]:
            out.append(f"{where} : {r['deposes']} étiquette(s) déposée(s) sur {r['attendus']}, mesure incomplète")
        elif hauteur_max is not None:
            a = _heights(r)[1]
            if a is not None and a > hauteur_max:
                out.append(f"{where} : {a} px après « Vérifier », au-delà de {hauteur_max} px")
    return out
