# Find the Hotspot — `trouver-zone`

H5P.ImageHotspotQuestion 1.8 · alias : trouver-zone, imagehotspotquestion, image-hotspot-question · syntaxe Markdown simplifiée : non (bloc ```yaml)

## Points d'attention

- Zones : `computedSettings: {x, y, width, height, figure}` ; `x`/`y` = coin haut-gauche **en % de l'image**, `width`/`height` en %, `figure` = `rectangle` ou `circle`.
- `userSettings: {correct: true|false, feedbackText: …}` pour chaque zone ; `noneSelectedFeedback` si l'élève clique hors zone.

## Champs (bloc ```yaml, noms H5P)

`*` = obligatoire ; les autres champs ont une valeur par défaut ou sont facultatifs.

- imageHotspotQuestion : groupe — Editeur de questions de l'image interactive
  - backgroundImageSettings : groupe — Image d'arrière-plan (groupe à un champ: écrire directement la valeur)
    - backgroundImage : image (chemin ou URL) — Image d'arrière-plan (Sélectionner une image à utiliser comme fond pour la question de la zone réactive de l'image.)
  - hotspotSettings : groupe — Zones sensibles (Sélectionnez la forme de votre choix pour votre zone sensible, redimensionnez-la en l'étirant et placez-la au…)
    - taskDescription : texte — Consigne (Consigne pour l'utilisateur.)
    - hotspot : liste — Zone sensible
      chaque élément :
        - userSettings : groupe — Réglages manuels
          - correct : booléen — Correct (Il peut y avoir plusieurs zones sensibles à trouver. Toutefois, l'utilisateur est averti de la justesse ou no…)
          - feedbackText : texte — Commentaire de retour
        - computedSettings : groupe — Réglages calculés automatiquement
          - x : nombre
          - y : nombre
          - width : nombre
          - height : nombre
          - figure : texte
    - noneSelectedFeedback : texte — Commentaire si l'utilisateur sélectionne une zone vide :
    - showFeedbackAsPopup : booléen, défaut true — Afficher un feedback sur la zone

Textes d'interface pré-remplis en français (ne pas fournir sauf besoin) : l10n, scoreBarLabel, a11yRetry.

## Exemple complet (validé : validateur officiel H5P + affichage)

Fichier `tests/examples/trouver-zone.md` (médias dans `tests/media/`).

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
  backgroundImageSettings: ../media/paysage.jpg
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
