# Agamotto — `agamotto`

H5P.Agamotto 1.7 · alias : agamotto · syntaxe Markdown simplifiée : oui

## Syntaxe Markdown

`# Titre` facultatif, puis une étape par section `## Libellé`, contenant une image `![description](image)` et une description Markdown facultative. Au moins 2 étapes (images de même taille de préférence).

## Champs (bloc ```yaml, noms H5P)

`*` = obligatoire ; les autres champs ont une valeur par défaut ou sont facultatifs.

- title : texte — Rubrique
- items* : liste (min 2, max 50) — Éléments
  chaque élément :
    - image* : sous-contenu, library: image — Image
    - labelText : texte — Vignette
    - description : texte riche (Markdown: a code em h3 h4 li ol pre strong sub sup ul) — Description
    - audio : audio (chemin ou URL) — Audio
- behaviour : réglages — Paramètres comportementaux
  startImage=1, snap=true, ticks=false, labels=false, transparencyReplacementColor=#000000, imagesDescriptionsRatio=70

Textes d'interface pré-remplis en français (ne pas fournir sauf besoin) : a11y.
