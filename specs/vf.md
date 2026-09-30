# True/False Question — `vf`

H5P.TrueFalse 1.8 · alias : vf, vrai-faux, truefalse, true-false · syntaxe Markdown simplifiée : oui

## Syntaxe Markdown

Affirmation en Markdown, puis `- [x] Vrai` / `- [ ] Faux` (cocher la bonne). Retour optionnel en ligne indentée `> …` sous chaque option (sous la bonne : affiché si réussi ; sous l'autre : si erroné). Variante courte : une ligne `réponse: faux`. Dans un quiz : `## vf: faux`.

```markdown
La mitochondrie contient de la chlorophylle.
- [ ] Vrai
  > Non : la chlorophylle est dans les chloroplastes.
- [x] Faux
  > Exact !
```

## Champs (bloc ```yaml, noms H5P)

`*` = obligatoire ; les autres champs ont une valeur par défaut ou sont facultatifs. Libellés et descriptions : ceux de la bibliothèque (anglais) ; valeurs par défaut : en français.

- media : groupe — Media
  - type : sous-contenu, library: image | video | audio — Type (Optional media to display above the question.)
  - disableImageZooming : booléen, défaut false, si type = H5P.Image — Disable image zooming
- question* : texte riche (Markdown: code em h2 h3 pre strong sub sup) — Question
- correct : choix true|false, défaut true — Correct answer
- behaviour : groupe — Behavioural settings (These options will let you control how the task behaves.)
  - enableRetry : booléen, défaut true — Enable "Retry" button
  - enableSolutionsButton : booléen, défaut true — Enable "Show Solution" button
  - confirmCheckDialog : booléen, défaut false — Show confirmation dialog on "Check"
  - confirmRetryDialog : booléen, défaut false — Show confirmation dialog on "Retry"
  - autoCheck : booléen, défaut false — Automatically check answer (Note that accessibility will suffer if enabling this option)
  - feedbackOnCorrect : texte — Feedback on correct answer (This will override the default feedback text. Variables available: @score and @total)
  - feedbackOnWrong : texte — Feedback on wrong answer (This will override the default feedback text. Variables available: @score and @total)

Textes d'interface pré-remplis en français (ne pas fournir sauf besoin) : l10n, confirmCheck, confirmRetry.

## Exemple complet (validé : validateur officiel H5P + affichage)

Fichier `sources/exemples/vf.md` (médias dans `sources/exemples/media/`).

```markdown
---
type: vf
title: Le cycle de l'eau – Vrai ou faux
language: fr
license: CC BY-SA 4.0
---
Lors de l'**évaporation**, l'eau passe de l'état liquide à l'état *gazeux*.
![Paysage avec lac et nuages](media/paysage.jpg)
- [x] Vrai
  > Exact : la chaleur du Soleil transforme l'eau liquide en vapeur d'eau.
- [ ] Faux
  > Non : relis la définition des changements d'état.
```
