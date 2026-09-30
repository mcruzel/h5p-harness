# Collage — `collage`

H5P.Collage 0.3 · alias : collage · syntaxe Markdown simplifiée : non (bloc ```yaml)

## Points d'attention

- `template` = nombre d'images par rangée séparé par des tirets (`"2-1"` : 2 images puis 1) ; fournir autant de `clips` que la somme (avertissement sinon).
- `offset` décale l'image dans son cadre, `scale` l'agrandit (1 = taille ajustée).

## Champs (bloc ```yaml, noms H5P)

`*` = obligatoire ; les autres champs ont une valeur par défaut ou sont facultatifs. Libellés et descriptions : ceux de la bibliothèque (anglais) ; valeurs par défaut : en français.

- collage : groupe — Preview (You can move(pan) the images around by dragging them. You can also select an image and then use the + or - keys on your keyboard to zoom or simply hold down the Z key while moving your mouse wheel.)
  - template : choix 1|1-1|2|2-1|1-2|2-2|3-1|1-3|2-3|3-2|…, défaut 2-1 — Layout
  - options : réglages — Display options
    heightRatio=0.75, spacing=0.5, frame=true
  - clips* : liste (min 1) — Clips
    chaque élément :
      - image : image (chemin ou URL) — Image
      - offset : réglages — Offset
        top=0, left=0
      - alt* : texte — Alternative text (Required. If the browser can't load the image this text will be displayed instead. Also used by readspeakers.)
      - title : texte — Hover text (Optional. This text is displayed when the user hovers his pointing device over the image.)
      - scale : nombre, min 0.01, défaut 1 — Scale

## Exemple complet (validé : validateur officiel H5P + affichage)

Fichier `sources/exemples/collage.md` (médias dans `sources/exemples/media/`).

````markdown
---
type: collage
title: Un quartier qui change
language: fr
preset: decouverte
license: CC BY-SA 4.0
authors: Équipe d'histoire-géographie
---
```yaml
collage:
  template: 1-2
  options: {heightRatio: 0.6, spacing: 0.5, frame: true}
  clips:
    - image: media/paysage.jpg
      alt: Le paysage rural d'origine, avec une maison et un arbre
      title: Le site en 1950
    - image: media/avant.jpg
      alt: Le quartier avant sa rénovation
      title: Le quartier en 1990
    - image: media/apres.jpg
      alt: Le quartier après sa rénovation
      title: Le quartier en 2020
      scale: 1.2
      offset: {top: -10, left: -5}
```
````
