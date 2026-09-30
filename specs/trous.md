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

`*` = obligatoire ; les autres champs ont une valeur par défaut ou sont facultatifs. Libellés et descriptions : ceux de la bibliothèque (anglais) ; valeurs par défaut : en français.

- media : groupe — Media
  - type : sous-contenu, library: image | video | audio — Type (Optional media to display above the question.)
  - disableImageZooming : booléen, défaut false, si type = H5P.Image — Disable image zooming
- text : texte riche (Markdown: a code em h2 h3 hr li ol pre strong u ul), défaut Complétez les mots manquants — Task description (A guide telling the user how to answer this task.)
- questions* : liste (min 1, max 31) — Text blocks
  chaque élément = texte riche (Markdown: code del em s strong u) — Line of text
- overallFeedback : groupe — Overall Feedback (groupe à un champ: écrire directement la valeur)
  - overallFeedback : liste (min 1) — Define custom feedback for any score range (Click the "Add range" button to add as many ranges as you need. Example: 0-20% Bad score, 21-91% Average Score, 91-100% Great Score!)
    chaque élément :
      - from : nombre, min 0, max 100, défaut 0 — Score Range
      - to : nombre, min 0, max 100, défaut 100
      - feedback : texte — Feedback for defined score range
- behaviour : réglages — Behavioural settings. (These options will let you control how the task behaves.)
  enableRetry=true, allowRetryIfCorrect=false, enableSolutionsButton=true, autoCheck=false, caseSensitive=true, showSolutionsRequiresInput=true, separateLines=false, confirmCheckDialog=false, confirmRetryDialog=false, acceptSpellingErrors=false

Textes d'interface pré-remplis en français (ne pas fournir sauf besoin) : showSolutions, tryAgain, checkAnswer, submitAnswer, notFilledOut, answerIsCorrect, answerIsWrong, answeredCorrectly, answeredIncorrectly, solutionLabel, inputLabel, inputHasTipLabel, tipLabel, confirmCheck, confirmRetry, scoreBarLabel, a11yCheck, a11yShowSolution, a11yRetry, a11yCheckingModeHeader.

## Exemple complet (validé : validateur officiel H5P + affichage)

Fichier `sources/exemples/trous.md` (médias dans `sources/exemples/media/`).

````markdown
---
type: trous
title: Conjugaison – le passé composé
language: fr
license: CC BY-SA 4.0
---
Complète chaque phrase avec le verbe entre parenthèses conjugué au **passé composé**.

Hier, nous {{sommes allés|sommes allées}} (aller) au musée d'Orsay.

Les élèves {{ont fini::auxiliaire avoir}} (finir) leur exposé à temps.

Marie {{est partie}} (partir) très tôt ce matin et elle {{a pris}} (prendre) le train de 7 h.

```yaml
behaviour:
  caseSensitive: false
  acceptSpellingErrors: false
overallFeedback:
  - {from: 0, to: 59, feedback: "Revois l'accord du participe passé avec l'auxiliaire être."}
  - {from: 60, to: 100, feedback: "Très bien !"}
```
````
