# Find Multiple Hotspots — `trouver-zones`

H5P.ImageMultipleHotspotQuestion 1.0 · alias : trouver-zones, imagemultiplehotspotquestion, image-multiple-hotspot-question · syntaxe Markdown simplifiée : non (bloc ```yaml)

## Champs (bloc ```yaml, noms H5P)

`*` = obligatoire ; les autres champs ont une valeur par défaut ou sont facultatifs.

- imageMultipleHotspotQuestion : groupe — Image Multiple Hotspot Question Editor
  - backgroundImageSettings : groupe — Background image
    - questionTitle : texte, défaut Question à zones sensibles su… — The title of this question
    - backgroundImage : image (chemin ou URL) — Background image
  - hotspotSettings : groupe — Hotspots
    - taskDescription : texte — Task description
    - hotspotName : texte — Hotspot Name
    - numberHotspots : nombre — Number of correct hotspots that need to be found for question complet…
    - hotspot : liste — Hotspot
      chaque élément :
        - userSettings : groupe — userSettings
          - correct : booléen — Correct
          - feedbackText : texte — Feedback
        - computedSettings : groupe — computedSettings
          - x : nombre
          - y : nombre
          - width : nombre
          - height : nombre
          - figure : texte
    - noneSelectedFeedback : texte — Feedback if the user selects an empty spot:
    - alreadySelectedFeedback : texte — Feedback if the user selects an already found hotspot:

## Exemple complet (validé : validateur officiel H5P + affichage)

Fichier `tests/examples/trouver-zones.md` (médias dans `tests/media/`).

````markdown
---
type: trouver-zones
title: Les éléments naturels d'un paysage
language: fr
preset: entrainement
license: CC BY-SA 4.0
authors: Équipe d'histoire-géographie
---
```yaml
imageMultipleHotspotQuestion:
  backgroundImageSettings:
    questionTitle: Les éléments naturels d'un paysage
    backgroundImage: ../media/paysage.jpg
  hotspotSettings:
    taskDescription: Clique sur les trois éléments naturels de ce paysage (ceux qui ne sont pas construits par l'être humain).
    hotspotName: éléments naturels
    numberHotspots: 3
    hotspot:
      - userSettings: {correct: true, feedbackText: "Oui, le Soleil est un élément naturel."}
        computedSettings: {x: 79, y: 10, width: 12.5, height: 18.75, figure: circle}
      - userSettings: {correct: true, feedbackText: "Oui, l'arbre est un élément naturel."}
        computedSettings: {x: 51.5, y: 37, width: 17, height: 33, figure: rectangle}
      - userSettings: {correct: true, feedbackText: "Oui, la prairie est un élément naturel."}
        computedSettings: {x: 0, y: 72, width: 100, height: 28, figure: rectangle}
      - userSettings: {correct: false, feedbackText: "Non : la maison est un aménagement humain."}
        computedSettings: {x: 10.8, y: 32.5, width: 24.2, height: 37.5, figure: rectangle}
    noneSelectedFeedback: Il n'y a rien à trouver ici, essaie ailleurs.
    alreadySelectedFeedback: Tu as déjà trouvé cet élément !
```
````
