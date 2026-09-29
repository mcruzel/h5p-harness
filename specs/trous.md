# Fill in the Blanks — `trous`

H5P.Blanks 1.14 · alias : trous, texte-a-trous, blanks · syntaxe Markdown simplifiée : oui

## Syntaxe Markdown

Premier(s) paragraphe(s) sans trou = consigne. Chaque paragraphe suivant = un bloc de texte à trous. Un trou : `{{réponse}}`, variantes acceptées `{{réponse|variante}}`, indice `{{réponse::indice}}`. Les caractères `*`, `/` et `:` sont interdits dans les réponses (syntaxe H5P, sans échappement) ; pour l'italique utiliser `_texte_`.

```markdown
Complète les phrases.

La photosynthèse produit du {{dioxygène|oxygène}} et du {{glucose::un sucre}}.

L'ADN se trouve dans le {{noyau}}.
```

## Champs (bloc ```yaml, noms H5P)

`*` = obligatoire ; les autres champs ont une valeur par défaut ou sont facultatifs.

- media : groupe — Média
  - type : sous-contenu, library: image | video | audio — Type
  - disableImageZooming : booléen, défaut false, conditionnel — Désactiver l'agrandissement de l'image
- text : texte riche (Markdown: a code em h2 h3 hr li ol pre strong u ul), défaut Complétez les mots manquants — Description de la tâche
- questions* : liste (min 1, max 31) — Blocs de texte
  chaque élément = texte riche (Markdown: code del em s strong u) — Ligne de texte
- overallFeedback : groupe — Retour général (groupe à un champ: écrire directement la valeur)
  - overallFeedback : liste (min 1) — Définissez des feedbacks pour différents intervalles de scores
    chaque élément :
      - from : nombre, min 0, max 100, défaut 0 — Fourchette de score
      - to : nombre, min 0, max 100, défaut 100
      - feedback : texte — Retour pour cet intervalle de score
- behaviour : réglages — Options générales
  enableRetry=true, allowRetryIfCorrect=false, enableSolutionsButton=true, autoCheck=false, caseSensitive=true, showSolutionsRequiresInput=true, separateLines=false, confirmCheckDialog=false, confirmRetryDialog=false, acceptSpellingErrors=false

Textes d'interface pré-remplis en français (ne pas fournir sauf besoin) : showSolutions, tryAgain, checkAnswer, submitAnswer, notFilledOut, answerIsCorrect, answerIsWrong, answeredCorrectly, answeredIncorrectly, solutionLabel, inputLabel, inputHasTipLabel, tipLabel, confirmCheck, confirmRetry, scoreBarLabel, a11yCheck, a11yShowSolution, a11yRetry, a11yCheckingModeHeader.
