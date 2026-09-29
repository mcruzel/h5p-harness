# Image Juxtaposition — `avant-apres`

H5P.ImageJuxtaposition 1.6 · alias : avant-apres, imagejuxtaposition, image-juxtaposition · syntaxe Markdown simplifiée : oui

## Syntaxe Markdown

Consigne facultative, puis deux lignes d'image : `![Avant](image1)` puis `![Après](image2)` (le texte alternatif sert aussi d'étiquette). Images de même taille.

## Champs (bloc ```yaml, noms H5P)

`*` = obligatoire ; les autres champs ont une valeur par défaut ou sont facultatifs.

- taskDescription : texte riche (Markdown: a code em h2 h3 hr li ol pre strong u ul) — Consigne (Put the heading/instructions you'd like to show above the before/after image here.)
- imageBefore : groupe — Première image
  - imageBefore* : sous-contenu, library: image — Première image (La première image. Assurez-vous qu'elle a les mêmes dimensions que la deuxième image.)
  - labelBefore : texte — Label pour la première image (Label à afficher au dessus de la première image.)
- imageAfter : groupe — Deuxième image
  - imageAfter* : sous-contenu, library: image — Deuxième image (La deuxième image. Assurez-vous qu'elle a les mêmes dimensions que la première image.)
  - labelAfter : texte — Label pour la deuxième image (Label à afficher au dessus de la deuxième image.)
- behavior : réglages — Paramètres de comportement (Position de démarrage du curseur en %)
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
