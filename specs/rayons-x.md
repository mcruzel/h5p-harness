# X-Ray — `rayons-x`

H5P.XRay 0.1 · alias : rayons-x, xray, x-ray · syntaxe Markdown simplifiée : non (bloc ```yaml)

## Points d'attention

- `imageForeground` = image visible ; `imageBackground` = image révélée sous la loupe (mêmes dimensions).
- `xRayLensWidth` / `xRayLensHeight` sont des **textes avec unité** : `"30%"` ou `"160px"` (un nombre seul est lu en pixels).

## Champs (bloc ```yaml, noms H5P)

`*` = obligatoire ; les autres champs ont une valeur par défaut ou sont facultatifs. Libellés et descriptions : ceux de la bibliothèque (anglais) ; valeurs par défaut : en français.

- imageBackground* : sous-contenu, library: image — Image (Image to be used in the background.)
- imageForeground* : sous-contenu, library: image — Image (Image to be used in the foreground.)
- visual : réglages — Visual settings (These options will let you control visual aspects.)
  imageWidth=100% (35%|50%|75%|100%|natural), imageAlignment=center (flex-start|center|flex-end), xRayLensWidth=20 %, xRayLensHeight=25 %, darkenImageOnXRay=true
- behaviour : réglages — Behavioural settings (These options will let you control how the task behaves.)
  autoXRay=true, hideXRayIndicator=false

Textes d'interface pré-remplis en français (ne pas fournir sauf besoin) : a11y.

## Exemple complet (validé : validateur officiel H5P + affichage)

Fichier `sources/exemples/rayons-x.md` (médias dans `sources/exemples/media/`).

````markdown
---
type: rayons-x
title: Sous le quartier rénové, l'ancien quartier
language: fr
preset: decouverte
license: CC BY-SA 4.0
authors: Équipe d'histoire-géographie
---
```yaml
imageForeground:   # image affichée
  library: image
  file: media/apres.jpg
  alt: Le quartier aujourd'hui, après sa rénovation
imageBackground:   # image révélée sous la loupe
  library: image
  file: media/avant.jpg
  alt: Le même quartier avant sa rénovation
visual:
  imageWidth: 75%
  xRayLensWidth: 30%
  xRayLensHeight: 35%
behaviour:
  autoXRay: true
```
````
