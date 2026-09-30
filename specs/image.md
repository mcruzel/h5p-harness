# Image — `image`

H5P.Image 1.1 · alias : image · syntaxe Markdown simplifiée : oui

## Syntaxe Markdown

Une seule ligne `![description](image ou URL "titre au survol")`. Description vide = image décorative.

## Champs (bloc ```yaml, noms H5P)

`*` = obligatoire ; les autres champs ont une valeur par défaut ou sont facultatifs. Libellés et descriptions : ceux de la bibliothèque (anglais) ; valeurs par défaut : en français.

- file* : image (chemin ou URL) — Image
- decorative : booléen, défaut false — Decorative only (Enable this option if the image is purely decorative and does not add any information to the content on the page. It will be ignored by screen readers and not given any alternative text.)
- alt : texte, si decorative = False — Alternative text (Required. If the browser can't load the image this text will be displayed instead. Also used by "text-to-speech" readers.)
- title : texte — Hover text (Optional. This text is displayed when the users hover their pointing device over the image.)

Textes d'interface pré-remplis en français (ne pas fournir sauf besoin) : contentName, expandImage, minimizeImage.
