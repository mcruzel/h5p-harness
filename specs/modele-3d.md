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
