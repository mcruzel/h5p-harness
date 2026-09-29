# Image Hotspots — `image-interactive`

H5P.ImageHotspots 1.11 · alias : image-interactive, imagehotspots, image-hotspots · syntaxe Markdown simplifiée : non (bloc ```yaml)

## Champs (bloc ```yaml, noms H5P)

`*` = obligatoire ; les autres champs ont une valeur par défaut ou sont facultatifs.

- image : image (chemin ou URL) — Image d'arrière-plan
- backgroundImageAltText : texte — Texte alternatif pour l'image d'arrière-plan
- globalIconType : choix icon|image|numbers, défaut icon — Global hotspot Icon
- globalIcon : choix plus|minus|times|check|question|info|exclamation, défaut plus, conditionnel — Predefined icon
- globalIconImage : image (chemin ou URL), conditionnel — Uploaded image
- globalColor : texte, défaut #981d99, conditionnel — Hotspot color
- hotspots* : liste (min 1) — Puce cliquable
  chaque élément :
    - position : groupe — Position de la puce cliquable
      - x* : nombre
      - y* : nombre
      - legacyPositioning : booléen
    - hotspotIconType : choix default|icon|image, défaut default — Custom hotspot icon
    - hotspotIcon : choix plus|minus|times|check|question|info|exclamation, défaut plus, conditionnel — Predefined icon
    - hotspotIconImage : image (chemin ou URL), conditionnel — Uploaded image
    - hotspotColor : texte, défaut #981d99, conditionnel — Hotspot color
    - alwaysFullscreen : booléen — Recouvrir toute l'image d'arrière-plan
    - header : texte — Header
    - content : liste — Contenu du popup
      chaque élément = sous-contenu, library: texte-simple | video | image | audio — Type de contenu

Textes d'interface pré-remplis en français (ne pas fournir sauf besoin) : untitledHotspotLabel, closeButtonLabel, containsAudioVideoLabel.
