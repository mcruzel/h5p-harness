# Drag the Words — `glisser-mots`

H5P.DragText 1.10 · alias : glisser-mots, dragtext, drag-text · syntaxe Markdown simplifiée : oui

## Syntaxe Markdown

Premier paragraphe sans `{{…}}` = consigne ; la suite = texte dans lequel chaque `{{mot}}` devient une case où glisser le mot (`{{mot::indice}}` pour un indice ; une seule réponse par case). Mots pièges : une ligne `Distracteurs: mot1, mot2`.

```markdown
Glisse les capitales au bon endroit.

{{Paris}} est la capitale de la France et {{Rome}} celle de l'Italie.
Distracteurs: Lyon, Milan
```

## Champs (bloc ```yaml, noms H5P)

`*` = obligatoire ; les autres champs ont une valeur par défaut ou sont facultatifs. Libellés et descriptions : ceux de la bibliothèque (anglais) ; valeurs par défaut : en français.

- media : groupe — Media
  - type : sous-contenu, library: image | video | audio — Type (Optional media to display above the question.)
  - disableImageZooming : booléen, défaut false, si type = H5P.Image — Disable image zooming
- taskDescription : texte riche (Markdown: a code em h2 h3 hr li ol pre strong u ul), défaut Déplacez les textes dans les … — Task description (Describe how the user should solve the task.)
- textField* : texte multiligne — Text
- distractors : texte — Distractors (Enter extra solutions that are wrong as distractors. Use the same asterisk (*) scheme as for the text.)
- overallFeedback : groupe — Overall Feedback (groupe à un champ: écrire directement la valeur)
  - overallFeedback : liste (min 1) — Define custom feedback for any score range (Click the "Add range" button to add as many ranges as you need. Example: 0-20% Bad score, 21-91% Average Score, 91-100% Great Score!)
    chaque élément :
      - from : nombre, min 0, max 100, défaut 0 — Score Range
      - to : nombre, min 0, max 100, défaut 100
      - feedback : texte — Feedback for defined score range
- behaviour : réglages — Behavioural settings. (These options will let you control how the task behaves.)
  enableRetry=true, enableSolutionsButton=true, instantFeedback=false

Textes d'interface pré-remplis en français (ne pas fournir sauf besoin) : checkAnswer, submitAnswer, tryAgain, showSolution, dropZoneIndex, empty, contains, ariaDraggableIndex, tipLabel, correctText, incorrectText, resetDropTitle, resetDropDescription, grabbed, cancelledDragging, correctAnswer, feedbackHeader, scoreBarLabel, a11yCheck, a11yShowSolution, a11yRetry.

## Exemple complet (validé : validateur officiel H5P + affichage)

Fichier `sources/exemples/glisser-mots.md` (médias dans `sources/exemples/media/`).

```markdown
---
type: glisser-mots
title: La cellule – vocabulaire
language: fr
license: CC BY-SA 4.0
---
Fais glisser chaque mot à la bonne place dans le texte.

La cellule est l'unité de base du {{vivant}}. Elle est délimitée par une {{membrane::elle sépare l'intérieur de l'extérieur}}.
Chez les végétaux, on trouve en plus une {{paroi}} et des {{chloroplastes}}.
Le {{noyau}} contient l'information génétique.
Distracteurs: mitochondrie, vacuole
```
