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
  - type : sous-contenu, library: image | video | audio — Type
  - disableImageZooming : booléen, défaut false, conditionnel — Désactiver la possibilité d'agrandir l'image
- question* : texte riche (Markdown: code em h2 h3 pre strong sub sup) — Question
- correct : choix true|false, défaut true — Bonne réponse
- behaviour : groupe — Options générales
  - enableRetry : booléen, défaut true — Activer le bouton "Recommencer"
  - enableSolutionsButton : booléen, défaut true — Activer le bouton "Voir la solution"
  - confirmCheckDialog : booléen, défaut false — Afficher la fenêtre de confirmation pour "Vérifier"
  - confirmRetryDialog : booléen, défaut false — Afficher la fenêtre de confirmation pour "Recommencer"
  - autoCheck : booléen, défaut false — Vérifier automatiquement la réponse cochée
  - feedbackOnCorrect : texte — Commentaire pour une réponse correcte
  - feedbackOnWrong : texte — Commentaire pour une mauvaise réponse

Textes d'interface pré-remplis en français (ne pas fournir sauf besoin) : l10n, confirmCheck, confirmRetry.
