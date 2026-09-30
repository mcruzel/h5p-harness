# 3D Model — `modele-3d`

H5P.ThreeDModel 1.0 · alias : modele-3d, threedmodel, three-d-model · syntaxe Markdown simplifiée : non (bloc ```yaml)

## Points d'attention

- Modèle au format `.glb` / `.gltf`.
- Une annotation n'est affichée que si elle a une `surface` (position sur le modèle) en plus de son `text` ; sans elle, le harnais émet un avertissement.

## Champs (bloc ```yaml, noms H5P)

`*` = obligatoire ; les autres champs ont une valeur par défaut ou sont facultatifs. Libellés et descriptions : ceux de la bibliothèque (anglais) ; valeurs par défaut : en français.

- model : groupe — Model
  - file : fichier (chemin ou URL) — 3D model file (Upload a glTF (.glb / .gltf) file here. The preferred format is "glTF 2.0 binary" in a single file.)
  - alt* : texte — Alternative text (Alternative text for screen readers.)
- annotations : groupe — Annotations
  - annotations* : liste (min 1) — Annotations (Add annotation labels to the 3D model by typing their their text and using the adjacent button.)
    chaque élément :
      - text : texte — Text
- visuals : groupe — Visual settings
  - backgroundImage : image (chemin ou URL) — Background image (Optional image that will be used for the background.)
  - backgroundColor : couleur #rrggbb, défaut rgba(255, 255, 255, 1) — Background color
  - poster : image (chemin ou URL) — Poster image (Optional image that will be shown before the 3D model is loaded. This can be used to show a preview of the 3D model that is large and may need some time to load. Note that it makes only sense to add a poster image if th…)
- size : groupe — Size settings
  - maxWidth : texte — Maximum width (H5P will usually scale content to full width. Set a maximum width here in CSS units (px, rem, etc.). Please note that this will not influence the maximum width of the H5P content as a whole.)
  - minHeight : texte — Minimum height (H5P will usually determine the height based on the width. Change the minimum height here in CSS units (px, rem, etc.) in case the model is displayes too small for your liking.)
  - maxHeight : texte — Maximum height (H5P will usually determine the height based on the width. Set a maximum height here in CSS units (px, rem, etc.). Please note that this will not influence the maximum height of the H5P content as a whole.)

Textes d'interface pré-remplis en français (ne pas fournir sauf besoin) : l10n, a11y.

## Exemple complet (validé : validateur officiel H5P + affichage)

Fichier `sources/exemples/modele-3d.md` (médias dans `sources/exemples/media/`).

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
  file: media/modele-3d-cristal.glb
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
