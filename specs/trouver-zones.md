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
