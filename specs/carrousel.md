# Image Slider — `carrousel`

H5P.ImageSlider 1.1 · alias : carrousel, imageslider, image-slider · syntaxe Markdown simplifiée : oui

## Syntaxe Markdown

Une image par ligne : `- ![description](image)` (au moins 2).

## Champs (bloc ```yaml, noms H5P)

`*` = obligatoire ; les autres champs ont une valeur par défaut ou sont facultatifs. Libellés et descriptions : ceux de la bibliothèque (anglais) ; valeurs par défaut : en français.

- imageSlides : liste — Images
  chaque élément = sous-contenu, library: imageslide — Image Slide
- aspectRatioMode : choix auto|custom|notFixed, défaut auto — Aspect ratio (Automatic means fixed aspect ratio automatically determined based on the images)
- aspectRatio : réglages — Aspect Ratio Settings
  aspectWidth=4, aspectHeight=3

Textes d'interface pré-remplis en français (ne pas fournir sauf besoin) : a11y.

## Exemple complet (validé : validateur officiel H5P + affichage)

Fichier `sources/exemples/carrousel.md` (médias dans `sources/exemples/media/`).

````markdown
---
type: carrousel
title: Les paysages de France
language: fr
preset: decouverte
license: CC BY 4.0
authors: Professeur d'histoire-géographie
---
- ![Un paysage de campagne vallonnée](media/paysage.jpg)
- ![Le même quartier avant sa rénovation urbaine](media/avant.jpg)
- ![Le même quartier après sa rénovation urbaine](media/apres.jpg)
- ![Vue panoramique d'un site naturel](media/panorama.jpg)

```yaml
aspectRatioMode: custom
aspectRatio: {aspectWidth: 3, aspectHeight: 2}
```
````
