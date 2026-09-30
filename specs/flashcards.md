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

`*` = obligatoire ; les autres champs ont une valeur par défaut ou sont facultatifs. Libellés et descriptions : ceux de la bibliothèque (anglais) ; valeurs par défaut : en français.

- description* : texte — Task description
- cards* : liste (min 1) — Cards
  chaque élément :
    - text : texte — Question (Optional textual question for the card. (The card may use just an image, just a text or both))
    - answer : texte — Answer (Answer (solution) for the card. Use a forward slash / to split alternative solutions. Use \/ if a solution should contain a /.)
    - image : image (chemin ou URL) — Image (Optional image for the card. (The card may use just an image, just a text or both))
    - imageAltText : texte — Alternative text for image
    - tip : groupe — Tip (groupe à un champ: écrire directement la valeur)
      - tip : texte riche (Markdown: code em strong) — Tip text
- showSolutionsRequiresInput : booléen, défaut true — Require user input before the solution can be viewed
- caseSensitive : booléen, défaut false — Case sensitive (Makes sure the user input has to be exactly the same as the answer.)
- randomCards : booléen, défaut false — Randomize cards (Enable to randomize the order of cards on display.)

Textes d'interface pré-remplis en français (ne pas fournir sauf besoin) : progressText, next, previous, checkAnswerText, defaultAnswerText, correctAnswerText, incorrectAnswerText, showSolutionText, results, cardsHeader, scoreHeader, ofCorrect, showResults, answerShortText, retry, cardAnnouncement, correctAnswerAnnouncement, pageAnnouncement.

## Exemple complet (validé : validateur officiel H5P + affichage)

Fichier `sources/exemples/flashcards.md` (médias dans `sources/exemples/media/`).

````markdown
---
type: flashcards
title: Flashcards – Nommer les figures
language: fr
license: CC BY-SA 4.0
---
Écris le nom de chaque figure géométrique.

## Quadrilatère avec quatre côtés égaux et quatre angles droits
carré
![Un carré rouge](media/carre-rouge.png)

## Polygone à six côtés
hexagone
![Un hexagone gris](media/hexagone-gris.png)
? Comme les alvéoles d'une ruche.

## Quadrilatère avec quatre côtés égaux, sans angle droit
losange
![Un losange violet](media/losange-violet.png)

## Polygone à trois côtés
triangle
![Un triangle vert](media/triangle-vert.png)

```yaml
randomCards: true
```
````
