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
  - markerImage: media/triangle-vert.png
    actionType: h5p
    interaction:
      interaction:
        library: qcm
        md: |
          Combien de côtés possède un triangle ?
          - [x] 3
          - [ ] 4
          - [ ] 5
  - markerImage: media/carre-rouge.png
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
