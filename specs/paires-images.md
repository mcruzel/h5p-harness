# Image Pair — `paires-images`

H5P.ImagePair 1.4 · alias : paires-images, imagepair, image-pair · syntaxe Markdown simplifiée : non (bloc ```yaml)

## Champs (bloc ```yaml, noms H5P)

`*` = obligatoire ; les autres champs ont une valeur par défaut ou sont facultatifs.

- taskDescription : texte, défaut Drag images from the left to … — Task Description
- cards* : liste (min 2, max 100) — Cards
  chaque élément :
    - image : image (chemin ou URL) — Image
    - imageAlt* : texte — Alternative text for Image
    - match : image (chemin ou URL) — Matching Image
    - matchAlt : texte — Alternative text for Matching Image
- behaviour : réglages — Behavioural settings
  allowRetry=true

Textes d'interface pré-remplis en français (ne pas fournir sauf besoin) : l10n.
