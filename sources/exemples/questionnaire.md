---
type: questionnaire
title: Questionnaire – Bilan de la séquence
language: fr
license: CC BY-SA 4.0
---
```yaml
questionnaireElements:
  - library:
      library: choix-simple
      question: As-tu trouvé cette séquence sur les volcans intéressante ?
      inputType: radio
      alternatives:
        - text: Oui, beaucoup
        - text: Un peu
        - text: Pas du tout
    requiredField: true
  - library:
      library: choix-simple
      question: Quelles activités as-tu préférées ?
      inputType: checkbox
      alternatives:
        - text: La vidéo sur l'Etna
        - text: La maquette de volcan
        - text: Le quiz final
  - library:
      library: question-ouverte
      question: Qu'aimerais-tu approfondir lors de la prochaine séance ?
      placeholderText: Écris ta réponse ici…
      inputRows: "3"
successScreenOptions:
  successMessage: Merci pour tes réponses ! Elles aideront ton professeur à préparer la suite.
```
