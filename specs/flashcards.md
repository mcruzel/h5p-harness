# Flashcards — `flashcards`

H5P.Flashcards 1.7 · alias : flashcards, cartes-memoire · syntaxe Markdown simplifiée : oui

## Syntaxe Markdown

Description facultative ; une section `## question` par carte, suivie de la réponse attendue (texte court saisi par l'élève), d'une image et d'un indice `? …` facultatifs.

```markdown
Donne la capitale.

## France
Paris
![Carte de France](images/france.png)

## Italie
Rome
? Elle a été fondée par Romulus.
```

## Champs (bloc ```yaml, noms H5P)

`*` = obligatoire ; les autres champs ont une valeur par défaut ou sont facultatifs.

- description* : texte — Consigne
- cards* : liste (min 1) — Cartes
  chaque élément :
    - text : texte — Question
    - answer : texte — Réponse
    - image : image (chemin ou URL) — Image
    - imageAltText : texte — Texte alternatif pour l'image
    - tip : groupe — Indice (groupe à un champ: écrire directement la valeur)
      - tip : texte riche (Markdown: code em strong) — Texte de l'indice
- showSolutionsRequiresInput : booléen, défaut true — Obliger l'utilisateur à entrer une réponse avant de pouvoir afficher …
- caseSensitive : booléen, défaut false — Sensible à la casse
- randomCards : booléen, défaut false — Mélanger les cartes

Textes d'interface pré-remplis en français (ne pas fournir sauf besoin) : progressText, next, previous, checkAnswerText, defaultAnswerText, correctAnswerText, incorrectAnswerText, showSolutionText, results, cardsHeader, scoreHeader, ofCorrect, showResults, answerShortText, retry, cardAnnouncement, correctAnswerAnnouncement, pageAnnouncement.
