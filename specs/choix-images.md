# Multimedia Choice — `choix-images`

H5P.MultiMediaChoice 0.3 · alias : choix-images, multimediachoice, multi-media-choice · syntaxe Markdown simplifiée : oui

## Syntaxe Markdown

Question en Markdown, puis une option par ligne : `- [x] ![description](image)` (bonne) ou `- [ ] ![description](image)` ; plusieurs `[x]` = plusieurs bonnes réponses.

## Champs (bloc ```yaml, noms H5P)

`*` = obligatoire ; les autres champs ont une valeur par défaut ou sont facultatifs. Libellés et descriptions : ceux de la bibliothèque (anglais) ; valeurs par défaut : en français.

- media : groupe — Media
  - type : sous-contenu, library: image | video | audio — Type (Optional media to display above the question.)
  - disableImageZooming : booléen, défaut false, si type = H5P.Image — Disable image zooming
- question* : texte riche (Markdown: code em h2 h3 pre strong sub sup) — Question
- options* : liste (min 2, max 20) — Available options
  chaque élément :
    - media* : sous-contenu, library: image | video | audio — Media (Media to display as a choice.)
    - poster : image (chemin ou URL), si media = H5P.Audio — Poster image
    - correct : booléen — Correct
- overallFeedback : groupe — Overall Feedback (groupe à un champ: écrire directement la valeur)
  - overallFeedback : liste (min 1) — Define custom feedback for any score range (Click the "Add range" button to add as many ranges as you need. Example: 0-20% Bad score, 21-91% Average Score, 91-100% Great Score!)
    chaque élément :
      - from : nombre, min 0, max 100, défaut 0 — Score Range
      - to : nombre, min 0, max 100, défaut 100
      - feedback : texte — Feedback for defined score range
- behaviour : réglages — Behavioural settings (These options will let you control how the task behaves.)
  enableRetry=true, enableSolutionsButton=true, confirmCheckDialog=false, confirmRetryDialog=false, singlePoint=false, showSolutionsRequiresInput=true, questionType=auto (auto|multi|single), aspectRatio=auto (auto|16to9|4to3|3to2|1to1), maxAlternativesPerRow=4 (1|2|3|4), passPercentage=100

Textes d'interface pré-remplis en français (ne pas fournir sauf besoin) : l10n.

## Exemple complet (validé : validateur officiel H5P + affichage)

Fichier `tests/examples/choix-images.md` (médias dans `tests/media/`).

````markdown
---
type: choix-images
title: Reconnaître les quadrilatères
language: fr
preset: entrainement
license: CC BY-SA 4.0
authors: Équipe de mathématiques
---
Sélectionne **toutes** les figures qui sont des **quadrilatères**.

- [x] ![Un carré rouge](../media/carre-rouge.png)
- [x] ![Un losange violet](../media/losange-violet.png)
- [ ] ![Un triangle vert](../media/triangle-vert.png)
- [ ] ![Un hexagone gris](../media/hexagone-gris.png)
- [ ] ![Un cercle bleu](../media/cercle-bleu.png)

```yaml
overallFeedback:
  - {from: 0, to: 49, feedback: Relis la définition d'un quadrilatère (polygone à 4 côtés).}
  - {from: 50, to: 99, feedback: "Presque : il manque une figure ou une figure est en trop."}
  - {from: 100, to: 100, feedback: Parfait !}
behaviour:
  aspectRatio: 4to3
  maxAlternativesPerRow: 3
```
````
