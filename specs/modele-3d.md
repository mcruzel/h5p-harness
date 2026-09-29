# 3D Model — `modele-3d`

H5P.ThreeDModel 1.0 · alias : modele-3d, threedmodel, three-d-model · syntaxe Markdown simplifiée : non (bloc ```yaml)

## Champs (bloc ```yaml, noms H5P)

`*` = obligatoire ; les autres champs ont une valeur par défaut ou sont facultatifs.

- model : groupe — Model
  - file : fichier (chemin ou URL) — 3D model file
  - alt* : texte — Alternative text
- annotations : groupe — Annotations
  - annotations* : liste (min 1) — Annotations
    chaque élément :
      - text : texte — Text
- visuals : groupe — Visual settings
  - backgroundImage : image (chemin ou URL) — Background image
  - backgroundColor : couleur #rrggbb, défaut rgba(255, 255, 255, 1) — Background color
  - poster : image (chemin ou URL) — Poster image
- size : groupe — Size settings
  - maxWidth : texte — Maximum width
  - minHeight : texte — Minimum height
  - maxHeight : texte — Maximum height

Textes d'interface pré-remplis en français (ne pas fournir sauf besoin) : l10n, a11y.

## Exemple complet (validé : validateur officiel H5P + affichage)

Fichier `tests/examples/modele-3d.md` (médias dans `tests/media/`).

````markdown
---
type: modele-3d
title: Le cristal de sel (halite)
language: fr
preset: decouverte
license: CC BY-SA 4.0
authors: Équipe de physique-chimie
---
```yaml
model:
  file: ../media/modele-3d-cristal.glb
  alt: Modèle 3D d'un cristal de sel gemme de forme cubique
annotations:
  annotations:
    # « surface » (champ caché, non documenté dans la fiche) : sans lui l'annotation n'est pas affichée.
    # Format model-viewer : n° de nœud, n° de primitive, 3 indices de sommets, 3 coordonnées barycentriques.
    - text: Face carrée du cristal
      surface: "0 0 16 17 18 0.4 0.3 0.3"
    - text: Arête entre deux faces
      surface: "0 0 8 9 10 0.1 0.45 0.45"
visuals:
  backgroundColor: "#f4f1e8"
```
````
