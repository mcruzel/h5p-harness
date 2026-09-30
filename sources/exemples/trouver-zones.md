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
    backgroundImage: media/paysage.jpg
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
