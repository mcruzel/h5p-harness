# Single Choice Set — `choix-unique`

H5P.SingleChoiceSet 1.11 · alias : choix-unique, singlechoiceset, single-choice-set · syntaxe Markdown simplifiée : oui

## Syntaxe Markdown

Une section `## question` par question, avec exactement une réponse `[x]` (l'ordre est mélangé à l'affichage).

```markdown
## Capitale de l'Espagne ?
- [x] Madrid
- [ ] Barcelone
- [ ] Séville

## 7 × 8 = ?
- [ ] 54
- [x] 56
```

## Champs (bloc ```yaml, noms H5P)

`*` = obligatoire ; les autres champs ont une valeur par défaut ou sont facultatifs.

- choices* : liste (min 1) — Liste des questions
  chaque élément :
    - question* : texte riche (Markdown: code em strong) — Question
    - answers* : liste (min 2, max 4) — Réponses possibles - la première de la liste est celle qui est juste.
      chaque élément = texte riche (Markdown: code em strong) — Réponse possible
- overallFeedback : groupe — Opacité des étiquettes (groupe à un champ: écrire directement la valeur)
  - overallFeedback : liste (min 1) — Définissez le feedback pour chaque intervalle de score
    chaque élément :
      - from : nombre, min 0, max 100, défaut 0 — Intervalle de score
      - to : nombre, min 0, max 100, défaut 100
      - feedback : texte — Feedback pour l'intervalle de score défini
- behaviour : réglages — Paramètres comportementaux
  autoContinue=true, timeoutCorrect=2000, timeoutWrong=3000, soundEffectsEnabled=true, enableRetry=true, enableSolutionsButton=true, passPercentage=100

Textes d'interface pré-remplis en français (ne pas fournir sauf besoin) : l10n.
