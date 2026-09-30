# Summary — `resume`

H5P.Summary 1.10 · alias : resume, summary · syntaxe Markdown simplifiée : oui

## Syntaxe Markdown

Paragraphe(s) d'introduction, puis des séries d'affirmations (une section `##` par série, ou des listes séparées par une ligne vide). Dans chaque série, une seule `- [x]` correcte ; `? indice` indenté optionnel.

```markdown
Choisis l'affirmation correcte dans chaque série.

## Série 1
- [x] La Terre tourne autour du Soleil.
- [ ] Le Soleil tourne autour de la Terre.

## Série 2
- [x] L'eau bout à 100 °C au niveau de la mer.
- [ ] L'eau bout à 50 °C au niveau de la mer.
```

## Champs (bloc ```yaml, noms H5P)

`*` = obligatoire ; les autres champs ont une valeur par défaut ou sont facultatifs. Libellés et descriptions : ceux de la bibliothèque (anglais) ; valeurs par défaut : en français.

- intro : texte riche (Markdown: a code em h2 h3 hr li ol pre strong u ul), défaut Choisissez l'affirmation exac… — Introduction text (Will be displayed above the summary task.)
- summaries* : liste (min 1, max 100) — Summary
  chaque élément :
    - summary* : liste (min 2) — List of statements for the summary - the first statement is correct.
      chaque élément = texte riche (Markdown) — Statement
    - tip : groupe — Tip (groupe à un champ: écrire directement la valeur)
      - tip : texte riche (Markdown: code em strong) — Tip text
- overallFeedback : groupe — Overall Feedback (groupe à un champ: écrire directement la valeur)
  - overallFeedback : liste (min 1) — Define custom feedback for any score range (Click the "Add range" button to add as many ranges as you need. Example: 0-20% Bad score, 21-91% Average Score, 91-100% Great Score!)
    chaque élément :
      - from : nombre, min 0, max 100, défaut 0 — Score Range
      - to : nombre, min 0, max 100, défaut 100
      - feedback : texte — Feedback for defined score range

Textes d'interface pré-remplis en français (ne pas fournir sauf besoin) : solvedLabel, scoreLabel, resultLabel, labelCorrect, labelIncorrect, alternativeIncorrectLabel, labelCorrectAnswers, tipButtonLabel, scoreBarLabel, progressText.

## Exemple complet (validé : validateur officiel H5P + affichage)

Fichier `sources/exemples/resume.md` (médias dans `sources/exemples/media/`).

```markdown
---
type: resume
title: Résumé – Les états de la matière
language: fr
license: CC BY-SA 4.0
---
Construis le résumé du chapitre : dans chaque série, choisis l'affirmation **exacte**.

## Les états
- [x] La matière existe principalement sous trois états : solide, liquide et gazeux.
- [ ] La matière existe uniquement sous deux états : solide et liquide.
- [ ] Un gaz a une forme propre.

## La fusion
- [ ] La fusion est le passage de l'état gazeux à l'état liquide.
- [x] La fusion est le passage de l'état solide à l'état liquide.
  ? Pense à un glaçon qui fond.

## La masse
- [x] Lors d'un changement d'état, la masse se conserve.
- [ ] Lors d'un changement d'état, la masse diminue toujours.
```
