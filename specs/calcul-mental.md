# Arithmetic Quiz — `calcul-mental`

H5P.ArithmeticQuiz 1.1 · alias : calcul-mental, arithmeticquiz, arithmetic-quiz · syntaxe Markdown simplifiée : non (bloc ```yaml)

## Champs (bloc ```yaml, noms H5P)

`*` = obligatoire ; les autres champs ont une valeur par défaut ou sont facultatifs.

- intro : texte — Introduction
- quizType : choix arithmetic|linearEquation, défaut arithmetic — Type du quiz
- arithmeticType : choix addition|subtraction|multiplication|division, défaut addition, conditionnel — Type d'opération
- equationType : choix basic|intermediate|advanced, défaut intermediate, conditionnel — Type d'équation
- useFractions : booléen, défaut false, conditionnel — Activer les fractions
- maxQuestions : nombre, min 2, max 100, défaut 20 — Nombre maximum de questions

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
