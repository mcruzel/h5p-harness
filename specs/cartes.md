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

`*` = obligatoire ; les autres champs ont une valeur par défaut ou sont facultatifs. Libellés et descriptions : ceux de la bibliothèque (anglais) ; valeurs par défaut : en français.

- title : texte riche (Markdown: code em strong) — Heading
- mode : choix normal|repetition, défaut normal — Mode (Mode of presenting the dialog cards)
- description : texte riche (Markdown: code em strong) — Task description
- dialogs* : liste (min 1) — Dialogs
  chaque élément :
    - text : texte riche (Markdown: code em strong), défaut  — Text (Hint for the first part of the dialogue)
    - answer : texte riche (Markdown: code em strong), défaut  — Answer (Hint for the second part of the dialogue)
    - image : image (chemin ou URL) — Image (Optional image for the card. (The card may use just an image, just a text or both))
    - imageAltText : texte — Alternative text for the image
    - audio : audio (chemin ou URL) — Audio files
    - tips : groupe — Tips
      - front : texte — Tip for text (Tip for the first part of the dialogue)
      - back : texte — Tip for answer (Tip for the second part of the dialogue)
- behaviour : réglages — Behavioural settings (These options will let you control how the task behaves.)
  enableRetry=true, disableBackwardsNavigation=false, scaleTextNotCard=false, randomCards=false, maxProficiency=5, quickProgression=false

Textes d'interface pré-remplis en français (ne pas fournir sauf besoin) : answer, next, prev, retry, correctAnswer, incorrectAnswer, round, cardsLeft, nextRound, startOver, showSummary, summary, summaryCardsRight, summaryCardsWrong, summaryCardsNotShown, summaryOverallScore, summaryCardsCompleted, summaryCompletedRounds, summaryAllDone, progressText, cardFrontLabel, cardBackLabel, tipButtonLabel, audioNotSupported, confirmStartingOver.

## Exemple complet (validé : validateur officiel H5P + affichage)

Fichier `sources/exemples/cartes.md` (médias dans `sources/exemples/media/`).

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
![Un carré rouge](media/carre-rouge.png)

## Un cercle
A *circle*
![Un cercle bleu](media/cercle-bleu.webp)
? It is round.

## Une étoile
A *star*
![Une étoile orange](media/etoile-orange.png)

## Un losange
A *diamond* (or a *rhombus*)
![Un losange violet](media/losange-violet.png)
? Comme sur les cartes à jouer.

```yaml
mode: repetition
```
````
