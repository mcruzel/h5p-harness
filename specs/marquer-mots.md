# Mark the Words — `marquer-mots`

H5P.MarkTheWords 1.11 · alias : marquer-mots, markthewords, mark-the-words · syntaxe Markdown simplifiée : oui

## Syntaxe Markdown

Premier paragraphe sans `{{…}}` = consigne ; la suite = texte où chaque mot à trouver est entouré de `{{…}}` (un seul mot par marque).

```markdown
Clique sur tous les verbes.

Le chat {{dort}} pendant que le chien {{court}} dans le jardin.
```

## Champs (bloc ```yaml, noms H5P)

`*` = obligatoire ; les autres champs ont une valeur par défaut ou sont facultatifs.

- media : groupe — Média
  - type : sous-contenu, library: image | video | audio — Type
  - disableImageZooming : booléen, défaut false, conditionnel — Désactiver le zoom sur image pour l'image de la question
- taskDescription* : texte riche (Markdown: a code em h2 h3 hr li ol pre strong u ul) — Description de la tâche
- textField* : texte riche (Markdown: code em strong) — Champ de texte
- overallFeedback : groupe — Feedback général (groupe à un champ: écrire directement la valeur)
  - overallFeedback : liste (min 1) — Définissez le feedback pour chaque intervalle de score
    chaque élément :
      - from : nombre, min 0, max 100, défaut 0 — Intervalle de score
      - to : nombre, min 0, max 100, défaut 100
      - feedback : texte — Feedback pour l'intervalle de score défini
- behaviour : réglages — Options générales
  enableRetry=true, enableSolutionsButton=true, showScorePoints=true

Textes d'interface pré-remplis en français (ne pas fournir sauf besoin) : checkAnswerButton, submitAnswerButton, tryAgainButton, showSolutionButton, correctAnswer, incorrectAnswer, missedAnswer, displaySolutionDescription, scoreBarLabel, a11yFullTextLabel, a11yClickableTextLabel, a11ySolutionModeHeader, a11yCheckingHeader, a11yCheck, a11yShowSolution, a11yRetry.
