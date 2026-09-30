# Arithmetic Quiz — `calcul-mental`

H5P.ArithmeticQuiz 1.1 · alias : calcul-mental, arithmeticquiz, arithmetic-quiz · syntaxe Markdown simplifiée : non (bloc ```yaml)

## Champs (bloc ```yaml, noms H5P)

`*` = obligatoire ; les autres champs ont une valeur par défaut ou sont facultatifs. Libellés et descriptions : ceux de la bibliothèque (anglais) ; valeurs par défaut : en français.

- intro : texte — Intro (The intro text (maximum 100 characters))
- quizType : choix arithmetic|linearEquation, défaut arithmetic — Quiz type
- arithmeticType : choix addition|subtraction|multiplication|division, défaut addition, si quizType = arithmetic — Arithmetic type
- equationType : choix basic|intermediate|advanced, défaut intermediate, si quizType = linearEquation — Equation type
- useFractions : booléen, défaut false, si quizType = linearEquation — Enable fractions (Enable to allow fractions in equations.)
- maxQuestions : nombre, min 2, max 100, défaut 20 — Max number of questions

Textes d'interface pré-remplis en français (ne pas fournir sauf besoin) : UI.

## Exemple complet (validé : validateur officiel H5P + affichage)

Fichier `tests/examples/calcul-mental.md` (médias dans `tests/media/`).

````markdown
---
type: calcul-mental
title: Calcul mental – tables de multiplication
language: fr
---
```yaml
intro: Entraîne-toi sur les tables de multiplication. Réponds le plus vite possible !
quizType: arithmetic
arithmeticType: multiplication
maxQuestions: 10
```
````
