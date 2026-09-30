# Interactive Video — `video-interactive`

H5P.InteractiveVideo 1.28 · alias : video-interactive, interactivevideo, interactive-video · syntaxe Markdown simplifiée : oui

## Syntaxe Markdown

**Interactions seulement d'après le transcrit.** Questions et activités ne sont ajoutées que si la source déclare le transcrit horodaté de la vidéo (`.vtt` ou `.srt`) : `transcript: fichier.vtt` dans l'en-tête (ou une ligne `transcrit: fichier.vtt` sous la vidéo). Sans lui, le harnais refuse les interactions et, pour une vidéo seule, indique en « piste » comment l'obtenir : le demander à l'agent qui a confié la tâche ou à l'utilisateur (sous-titres de la plateforme vidéo, export d'un outil de transcription). `python -m h5pharness transcript fichier.vtt` l'affiche en lignes horodatées `m:ss texte` : placer chaque question après le passage qui y répond. Le harnais vérifie que chaque interaction tombe dans la durée du transcrit, signale une question sans mot commun avec ce qui vient d'être dit, et ajoute le transcrit comme sous-titres de la vidéo.

Une ligne `![titre](vidéo)` (fichier MP4/WebM, URL, ou lien YouTube/Vimeo), une courte description facultative, puis une section par moment de la vidéo : `## <temps> <type>` avec le temps en `m:ss` (ou secondes). Types : questions (`qcm`, `vf: faux`, `trous`, `glisser-mots`, `marquer-mots`, `choix-unique`, `resume`…) affichées en carte et mettant la vidéo en pause ; `texte` (bouton d'information, sans pause) ; `signet: Titre` (chapitre) ; `fin: Titre` (écran de fin). Une interaction reste affichée 10 s, ou jusqu'à l'apparition de la suivante. Positions et durées fines : bloc ```yaml (`interactiveVideo.assets.interactions[n]` : temps en secondes ou `m:ss`, x/y en % de la vidéo, width/height en em, facultatifs). Un bloc ```yaml peut aussi compléter le raccourci (ex. `summary`).

```markdown
![La photosynthèse](videos/photosynthese.mp4)
transcrit: videos/photosynthese.vtt
Regarde la vidéo et réponds aux questions.

## 0:00 signet: Introduction

## 0:45 texte
Observe la couleur des feuilles.

## 1:30 qcm
Quel gaz est rejeté ?
- [x] Le dioxygène
- [ ] Le dioxyde de carbone
```

## Champs (bloc ```yaml, noms H5P)

`*` = obligatoire ; les autres champs ont une valeur par défaut ou sont facultatifs. Libellés et descriptions : ceux de la bibliothèque (anglais) ; valeurs par défaut : en français.

- interactiveVideo : groupe — Interactive Video Editor
  - video : groupe — Upload/embed video
    - files : vidéo (URL YouTube/Vimeo, chemin ou URL) — Add a video (Click below to add a video you wish to use in your interactive video. You can add a video link or upload video files. It is possible to add several versions of the video with different qualities. To ensure maximum suppo…)
    - startScreenOptions : groupe — Start screen options (unsupported for YouTube videos)
      - title : texte, défaut Vidéo interactive — The title of this interactive video (Used in summaries, statistics etc.)
      - hideStartTitle : booléen, défaut false — Hide title on video start screen
      - shortStartDescription : texte — Short description (Optional) (Optional. Display a short description text on the video start screen. Does not work for YouTube videos.)
      - poster : image (chemin ou URL) — Poster image (Image displayed before the user launches the video. Does not work for YouTube Videos.)
    - textTracks : groupe — Text tracks (unsupported for YouTube videos)
      - videoTrack : liste (min 0) — Available text tracks
        chaque élément :
          - label : texte, défaut Sous-titres — Track label (Used if you offer multiple tracks and the user has to choose a track. For instance 'Spanish subtitles' could be the label of a Spanish subtitle track.)
          - kind : choix subtitles|captions|descriptions, défaut subtitles — Type of text track
          - srcLang : texte, défaut en — Source language, must be defined for subtitles (Must be a valid BCP 47 language tag. If 'Subtitles' is the type of text track selected, the source language of the track must be defined.)
          - track : fichier (chemin ou URL) — Track source (WebVTT file)
      - defaultTrackLabel : texte — Default text track (If left empty or not matching any of the text tracks the first text track will be used as the default.)
  - assets : groupe — Add interactions
    - interactions : liste
      chaque élément :
        - duration : groupe — Display time
          - from* : nombre
          - to* : nombre
        - pause : booléen — Pause video
        - displayType : choix button|poster, défaut button — Display as (Button is a collapsed interaction the user must press to open. Poster is an expanded interaction displayed directly on top of the video)
        - buttonOnMobile : booléen, défaut false — Turn into button on small screens
        - label : texte riche (Markdown) — Label (Label displayed next to interaction icon.)
        - x, y, width, height : nombre, facultatif — x, y en % de la vidéo ; width, height en em ; défaut : carte centrée (poster) ou bouton au centre
        - action* : sous-contenu, library: nil | texte-simple | tableau | lien | image | resume | choix-unique | qcm | vf | trous | glisser-deposer | marquer-mots | glisser-mots | aller-a-question | zone-video | questionnaire | question-libre | choix-images
        - adaptivity : groupe — Adaptivity
          - correct : groupe — Action on all correct
            - seekTo* : nombre — Seek to (Enter timecode in the format M:SS)
            - allowOptOut : booléen — Allow the user to opt out and continue
            - message* : texte riche (Markdown: a code del em s strong) — Message
            - seekLabel* : texte — Label for seek button
          - wrong : groupe — Action on wrong
            - seekTo* : nombre — Seek to (Enter timecode in the format M:SS)
            - allowOptOut : booléen — Allow the user to opt out and continue
            - message* : texte riche (Markdown: a code del em s strong) — Message
            - seekLabel* : texte — Label for seek button
          - requireCompletion : booléen — Require full score for task before proceeding (For best functionality this option should be used in conjunction with the "Disable navigation forward in a video" option of Interactive Video.)
        - visuals : réglages — Visuals
          backgroundColor=rgb(255, 255, 255), boxShadow=true
        - goto : groupe — Go to on click
          - type : choix timecode|url — Type
          - time : nombre — Go To (The target time the user will be taken to upon pressing the hotspot. Enter timecode in the format M:SS.)
          - url : groupe — URL
            - protocol : choix http://|https://|/|other, défaut http:// — Protocol
            - url : texte — URL
          - visualize : booléen — Visualize (Show that interaction can be clicked by adding a border and an icon)
    - bookmarks : liste
      chaque élément :
        - time* : nombre
        - label* : texte
    - endscreens : liste
      chaque élément :
        - time* : nombre
        - label* : texte
  - summary : groupe — Summary task
    - task : sous-contenu, library: resume, défaut {'library': 'H5P.Summary 1.10…
    - displayAt : nombre, défaut 3 — Display at (Number of seconds before the video ends.)
- override : groupe — Behavioural settings
  - startVideoAt : nombre — Start video at (Enter timecode in the format M:SS)
  - autoplay : booléen, défaut false — Auto-play video (Start playing the video automatically)
  - loop : booléen, défaut false — Loop the video (Check if video should run in a loop)
  - hasNoAutoPause : booléen, défaut false — Deactivate auto-pause (Prevents video from pausing automatically if video gets hidden.)
  - showSolutionButton : choix on|off — Override "Show Solution" button (This option determines if the "Show Solution" button will be shown for all questions, disabled for all or configured for each question individually.)
  - retryButton* : choix on|off — Override "Retry" button (This option determines if the "Retry" button will be shown for all questions, disabled for all or configured for each question individually.)
  - showBookmarksmenuOnLoad : booléen, défaut false — Start with bookmarks menu open (This function is not available on iPad when using YouTube as video source.)
  - showRewind10 : booléen, défaut false — Show button for rewinding 10 seconds
  - preventSkippingMode : choix none|forward|both, défaut none — Disable navigation (These options will disable user video navigation as specified.)
  - deactivateSound : booléen, défaut false — Deactivate sound (Enabling this option will deactivate the video's sound and prevent it from being switched on.)

Textes d'interface pré-remplis en français (ne pas fournir sauf besoin) : l10n.

## Exemple complet (validé : validateur officiel H5P + affichage)

Fichier `sources/exemples/video-interactive.md` (médias dans `sources/exemples/media/`).

````markdown
---
type: video-interactive
title: Les états de l'eau – vidéo interactive
language: fr
preset: entrainement
transcript: media/etats-eau.vtt
---
![Les états de l'eau](media/clip.webm)
Regarde la vidéo et réponds aux questions.

## 0:00 signet: Introduction

## 0:00 texte
L'eau existe sous trois états : **solide**, **liquide** et **gazeux**.

## 0:01 signet: Questions

## 0:01 qcm
À quelle température l'eau pure bout-elle (au niveau de la mer) ?
- [x] 100 °C
- [ ] 0 °C
  > Non : 0 °C est la température de fusion de la glace.
- [ ] 50 °C

## 0:02 vf
La glace est de l'eau à l'état solide.
- [x] Vrai
- [ ] Faux

```yaml
# ce que le raccourci ne couvre pas s'ajoute dans un bloc yaml (fusionné avec le Markdown)
interactiveVideo:
  summary:
    displayAt: 1
    task:
      library: resume
      md: |
        Choisis l'affirmation correcte.

        - [x] La vapeur d'eau est de l'eau à l'état gazeux.
        - [ ] La vapeur d'eau est de l'eau à l'état liquide.
```
````

Même activité entièrement en YAML (positions explicites) : `tests/fixtures/video-interactive.yaml.md`.
