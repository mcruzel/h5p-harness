# Image Slider — `carrousel`

H5P.ImageSlider 1.1 · alias : carrousel, imageslider, image-slider · syntaxe Markdown simplifiée : oui

## Syntaxe Markdown

Une image par ligne : `- ![description](image)` (au moins 2).

## Champs (bloc ```yaml, noms H5P)

`*` = obligatoire ; les autres champs ont une valeur par défaut ou sont facultatifs.

- imageSlides : liste — Images
  chaque élément = sous-contenu, library: imageslide — Diapositive
- aspectRatioMode : choix auto|custom|notFixed, défaut auto — Ratio de l'affichage
- aspectRatio : réglages — Paramétrages du ratio de l'affichage
  aspectWidth=4, aspectHeight=3

Textes d'interface pré-remplis en français (ne pas fournir sauf besoin) : a11y.
