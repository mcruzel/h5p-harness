# Video — `video`

H5P.Video 1.6 · alias : video · syntaxe Markdown simplifiée : oui

## Syntaxe Markdown

Une ou plusieurs lignes `![titre](URL YouTube/Vimeo ou fichier .mp4/.webm)`.

## Champs (bloc ```yaml, noms H5P)

`*` = obligatoire ; les autres champs ont une valeur par défaut ou sont facultatifs.

- sources : vidéo (URL YouTube/Vimeo, chemin ou URL) — Sources vidéo (Selectionnez les fichiers vidéo que vous souhaitez utiliser. Pour assurer une compatibilité maximum avec les …)
- visuals : groupe — Visuels
  - poster : image (chemin ou URL) — Image à la une
  - fit : booléen, défaut true — Le lecteur vidéo utilise toute la place disponible (Si non précisé, le lecteur aura la même taille que la vidéo.)
  - controls : booléen, défaut true — Montrer les boutons de contrôle de la vidéo (Montre les boutons de contrôle de la vidéo : lecture, pause...)
- playback : réglages — Playback
  autoplay=false, loop=false, hasNoAutoPause=false
- a11y : groupe — Accessibilité (groupe à un champ: écrire directement la valeur)
  - videoTrack : liste (min 0) — Ajouter une piste vidéo
    chaque élément :
      - label : texte — Intitulé de la piste
      - kind : choix subtitles|captions|descriptions|chapters, défaut descriptions — Type de piste, voir standard HTML actuel
      - srcLang : texte, défaut en — Fichier de la piste (format WebVTT) (Doit être un code langage conforme à la norme BCP 47. Si le type de piste est défini à "Sous-titres", alors l…)
      - track : fichier (chemin ou URL) — Fichier de la piste (format WebVTT)

Textes d'interface pré-remplis en français (ne pas fournir sauf besoin) : l10n.
