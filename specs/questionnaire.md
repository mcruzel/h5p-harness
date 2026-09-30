# Questionnaire — `questionnaire`

H5P.Questionnaire 1.3 · alias : questionnaire · syntaxe Markdown simplifiée : non (bloc ```yaml)

## Champs (bloc ```yaml, noms H5P)

`*` = obligatoire ; les autres champs ont une valeur par défaut ou sont facultatifs. Libellés et descriptions : ceux de la bibliothèque (anglais) ; valeurs par défaut : en français.

- questionnaireElements* : liste (min 1) — Questionnaire elements
  chaque élément :
    - library* : sous-contenu, library: question-ouverte | choix-simple — Library (Choose a library)
    - requiredField : booléen, défaut false — Required field
- successScreenOptions : groupe — Success screen options
  - enableSuccessScreen : booléen, défaut true — Enable success screen
  - successScreenImage : groupe — Add success screen image (groupe à un champ: écrire directement la valeur)
    - successScreenImage : sous-contenu, library: image — Replace success icon with image
  - successMessage : texte, défaut Vous avez terminé le question… — Text to display on submit

Textes d'interface pré-remplis en français (ne pas fournir sauf besoin) : uiElements.

## Exemple complet (validé : validateur officiel H5P + affichage)

Fichier `tests/examples/questionnaire.md` (médias dans `tests/media/`).

````markdown
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
````
