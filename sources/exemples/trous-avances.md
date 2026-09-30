---
type: trous-avances
title: Homophones a / à et et / est
language: fr
license: CC BY-SA 4.0
---
```yaml
content:
  task: Complète chaque phrase avec **a** ou **à**, **et** ou **est**.
  blanksText: |
    Léa ___ fini ses devoirs ___ elle part ___ la piscine.

    Le ciel ___ gris ce matin.
  blanksList:
    - - text: a
        isCorrect: true
        hint: "Essaie de remplacer par « avait »."
      - text: à
        optionsIncorrect:
          incorrectAnswerFeedback: "On peut dire « Léa **avait** fini » : c'est le verbe *avoir*, donc « a » sans accent."
    - - text: et
        isCorrect: true
      - text: est
        optionsIncorrect:
          incorrectAnswerFeedback: "On ne peut pas dire « Léa a fini ses devoirs **était** elle part » : il faut « et »."
    - - text: à
        isCorrect: true
      - text: a
        optionsIncorrect:
          incorrectAnswerFeedback: "On ne peut pas dire « elle part **avait** la piscine » : c'est la préposition « à »."
    - - text: est
        isCorrect: true
        hint: "Essaie de remplacer par « était »."
      - text: et
        optionsIncorrect:
          incorrectAnswerFeedback: "« Le ciel **était** gris » fonctionne : c'est le verbe *être*."
behaviour:
  mode: selection
  selectAlternatives: alternatives
overallFeedback:
  - {from: 0, to: 74, feedback: "Pense à remplacer par « avait » ou « était »."}
  - {from: 75, to: 100, feedback: "Bravo, tu maîtrises ces homophones !"}
```
