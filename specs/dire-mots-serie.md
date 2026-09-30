# Speak the Words Set — `dire-mots-serie`

H5P.SpeakTheWordsSet 1.3 · alias : dire-mots-serie, speakthewordsset, speak-the-words-set · syntaxe Markdown simplifiée : non (bloc ```yaml)

## Champs (bloc ```yaml, noms H5P)

`*` = obligatoire ; les autres champs ont une valeur par défaut ou sont facultatifs. Libellés et descriptions : ceux de la bibliothèque (anglais) ; valeurs par défaut : en français.

- introduction : groupe — Introduction
  - showIntroPage : booléen, défaut false — Display introduction
  - introductionImage : image (chemin ou URL), si showIntroPage = True — Introduction image
  - introductionImageAltText : texte, si showIntroPage = True — Alternative text for introduction image
  - introductionTitle : texte, si showIntroPage = True — Title
  - introductionText : texte riche (Markdown: code em strong sub sup), si showIntroPage = True — Introduction text (This title will be displayed above the introduction text.)
- questions* : liste (min 1) — Questions
  chaque élément = sous-contenu, library: dire-mots — Question
- overallFeedback : groupe — Overall Feedback (groupe à un champ: écrire directement la valeur)
  - overallFeedback : liste (min 1) — Define custom feedback for any score range (Click the "Add range" button to add as many ranges as you need. Example: 0-20% Bad score, 21-91% Average Score, 91-100% Great Score!)
    chaque élément :
      - from : nombre, min 0, max 100, défaut 0 — Score Range
      - to : nombre, min 0, max 100, défaut 100
      - feedback : texte — Feedback for defined score range

Textes d'interface pré-remplis en français (ne pas fournir sauf besoin) : l10n.

## Exemple complet (validé : validateur officiel H5P + affichage)

Fichier `tests/examples/dire-mots-serie.md` (médias dans `tests/media/`).

````markdown
---
type: dire-mots-serie
title: Série orale – les formes en anglais
language: fr
---
```yaml
introduction:
  showIntroPage: true
  introductionImage: ../media/paysage.jpg
  introductionImageAltText: Un paysage
  introductionTitle: Say the shapes!
  introductionText: Pour chaque image, dis **en anglais** le nom de la forme.
questions:
  - library: dire-mots
    media: {type: {library: image, file: ../media/cercle-bleu.png, alt: Un cercle bleu}}
    question: Quelle est cette forme ?
    acceptedAnswers: [circle, a circle, it's a circle]
    inputLanguage: en-GB
  - library: dire-mots
    media: {type: {library: image, file: ../media/triangle-vert.png, alt: Un triangle vert}}
    question: Quelle est cette forme ?
    acceptedAnswers: [triangle, a triangle, it's a triangle]
    inputLanguage: en-GB
  - library: dire-mots
    media: {type: {library: image, file: ../media/etoile-orange.png, alt: Une étoile orange}}
    question: Quelle est cette forme ?
    acceptedAnswers: [star, a star, it's a star]
    inputLanguage: en-GB
overallFeedback:
  - {from: 0, to: 50, feedback: Continue à t'entraîner !}
  - {from: 51, to: 100, feedback: Excellent travail !}
```
````
