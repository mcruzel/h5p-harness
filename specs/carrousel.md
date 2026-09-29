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

## Exemple complet (validé : validateur officiel H5P + affichage)

Fichier `tests/examples/carrousel.md` (médias dans `tests/media/`).

````markdown
---
type: carrousel
title: Les paysages de France
language: fr
preset: decouverte
license: CC BY 4.0
authors: Professeur d'histoire-géographie
---
- ![Un paysage de campagne vallonnée](../media/paysage.jpg)
- ![Le même quartier avant sa rénovation urbaine](../media/avant.jpg)
- ![Le même quartier après sa rénovation urbaine](../media/apres.jpg)
- ![Vue panoramique d'un site naturel](../media/panorama.jpg)

```yaml
aspectRatioMode: custom
aspectRatio: {aspectWidth: 3, aspectHeight: 2}
```
````
