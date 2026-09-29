# Advanced Fill in the Blanks — `trous-avances`

H5P.AdvancedBlanks 1.4 · alias : trous-avances, advancedblanks, advanced-blanks · syntaxe Markdown simplifiée : non (bloc ```yaml)

## Champs (bloc ```yaml, noms H5P)

`*` = obligatoire ; les autres champs ont une valeur par défaut ou sont facultatifs.

- media : groupe — Média
  - type : sous-contenu, library: image | video | audio — Type
  - disableImageZooming : booléen, défaut false, conditionnel — Désactiver le zoom pour l'image attachée à la question
- content : groupe — Contenu
  - task : texte riche (Markdown: a em h1 h2 h3 hr li ol strong u ul), défaut Complétez les blancs. — Consigne
  - blanksText* : texte riche (Markdown: col colgroup em figcaption figure h1 h2 h3 hr li ol s strike strong sub sup table tbody td tfoot th thead tr u ul) — Texte à trous
  - blanksList* : liste (min 1) — Paramétrage des blancs utilisés dans le texte
    chaque élément = liste (min 1) — blanc
- snippets : groupe — Fragments de feedback (groupe à un champ: écrire directement la valeur)
  - list : liste (min 0) — Liste des fragments de feedback
    chaque élément :
      - snippetName* : texte — Nom
      - snippetText* : texte riche (Markdown: a em li ol strong sub sup u ul) — Texte
- overallFeedback : groupe — Feedback général (groupe à un champ: écrire directement la valeur)
  - overallFeedback : liste (min 1) — Définissez des feedbacks pour différents intervalles de scores
    chaque élément :
      - from : nombre, min 0, max 100, défaut 0 — Intervalle de scores
      - to : nombre, min 0, max 100, défaut 100
      - feedback : texte — Feedback pour cet intervalle de scores
- behaviour : réglages — Options générales
  mode=typing (selection|typing), selectAlternatives=alternatives (alternatives|all), randomAnswers=true, selectAlternativeRestriction=5, spellingErrorBehaviour=mistake (accept|warn|mistake), caseSensitive=false, autoCheck=false, enableSolutionsButton=true, showSolutionsRequiresInput=true, enableRetry=true, confirmCheckDialog=false, confirmRetryDialog=false

Textes d'interface pré-remplis en français (ne pas fournir sauf besoin) : showSolutions, tryAgain, checkAnswer, submitAnswer, a11yCheck, a11ySubmitAndCheck, a11yShowSolution, a11yRetry, notFilledOut, tipLabel, spellingMistakeWarning, noBlanks, confirmCheck, confirmRetry, scoreBarLabel.
