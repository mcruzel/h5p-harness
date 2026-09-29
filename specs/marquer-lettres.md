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
