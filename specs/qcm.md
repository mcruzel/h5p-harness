# Multiple Choice — `qcm`

H5P.MultiChoice 1.16 · alias : qcm, choix-multiple, multichoice, multi-choice · syntaxe Markdown simplifiée : oui

## Syntaxe Markdown

Énoncé en Markdown, puis une ligne par réponse : `- [x]` bonne réponse, `- [ ]` distracteur (plusieurs `[x]` = cases à cocher). Sous une réponse, lignes indentées : `> retour si cochée`, `< retour si non cochée`, `? indice`. Une ligne `![description](image, vidéo YouTube ou audio)` avant les réponses ajoute un média.

```markdown
Quel organite est le siège de la **photosynthèse** ?
![Cellule végétale](images/cellule.png)
- [x] Le chloroplaste
- [ ] La mitochondrie
  > Non : elle assure la respiration cellulaire.
- [ ] Le noyau
  ? Pense à la couleur des feuilles.
```

## Champs (bloc ```yaml, noms H5P)

`*` = obligatoire ; les autres champs ont une valeur par défaut ou sont facultatifs.

- media : groupe — Média
  - type : sous-contenu, library: image | video | audio — Type
  - disableImageZooming : booléen, défaut false, conditionnel — Désactiver le zoom sur image pour l'image de la question
- question* : texte riche (Markdown: code em h2 h3 pre strong sub sup) — Question
- answers* : liste (min 1) — Options disponibles
  chaque élément :
    - text* : texte riche (Markdown: code em strong sub sup) — Réponse
    - correct : booléen — Réponse correcte
    - tipsAndFeedback : groupe — Aide et retour
      - tip : texte riche (Markdown: a code em strong) — Indice
      - chosenFeedback : texte riche (Markdown: a code em strong sub sup) — Commentaire (si cette réponse a été sélectionnée)
      - notChosenFeedback : texte riche (Markdown: a code em strong sub sup) — Commentaire (si cette réponse n'a pas été sélectionnée)
- overallFeedback : groupe — Retour général (groupe à un champ: écrire directement la valeur)
  - overallFeedback : liste (min 1) — Définir un retour personnalisé pour chaque tranche de score
    chaque élément :
      - from : nombre, min 0, max 100, défaut 0 — Fourchette de score
      - to : nombre, min 0, max 100, défaut 100
      - feedback : texte — Retour pour cet intervalle de score
- behaviour : réglages — Paramètres comportementaux
  enableRetry=true, enableSolutionsButton=true, type=auto (auto|multi|single), singlePoint=false, randomAnswers=true, showSolutionsRequiresInput=true, confirmCheckDialog=false, confirmRetryDialog=false, autoCheck=false, passPercentage=100, showScorePoints=true

Textes d'interface pré-remplis en français (ne pas fournir sauf besoin) : UI, confirmCheck, confirmRetry.
