# Image Juxtaposition — `avant-apres`

H5P.ImageJuxtaposition 1.6 · alias : avant-apres, imagejuxtaposition, image-juxtaposition · syntaxe Markdown simplifiée : oui

## Syntaxe Markdown

Consigne facultative, puis deux lignes d'image : `![Avant](image1)` puis `![Après](image2)` (le texte alternatif sert aussi d'étiquette). Images de même taille.

## Champs (bloc ```yaml, noms H5P)

`*` = obligatoire ; les autres champs ont une valeur par défaut ou sont facultatifs.

- taskDescription : texte riche (Markdown: a code em h2 h3 hr li ol pre strong u ul) — Consigne
- imageBefore : groupe — Première image
  - imageBefore* : sous-contenu, library: image — Première image
  - labelBefore : texte — Label pour la première image
- imageAfter : groupe — Deuxième image
  - imageAfter* : sous-contenu, library: image — Deuxième image
  - labelAfter : texte — Label pour la deuxième image
- behavior : réglages — Paramètres de comportement
  startingPosition=50, sliderOrientation=horizontal (horizontal|vertical), sliderColor=#f3f3f3

Textes d'interface pré-remplis en français (ne pas fournir sauf besoin) : a11y.
