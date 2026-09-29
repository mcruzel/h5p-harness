# Advent Calendar (beta) — `calendrier-avent`

H5P.AdventCalendar 0.4 · alias : calendrier-avent, adventcalendar, advent-calendar · syntaxe Markdown simplifiée : non (bloc ```yaml)

## Champs (bloc ```yaml, noms H5P)

`*` = obligatoire ; les autres champs ont une valeur par défaut ou sont facultatifs.

- modeDoorImage : choix manual|automatic, défaut automatic — Mode for door images
- doors* : liste (min 24, max 24) — Doors
  chaque élément :
    - type* : choix audio|image|link|text|video — Content type
    - audio : audio (chemin ou URL), conditionnel — Audio
    - image : sous-contenu, library: image, conditionnel — Image
    - link : sous-contenu, library: lien, conditionnel — Link
    - text : sous-contenu, library: texte, conditionnel — Text
    - video : vidéo (URL YouTube/Vimeo, chemin ou URL), conditionnel — Video
    - autoplay : booléen, défaut false, conditionnel — Autoplay
    - doorCover : image (chemin ou URL), conditionnel — Door image
    - previewImage : image (chemin ou URL) — Background image
- visuals : groupe — Visual settings
  - backgroundImage : image (chemin ou URL) — Calendar background image
  - doorImageTemplate : image (chemin ou URL), conditionnel — Door image template
  - hideDoorBorder : booléen, défaut false — Hide door border
  - hideNumbers : booléen, défaut false — Hide door numbers
  - hideDoorKnobs : booléen, défaut false — Hide door knobs
  - hideDoorFrame : booléen, défaut false — Hide door frame
  - snow : booléen, défaut false — Let it snow
- audio : groupe — Audio settings
  - backgroundMusic : audio (chemin ou URL) — Background music
  - autoplay : booléen, défaut false — Autoplay background music
- behaviour : réglages — Behavioural settings
  modeDoorPlacement=dynamic (fixed|dynamic), doorPlacementRatio=6x4 (6x4|4x6), randomize=false, keepImageOrder=false, designMode=true

Textes d'interface pré-remplis en français (ne pas fournir sauf besoin) : l10n, a11y.
