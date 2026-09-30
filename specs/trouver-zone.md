# Find the Hotspot — `trouver-zone`

H5P.ImageHotspotQuestion 1.8 · alias : trouver-zone, imagehotspotquestion, image-hotspot-question · syntaxe Markdown simplifiée : non (bloc ```yaml)

## Points d'attention

- Zones : `computedSettings: {x, y, width, height, figure}` ; `x`/`y` = coin haut-gauche **en % de l'image**, `width`/`height` en %, `figure` = `rectangle` ou `circle`.
- `userSettings: {correct: true|false, feedbackText: …}` pour chaque zone ; `noneSelectedFeedback` si l'élève clique hors zone.

## Champs (bloc ```yaml, noms H5P)

`*` = obligatoire ; les autres champs ont une valeur par défaut ou sont facultatifs. Libellés et descriptions : ceux de la bibliothèque (anglais) ; valeurs par défaut : en français.

- imageHotspotQuestion : groupe — Image Hotspot Question Editor
  - backgroundImageSettings : groupe — Background image (groupe à un champ: écrire directement la valeur)
    - backgroundImage* : image (chemin ou URL) — Background image (Select an image to use as background for the image hotspot question.)
  - hotspotSettings : groupe — Hotspots (Drag and drop the desired figure from the toolbar to create a new hotspot. Double-click to edit an existing hotspot. Drag the hotspot to move it. Pull the resize handler in the lower right corner to resize.)
    - taskDescription : texte — Task description (Instructions to the user.)
    - hotspot : liste — Hotspot
      chaque élément :
        - userSettings : groupe — userSettings
          - correct : booléen — Correct (There can be multiple correct hotspots. However, the user gets correct/incorrect feedback immediately after first click.)
          - feedbackText : texte — Feedback
        - computedSettings : groupe — computedSettings
          - x : nombre
          - y : nombre
          - width : nombre
          - height : nombre
          - figure : texte
    - noneSelectedFeedback : texte — Feedback if the user selects an empty spot:
    - showFeedbackAsPopup : booléen, défaut true — Show feedback as a popup

Textes d'interface pré-remplis en français (ne pas fournir sauf besoin) : l10n, scoreBarLabel, a11yRetry.

## Exemple complet (validé : validateur officiel H5P + affichage)

Fichier `sources/exemples/trouver-zone.md` (médias dans `sources/exemples/media/`).

````markdown
---
type: trouver-zone
title: La source d'énergie de la photosynthèse
language: fr
preset: entrainement
license: CC BY-SA 4.0
authors: Équipe de SVT
---
```yaml
imageHotspotQuestion:
  backgroundImageSettings: media/paysage.jpg
  hotspotSettings:
    taskDescription: Clique sur la source d'énergie qui permet aux végétaux de réaliser la photosynthèse.
    hotspot:
      - userSettings:
          correct: true
          feedbackText: Bravo ! Le Soleil fournit l'énergie lumineuse captée par la chlorophylle.
        computedSettings: {x: 79, y: 10, width: 12.5, height: 18.75, figure: circle}
      - userSettings:
          correct: false
          feedbackText: L'arbre utilise l'énergie lumineuse, mais il ne la produit pas.
        computedSettings: {x: 51.5, y: 37, width: 17, height: 33, figure: rectangle}
      - userSettings:
          correct: false
          feedbackText: La maison ne joue aucun rôle dans la photosynthèse.
        computedSettings: {x: 10.8, y: 32.5, width: 24.2, height: 37.5, figure: rectangle}
    noneSelectedFeedback: Tu n'as cliqué sur aucun élément du paysage. Observe le ciel !
    showFeedbackAsPopup: true
```
````
