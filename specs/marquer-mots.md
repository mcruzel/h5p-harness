# Mark the Words — `marquer-mots`

H5P.MarkTheWords 1.11 · alias : marquer-mots, markthewords, mark-the-words · syntaxe Markdown simplifiée : oui

## Syntaxe Markdown

Premier paragraphe sans `{{…}}` = consigne ; la suite = texte où chaque mot à trouver est entouré de `{{…}}` (un seul mot par marque).

```markdown
Clique sur tous les verbes.

Le chat {{dort}} pendant que le chien {{court}} dans le jardin.
```

## Champs (bloc ```yaml, noms H5P)

`*` = obligatoire ; les autres champs ont une valeur par défaut ou sont facultatifs. Libellés et descriptions : ceux de la bibliothèque (anglais) ; valeurs par défaut : en français.

- media : groupe — Media
  - type : sous-contenu, library: image | video | audio — Type (Optional media to display above the question.)
  - disableImageZooming : booléen, défaut false, si type = H5P.Image — Disable image zooming
- taskDescription* : texte riche (Markdown: a code em h2 h3 hr li ol pre strong u ul) — Task description (Describe how the user should solve the task.)
- textField* : texte riche (Markdown: code em strong) — Textfield
- overallFeedback : groupe — Overall Feedback (groupe à un champ: écrire directement la valeur)
  - overallFeedback : liste (min 1) — Define custom feedback for any score range (Click the "Add range" button to add as many ranges as you need. Example: 0-20% Bad score, 21-91% Average Score, 91-100% Great Score!)
    chaque élément :
      - from : nombre, min 0, max 100, défaut 0 — Score Range
      - to : nombre, min 0, max 100, défaut 100
      - feedback : texte — Feedback for defined score range
- behaviour : réglages — Behavioural settings. (These options will let you control how the task behaves.)
  enableRetry=true, enableSolutionsButton=true, showScorePoints=true

Textes d'interface pré-remplis en français (ne pas fournir sauf besoin) : checkAnswerButton, submitAnswerButton, tryAgainButton, showSolutionButton, correctAnswer, incorrectAnswer, missedAnswer, displaySolutionDescription, scoreBarLabel, a11yFullTextLabel, a11yClickableTextLabel, a11ySolutionModeHeader, a11yCheckingHeader, a11yCheck, a11yShowSolution, a11yRetry.

## Exemple complet (validé : validateur officiel H5P + affichage)

Fichier `sources/exemples/marquer-mots.md` (médias dans `sources/exemples/media/`).

```markdown
---
type: marquer-mots
title: Repérer les adjectifs qualificatifs
language: fr
license: CC BY-SA 4.0
---
Clique sur tous les **adjectifs qualificatifs** du texte.

Le {{vieux}} marin regardait la mer {{grise}}. Un vent {{glacial}} soufflait sur le port {{désert}}, et les mouettes criaient au-dessus des bateaux.
```
