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

`*` = obligatoire ; les autres champs ont une valeur par défaut ou sont facultatifs.

- media : groupe — Média
  - type : sous-contenu, library: image | video | audio — Type (Média à afficher au-dessus de la question (facultatif).)
  - disableImageZooming : booléen, défaut false, conditionnel — Désactiver la possibilité d'agrandir l'image
- question* : texte riche (Markdown: code em h2 h3 pre strong sub sup) — Question
- correct : choix true|false, défaut true — Bonne réponse
- behaviour : groupe — Options générales (Ces options vous permettent de paramétrer le déroulement de l'exercice.)
  - enableRetry : booléen, défaut true — Activer le bouton "Recommencer"
  - enableSolutionsButton : booléen, défaut true — Activer le bouton "Voir la solution"
  - confirmCheckDialog : booléen, défaut false — Afficher la fenêtre de confirmation pour "Vérifier"
  - confirmRetryDialog : booléen, défaut false — Afficher la fenêtre de confirmation pour "Recommencer"
  - autoCheck : booléen, défaut false — Vérifier automatiquement la réponse cochée (Noter que l'accessibilité sera pénalisée si cette option est activée)
  - feedbackOnCorrect : texte — Commentaire pour une réponse correcte (Ceci remplacera le commentaire par défaut. Variables disponibles: @score et @total)
  - feedbackOnWrong : texte — Commentaire pour une mauvaise réponse (Ceci remplacera le commentaire par défaut. Variables disponibles: @score et @total)

Textes d'interface pré-remplis en français (ne pas fournir sauf besoin) : l10n, confirmCheck, confirmRetry.

## Exemple complet (validé : validateur officiel H5P + affichage)

Fichier `tests/examples/vf.md` (médias dans `tests/media/`).

```markdown
---
type: vf
title: Le cycle de l'eau – Vrai ou faux
language: fr
license: CC BY-SA 4.0
---
Lors de l'**évaporation**, l'eau passe de l'état liquide à l'état *gazeux*.
![Paysage avec lac et nuages](../media/paysage.jpg)
- [x] Vrai
  > Exact : la chaleur du Soleil transforme l'eau liquide en vapeur d'eau.
- [ ] Faux
  > Non : relis la définition des changements d'état.
```
