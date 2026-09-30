# Image Juxtaposition — `avant-apres`

H5P.ImageJuxtaposition 1.6 · alias : avant-apres, imagejuxtaposition, image-juxtaposition · syntaxe Markdown simplifiée : oui

## Syntaxe Markdown

Consigne facultative, puis deux lignes d'image : `![Avant](image1)` puis `![Après](image2)` (le texte alternatif sert aussi d'étiquette). Images de même taille.

## Champs (bloc ```yaml, noms H5P)

`*` = obligatoire ; les autres champs ont une valeur par défaut ou sont facultatifs. Libellés et descriptions : ceux de la bibliothèque (anglais) ; valeurs par défaut : en français.

- taskDescription : texte riche (Markdown: a code em h2 h3 hr li ol pre strong u ul) — Task description (Put the heading/instructions you'd like to show above the before/after image here.)
- imageBefore : groupe — First image
  - imageBefore* : sous-contenu, library: image — First image (The first image. Please make sure that it has the same size as the second image.)
  - labelBefore : texte — Label for first image (Label to put over first image)
- imageAfter : groupe — Second image
  - imageAfter* : sous-contenu, library: image — Second image (The second image. Please make sure that it has the same size as the first image.)
  - labelAfter : texte — Label for second image (Label to put over second image)
- behavior : réglages — Behavioral settings (These options will let you set some details)
  startingPosition=50, sliderOrientation=horizontal (horizontal|vertical), sliderColor=#f3f3f3

Textes d'interface pré-remplis en français (ne pas fournir sauf besoin) : a11y.

## Exemple complet (validé : validateur officiel H5P + affichage)

Fichier `tests/examples/avant-apres.md` (médias dans `tests/media/`).

````markdown
---
type: avant-apres
title: La rénovation d'un quartier
language: fr
preset: decouverte
license: CC BY-SA 4.0
authors: Équipe d'histoire-géographie
---
Fais glisser le curseur pour comparer le quartier **avant** et **après** sa rénovation.

- Quels bâtiments ont disparu ?
- Quels nouveaux aménagements repères-tu ?

![Avant (1990)](../media/avant.jpg)
![Après (2020)](../media/apres.jpg)

```yaml
behavior:
  startingPosition: 40
  sliderColor: "#ffcc00"
```
````
