# Video — `video`

H5P.Video 1.6 · alias : video · syntaxe Markdown simplifiée : oui

## Syntaxe Markdown

Une ou plusieurs lignes `![titre](URL YouTube/Vimeo ou fichier .mp4/.webm)`.

## Champs (bloc ```yaml, noms H5P)

`*` = obligatoire ; les autres champs ont une valeur par défaut ou sont facultatifs. Libellés et descriptions : ceux de la bibliothèque (anglais) ; valeurs par défaut : en français.

- sources* : vidéo (URL YouTube/Vimeo, chemin ou URL) — Video sources (To ensure that the video works in all browsers you should add both WebM and MP4 formatted sources.)
- visuals : groupe — Visuals
  - poster : image (chemin ou URL) — Poster image
  - fit : booléen, défaut true — Fit video player to use all available space (If not set the video player will have the same aspect ratio as the video.)
  - controls : booléen, défaut true — Show video player controls (Add controls to the video player. This allows users to play, pause, etc.)
- playback : réglages — Playback
  autoplay=false, loop=false, hasNoAutoPause=false
- a11y : groupe — Accessibility (groupe à un champ: écrire directement la valeur)
  - videoTrack : liste (min 0) — Add video track
    chaque élément :
      - label : texte — Track label
      - kind : choix subtitles|captions|descriptions|chapters, défaut descriptions — Type kind, refer to HTML living standard
      - srcLang : texte, défaut en — Source language, must be defined for subtitles (Must be a valid BCP 47 language tag. If the kind attribute is set to subtitles, then srclang must be defined.)
      - track : fichier (chemin ou URL) — Track file (WebVTT)

Textes d'interface pré-remplis en français (ne pas fournir sauf besoin) : l10n.
