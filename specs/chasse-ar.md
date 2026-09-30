# AR Scavenger (beta) — `chasse-ar`

H5P.ARScavenger 1.6 · alias : chasse-ar, arscavenger, ar-scavenger · syntaxe Markdown simplifiée : non (bloc ```yaml)

## Points d'attention

- Une image par marqueur (`markerImage`) : carrée, contrastée, **différente pour chaque marqueur**. Le harnais en calcule le motif ARToolKit (`markerPattern`) exactement comme l'éditeur H5P : ne pas le fournir.
- Les marqueurs à imprimer (image entourée d'un cadre noir) se téléchargent dans l'éditeur H5P de Moodle (bouton sous chaque marqueur, en modifiant l'activité).
- L'élève doit autoriser la caméra (page en HTTPS) ; sans caméra, le lecteur affiche « Impossible d'accéder à la caméra ».

## Champs (bloc ```yaml, noms H5P)

`*` = obligatoire ; les autres champs ont une valeur par défaut ou sont facultatifs. Libellés et descriptions : ceux de la bibliothèque (anglais) ; valeurs par défaut : en français.

- showTitleScreen : booléen, défaut false — Show start screen (If checked, the content will show the title screen when starting.)
- titleScreen : groupe, si showTitleScreen = True — Start screen
  - titleScreenIntroduction : texte riche (Markdown: a code em h2 h3 hr li ol pre strong u ul) — Introduction
  - titleScreenImage : sous-contenu, library: image — Title screen image
- markers : groupe — Markers (groupe à un champ: écrire directement la valeur)
  - markers* : liste (min 1) — Markers
    chaque élément :
      - markerImage : image (chemin ou URL) — Marker image (original) (Upload the image that you want to create a marker for. Should be a square image or it will be cropped. Keep in mind that you will need a unique marker image for every interaction.)
      - markerPattern : fichier (chemin ou URL) — Marker image (pattern) (Download this image to use as a marker displayed on a screen or printed on paper.) — **généré à partir de markerImage (ne pas fournir)**
      - actionType : choix h5p|model, défaut h5p — Action type (Action that should be triggered when the marker is found.)
      - interaction : groupe, si actionType = h5p — Interaction
        - interaction* : sous-contenu, library: modele-3d | accordeon | agamotto | audio | enregistreur-audio | graphique | collage | cadenas | presentation | mots-croises | cartes | outil-documentation | glisser-deposer | glisser-mots | redaction | trous | trouver-zone | devinette | image | choix-images | image-interactive | carrousel | video-interactive | lien | marquer-mots | memory | qcm | questionnaire | quiz | choix-unique | resume | tableau | texte | frise | vf | video — Interaction
      - model : groupe, si actionType = model — 3D Model
        - file : fichier (chemin ou URL) — 3D model file (Upload a glTF (.glb / .gltf) file here. The preferred format is "glTF 2.0 binary" in a single file.)
        - geometry : groupe — Geometry
          - scale : groupe — Scale (Scale the model up or down to match your marker size.)
            - scale : nombre, min 1, défaut 100 — Percentage
          - position : réglages — Position (Set the model's offset position relative to the marker.)
            x=0, y=0, z=0
          - rotation : réglages — Rotation (Set the rotation in degrees.)
            x=0, y=0, z=0
- showEndScreen : booléen, défaut false — Show end screen (If checked, show an end screen when all interactions have been completed. The end screen will not be available if you only use 3D models though.)
- endScreen : groupe, si showEndScreen = True — End screen
  - endScreenImage : sous-contenu, library: image — end screen image
  - endScreenOutro : texte riche (Markdown: a code em h2 h3 hr li ol pre strong u ul) — End screen text
  - overallFeedback : groupe — Overall Feedback (groupe à un champ: écrire directement la valeur)
    - overallFeedback : liste (min 1) — Define custom feedback for any score range (Click the "Add range" button to add as many ranges as you need. Example: 0-20% Bad score, 21-91% Average Score, 91-100% Great Score!)
      chaque élément :
        - from : nombre, min 0, max 100, défaut 0 — Score Range
        - to : nombre, min 0, max 100, défaut 100
        - feedback : texte — Feedback for defined score range
- behaviour : réglages — Behavioural settings
  enableRetry=true, overrideShowSolutionButton=useBehavioural (useBehavioural|always|n…, overrideRetryButton=useBehavioural (useBehavioural|always|n…, fallbackHeight=400

Textes d'interface pré-remplis en français (ne pas fournir sauf besoin) : l10n, a11y.

## Exemple complet (validé : validateur officiel H5P + affichage)

Fichier `tests/examples/chasse-ar.md` (médias dans `tests/media/`).

````markdown
---
type: chasse-ar
title: Chasse aux formes en réalité augmentée
language: fr
preset: entrainement
---
```yaml
showTitleScreen: true
titleScreen:
  titleScreenIntroduction: |
    ## Chasse aux formes
    Imprime les marqueurs, cache-les dans la classe, puis vise-les avec la caméra
    pour débloquer les questions.
# le motif de chaque marqueur (markerPattern) est calculé à partir de son image
markers:
  - markerImage: ../media/triangle-vert.png
    actionType: h5p
    interaction:
      interaction:
        library: qcm
        md: |
          Combien de côtés possède un triangle ?
          - [x] 3
          - [ ] 4
          - [ ] 5
  - markerImage: ../media/carre-rouge.png
    actionType: h5p
    interaction:
      interaction:
        library: vf
        md: |
          Un carré a quatre angles droits.
          - [x] Vrai
          - [ ] Faux
showEndScreen: true
endScreen:
  endScreenOutro: Bravo, tu as trouvé **tous les marqueurs** !
```
````
