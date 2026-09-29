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
  - overallFeedback : liste (min 1) — Définissez le feedback pour chaque intervalle de score (Cliquez le bouton "Ajouter Intervalle" pour ajouter autant d'intervalles que vous le souhaitez. Exemple : 0-2…)
    chaque élément :
      - from : nombre, min 0, max 100, défaut 0 — Intervalle de score
      - to : nombre, min 0, max 100, défaut 100
      - feedback : texte — Feedback pour l'intervalle de score défini
- behaviour : réglages — Paramètres comportementaux
  autoContinue=true, timeoutCorrect=2000, timeoutWrong=3000, soundEffectsEnabled=true, enableRetry=true, enableSolutionsButton=true, passPercentage=100

Textes d'interface pré-remplis en français (ne pas fournir sauf besoin) : l10n.

## Exemple complet (validé : validateur officiel H5P + affichage)

Fichier `tests/examples/choix-unique.md` (médias dans `tests/media/`).

````markdown
---
type: choix-unique
title: Révolution française – questions rapides
language: fr
license: CC BY-SA 4.0
---
## En quelle année a eu lieu la prise de la Bastille ?
- [ ] 1792
- [x] 1789
- [ ] 1815

## Quel texte est adopté le 26 août 1789 ?
- [x] La *Déclaration des droits de l'homme et du citoyen*
- [ ] Le Code civil
- [ ] La Constitution de la Ve République

## Qui est roi de France en 1789 ?
- [ ] Louis XIV
- [ ] Napoléon Ier
- [x] Louis XVI
- [ ] Charles X

```yaml
behaviour:
  timeoutCorrect: 1500
  passPercentage: 60
overallFeedback:
  - {from: 0, to: 59, feedback: "Relis la chronologie de la Révolution."}
  - {from: 60, to: 100, feedback: "Bravo, tu maîtrises les dates clés !"}
```
````
