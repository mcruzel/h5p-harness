---
type: outil-documentation
title: Carnet de bord – exposé sur le système solaire
language: fr
---
```yaml
# metadata.title = titre de la page dans le sommaire
taskDescription: Carnet de bord de l'exposé
pagesList:
  - library: goalspage
    metadata: {title: Mes objectifs}
    description: |
      Fixe-toi **deux ou trois objectifs** pour ton exposé sur le système solaire
      (par exemple : « parler 5 minutes sans lire mes notes »).
  - library: page-standard
    metadata: {title: Mes recherches}
    elementList:
      - library: texte-simple
        text: |
          ## Mes recherches
          Note ici ce que tu as appris sur la planète que tu as choisie.
      - library: textinputfield
        taskDescription: Quelle planète as-tu choisie ?
        placeholderText: Mars, Jupiter…
        requiredField: true
      - library: textinputfield
        taskDescription: Cite trois informations importantes sur cette planète.
        inputFieldSize: "10"
      - library: image
        file: ../media/cercle-bleu.png
        alt: Schéma d'une planète
    helpText: Utilise au moins **deux sources** différentes (manuel, CDI, site institutionnel).
  - library: goalsassessmentpage
    metadata: {title: Bilan des objectifs}
    description: Évalue maintenant les objectifs que tu t'étais fixés.
  - library: documentexportpage
    metadata: {title: Exporter le carnet}
    description: Exporte ton carnet de bord pour le rendre à ton professeur.
```
