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

`*` = obligatoire ; les autres champs ont une valeur par défaut ou sont facultatifs.

- media : groupe — Média
  - type : sous-contenu, library: image | video | audio — Type
  - disableImageZooming : booléen, défaut false, conditionnel — Désactiver le zoom sur image pour l'image de la question
- taskDescription : texte riche (Markdown: a code em h2 h3 hr li ol pre strong u ul), défaut Déplacez les textes dans les … — Description de la tâche
- textField* : texte multiligne — Question
- distractors : texte — Distractors
- overallFeedback : groupe — Feedback général (groupe à un champ: écrire directement la valeur)
  - overallFeedback : liste (min 1) — Définissez le feedback pour chaque intervalle de scores
    chaque élément :
      - from : nombre, min 0, max 100, défaut 0 — Intervalle de score
      - to : nombre, min 0, max 100, défaut 100
      - feedback : texte — Feedback pour un intervalle de score défini
- behaviour : réglages — Options générales.
  enableRetry=true, enableSolutionsButton=true, instantFeedback=false

Textes d'interface pré-remplis en français (ne pas fournir sauf besoin) : checkAnswer, submitAnswer, tryAgain, showSolution, dropZoneIndex, empty, contains, ariaDraggableIndex, tipLabel, correctText, incorrectText, resetDropTitle, resetDropDescription, grabbed, cancelledDragging, correctAnswer, feedbackHeader, scoreBarLabel, a11yCheck, a11yShowSolution, a11yRetry.
