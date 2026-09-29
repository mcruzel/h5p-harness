# Find the Hotspot — `trouver-zone`

H5P.ImageHotspotQuestion 1.8 · alias : trouver-zone, imagehotspotquestion, image-hotspot-question · syntaxe Markdown simplifiée : non (bloc ```yaml)

## Champs (bloc ```yaml, noms H5P)

`*` = obligatoire ; les autres champs ont une valeur par défaut ou sont facultatifs.

- imageHotspotQuestion : groupe — Editeur de questions de l'image interactive
  - backgroundImageSettings : groupe — Image d'arrière-plan (groupe à un champ: écrire directement la valeur)
    - backgroundImage : image (chemin ou URL) — Image d'arrière-plan
  - hotspotSettings : groupe — Zones sensibles
    - taskDescription : texte — Consigne
    - hotspot : liste — Zone sensible
      chaque élément :
        - userSettings : groupe — Réglages manuels
          - correct : booléen — Correct
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
