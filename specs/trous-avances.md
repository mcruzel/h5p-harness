# Advanced Fill in the Blanks — `trous-avances`

H5P.AdvancedBlanks 1.4 · alias : trous-avances, advancedblanks, advanced-blanks · syntaxe Markdown simplifiée : oui

## Syntaxe Markdown

Comme `trous` : consigne, puis texte avec `{{réponse|variante::indice}}`. Pour un menu déroulant, ajouter des propositions fausses préfixées par `~` (retour facultatif après `>`) : le mode « sélection » est alors activé.

```markdown
Complète.

La capitale de la France est {{Paris|~Lyon>C'est la 3e ville.|~Marseille}}.
L'eau bout à {{100|cent::en degrés Celsius}} °C.
```

## Champs (bloc ```yaml, noms H5P)

`*` = obligatoire ; les autres champs ont une valeur par défaut ou sont facultatifs.

- media : groupe — Média
  - type : sous-contenu, library: image | video | audio — Type (Média à afficher au-dessus de la question (facultatif).)
  - disableImageZooming : booléen, défaut false, conditionnel — Désactiver le zoom pour l'image attachée à la question
- content : groupe — Contenu
  - task : texte riche (Markdown: a em h1 h2 h3 hr li ol strong u ul), défaut Complétez les blancs. — Consigne (Consigne indiquant à l'utilisateur comment faire l'exercice.)
  - blanksText* : texte riche (Markdown: col colgroup em figcaption figure h1 h2 h3 hr li ol s strike strong sub sup table tbody td tfoot th thead tr u ul) — Texte à trous
  - blanksList* : liste (min 1) — Paramétrage des blancs utilisés dans le texte
    chaque élément = liste (min 1) — blanc
- snippets : groupe — Fragments de feedback (groupe à un champ: écrire directement la valeur)
  - list : liste (min 0) — Liste des fragments de feedback (Les fragments de feedback sont des textes qui peuvent être réutilisés dans les textes de feedback en insérant…)
    chaque élément :
      - snippetName* : texte — Nom (Pour le nom du fragment de feedback vous ne pouvez utiliser que des lettres, des chiffres ou le trait de soul…)
      - snippetText* : texte riche (Markdown: a em li ol strong sub sup u ul) — Texte
- overallFeedback : groupe — Feedback général (groupe à un champ: écrire directement la valeur)
  - overallFeedback : liste (min 1) — Définissez des feedbacks pour différents intervalles de scores (Cliquez sur le bouton "Ajouter Intervalle" pour ajouter autant d'intervalles de score que vous souhaitez. Exe…)
    chaque élément :
      - from : nombre, min 0, max 100, défaut 0 — Intervalle de scores
      - to : nombre, min 0, max 100, défaut 100
      - feedback : texte — Feedback pour cet intervalle de scores
- behaviour : réglages — Options générales (Ces options vous permettent de paramétrer le déroulement de l'exercice.)
  mode=typing (selection|typing), selectAlternatives=alternatives (alternatives|all), randomAnswers=true, selectAlternativeRestriction=5, spellingErrorBehaviour=mistake (accept|warn|mistake), caseSensitive=false, autoCheck=false, enableSolutionsButton=true, showSolutionsRequiresInput=true, enableRetry=true, confirmCheckDialog=false, confirmRetryDialog=false

Textes d'interface pré-remplis en français (ne pas fournir sauf besoin) : showSolutions, tryAgain, checkAnswer, submitAnswer, a11yCheck, a11ySubmitAndCheck, a11yShowSolution, a11yRetry, notFilledOut, tipLabel, spellingMistakeWarning, noBlanks, confirmCheck, confirmRetry, scoreBarLabel.

## Exemple complet (validé : validateur officiel H5P + affichage)

Fichier `tests/examples/trous-avances.md` (médias dans `tests/media/`).

````markdown
---
type: trous-avances
title: Homophones a / à et et / est
language: fr
license: CC BY-SA 4.0
---
```yaml
content:
  task: Complète chaque phrase avec **a** ou **à**, **et** ou **est**.
  blanksText: |
    Léa ___ fini ses devoirs ___ elle part ___ la piscine.

    Le ciel ___ gris ce matin.
  blanksList:
    - - text: a
        isCorrect: true
        hint: "Essaie de remplacer par « avait »."
      - text: à
        optionsIncorrect:
          incorrectAnswerFeedback: "On peut dire « Léa **avait** fini » : c'est le verbe *avoir*, donc « a » sans accent."
    - - text: et
        isCorrect: true
      - text: est
        optionsIncorrect:
          incorrectAnswerFeedback: "On ne peut pas dire « Léa a fini ses devoirs **était** elle part » : il faut « et »."
    - - text: à
        isCorrect: true
      - text: a
        optionsIncorrect:
          incorrectAnswerFeedback: "On ne peut pas dire « elle part **avait** la piscine » : c'est la préposition « à »."
    - - text: est
        isCorrect: true
        hint: "Essaie de remplacer par « était »."
      - text: et
        optionsIncorrect:
          incorrectAnswerFeedback: "« Le ciel **était** gris » fonctionne : c'est le verbe *être*."
behaviour:
  mode: selection
  selectAlternatives: alternatives
overallFeedback:
  - {from: 0, to: 74, feedback: "Pense à remplacer par « avait » ou « était »."}
  - {from: 75, to: 100, feedback: "Bravo, tu maîtrises ces homophones !"}
```
````
