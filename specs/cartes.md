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
- mode : choix normal|repetition, défaut normal — Mode
- description : texte riche (Markdown: code em strong) — Consigne
- dialogs* : liste (min 1) — Dialogue
  chaque élément :
    - text : texte riche (Markdown: code em strong), défaut  — Question
    - answer : texte riche (Markdown: code em strong), défaut  — Réponse
    - image : image (chemin ou URL) — Image
    - imageAltText : texte — Texte alternatif pour l'image
    - audio : audio (chemin ou URL) — Fichiers audio
    - tips : groupe — Indices
      - front : texte — Indice pour la face avant
      - back : texte — Indice pour le dos
- behaviour : réglages — Paramètres comportementaux
  enableRetry=true, disableBackwardsNavigation=false, scaleTextNotCard=false, randomCards=false, maxProficiency=5, quickProgression=false

Textes d'interface pré-remplis en français (ne pas fournir sauf besoin) : answer, next, prev, retry, correctAnswer, incorrectAnswer, round, cardsLeft, nextRound, startOver, showSummary, summary, summaryCardsRight, summaryCardsWrong, summaryCardsNotShown, summaryOverallScore, summaryCardsCompleted, summaryCompletedRounds, summaryAllDone, progressText, cardFrontLabel, cardBackLabel, tipButtonLabel, audioNotSupported, confirmStartingOver.
