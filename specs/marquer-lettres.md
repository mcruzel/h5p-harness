# Mark the Letters — `marquer-lettres`

H5P.MarkTheLetters 1.1 · alias : marquer-lettres, marktheletters, mark-the-letters · syntaxe Markdown simplifiée : non (bloc ```yaml)

## Champs (bloc ```yaml, noms H5P)

`*` = obligatoire ; les autres champs ont une valeur par défaut ou sont facultatifs.

- question* : texte riche (Markdown: a em h2 h3 hr li ol strong u ul) — Question
- textField* : texte riche (Markdown: a em h2 h3 hr li ol strong u ul,) — Text
- addSolution : choix true|false, défaut true — Give solution separately
- solution : texte — Solution
- overallFeedback : groupe — Overall Feedback (groupe à un champ: écrire directement la valeur)
  - overallFeedback : liste (min 1) — Define custom feedback for any score range
    chaque élément :
      - from : nombre, min 0, max 100, défaut 0 — Score Range
      - to : nombre, min 0, max 100, défaut 100
      - feedback : texte — Feedback for defined score range
- behaviour : réglages — Behavioural settings.
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
