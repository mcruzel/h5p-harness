# Dialog Cards — `cartes`

H5P.Dialogcards 1.9 · alias : cartes, cartes-dialogue, dialogcards · syntaxe Markdown simplifiée : oui

## Syntaxe Markdown

Première ligne `# Titre` facultative, puis description ; une section `## recto` par carte, suivie du verso (Markdown), d'une image `![description](image)` et d'un indice `? …` facultatifs.

```markdown
# Vocabulaire anglais

## Apple
Pomme
![Une pomme](images/pomme.png)

## Book
Livre
? Se lit.
```

## Champs (bloc ```yaml, noms H5P)

`*` = obligatoire ; les autres champs ont une valeur par défaut ou sont facultatifs.

- title : texte riche (Markdown: code em strong) — En-tête
- mode : choix normal|repetition, défaut normal — Mode (Mode de présentation des cartes de dialogue)
- description : texte riche (Markdown: code em strong) — Consigne
- dialogs* : liste (min 1) — Dialogue
  chaque élément :
    - text : texte riche (Markdown: code em strong), défaut  — Question (Texte pour la face avant de la carte)
    - answer : texte riche (Markdown: code em strong), défaut  — Réponse (Texte pour le dos de la carte)
    - image : image (chemin ou URL) — Image (Image facultative pour la carte. (Une carte peut contenir une image seule, un texte seul ou les deux combinés))
    - imageAltText : texte — Texte alternatif pour l'image
    - audio : audio (chemin ou URL) — Fichiers audio
    - tips : groupe — Indices
      - front : texte — Indice pour la face avant (Indice pour la face avant de la carte)
      - back : texte — Indice pour le dos (Indice pour le dos de la carte)
- behaviour : réglages — Paramètres comportementaux (Ces options vous permettent de paramétrer le déroulement de l'exercice.)
  enableRetry=true, disableBackwardsNavigation=false, scaleTextNotCard=false, randomCards=false, maxProficiency=5, quickProgression=false

Textes d'interface pré-remplis en français (ne pas fournir sauf besoin) : answer, next, prev, retry, correctAnswer, incorrectAnswer, round, cardsLeft, nextRound, startOver, showSummary, summary, summaryCardsRight, summaryCardsWrong, summaryCardsNotShown, summaryOverallScore, summaryCardsCompleted, summaryCompletedRounds, summaryAllDone, progressText, cardFrontLabel, cardBackLabel, tipButtonLabel, audioNotSupported, confirmStartingOver.

## Exemple complet (validé : validateur officiel H5P + affichage)

Fichier `tests/examples/cartes.md` (médias dans `tests/media/`).

````markdown
---
type: cartes
title: Cartes – Les formes en anglais
language: fr
license: CC BY-SA 4.0
---
# Les formes géométriques en anglais

Lis le mot français, cherche le mot **anglais**, puis retourne la carte pour vérifier.

## Un carré
A *square*
![Un carré rouge](../media/carre-rouge.png)

## Un cercle
A *circle*
![Un cercle bleu](../media/cercle-bleu.webp)
? It is round.

## Une étoile
A *star*
![Une étoile orange](../media/etoile-orange.png)

## Un losange
A *diamond* (or a *rhombus*)
![Un losange violet](../media/losange-violet.png)
? Comme sur les cartes à jouer.

```yaml
mode: repetition
```
````
