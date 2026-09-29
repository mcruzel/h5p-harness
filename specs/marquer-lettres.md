# Mark the Letters — `marquer-lettres`

H5P.MarkTheLetters 1.1 · alias : marquer-lettres, marktheletters, mark-the-letters · syntaxe Markdown simplifiée : non (bloc ```yaml)

## Points d'attention

- Dans `textField`, entourer chaque lettre à trouver : `*t*` (ou `{{t}}`), ex. `Le cha*t* dor*t*.`.
- La bibliothèque ne garde que les lettres a-z : les lettres accentuées disparaissent (avertissement du harnais).

## Champs (bloc ```yaml, noms H5P)

`*` = obligatoire ; les autres champs ont une valeur par défaut ou sont facultatifs.

- question* : texte riche (Markdown: a em h2 h3 hr li ol strong u ul) — Question (Describe how the user should solve the task.)
- textField* : texte riche (Markdown: a em h2 h3 hr li ol strong u ul,) — Text (Correct letters are marked with asterisks (*) before and after the letter.)
- addSolution : choix true|false, défaut true — Give solution separately
- solution : texte — Solution (Enter the correct solution here if you need to take all occurance of the specific letter as answer.)
- overallFeedback : groupe — Overall Feedback (groupe à un champ: écrire directement la valeur)
  - overallFeedback : liste (min 1) — Define custom feedback for any score range (Click the "Add range" button to add as many ranges as you need. Example: 0-20% Bad score, 21-91% Average Scor…)
    chaque élément :
      - from : nombre, min 0, max 100, défaut 0 — Score Range
      - to : nombre, min 0, max 100, défaut 100
      - feedback : texte — Feedback for defined score range
- behaviour : réglages — Behavioural settings. (These options will let you control how the task behaves.)
  enableRetry=true, enableSolutionsButton=true, showScorePoints=true

Textes d'interface pré-remplis en français (ne pas fournir sauf besoin) : checkAnswerButton, tryAgainButton, showSolutionButton, correctAnswer, incorrectAnswer, missedAnswer, displaySolutionDescription, scoreBarLabel.

## Exemple complet (validé : validateur officiel H5P + affichage)

Fichier `tests/examples/marquer-lettres.md` (médias dans `tests/media/`).

````markdown
---
type: marquer-lettres
title: Les lettres muettes en fin de mot
language: fr
preset: entrainement
license: CC BY-SA 4.0
authors: Équipe de lettres
---
```yaml
question: Clique sur les **lettres muettes** à la fin des mots.
textField: Le cha\*t\* de mon voisin dor\*t\* dan\*s\* le jardin.
addSolution: "false"
solution: ""
overallFeedback:
  - {from: 0, to: 99, feedback: Relis chaque mot à voix haute pour repérer les lettres que l'on n'entend pas.}
  - {from: 100, to: 100, feedback: Bravo !}
```
````
