---
type: glisser-deposer
title: Polygone ou pas ? Classe les figures
language: fr
preset: entrainement
---
```yaml
# x, y en % de la zone ; width, height en em (1 em = 16 px pour une zone de 620 × 310)
question:
  settings:
    background: /sources/exemples/media/paysage.jpg
    size: {width: 620, height: 310}
  task:
    elements:
      - type: {library: image, file: /sources/exemples/media/carre-rouge.png, alt: Un carré rouge}
        dropZones: [0]
        x: 2
        y: 6
        width: 5
        height: 3.75
      - type: {library: image, file: /sources/exemples/media/triangle-vert.png, alt: Un triangle vert}
        dropZones: [0]
        x: 19
        y: 6
        width: 5
        height: 3.75
      - type: {library: image, file: /sources/exemples/media/cercle-bleu.png, alt: Un disque bleu}
        dropZones: [1]
        x: 2
        y: 36
        width: 5
        height: 3.75
      - type: {library: texte, text: un losange}
        dropZones: [0]
        x: 19
        y: 40
        width: 5.5
        height: 2
      - type: {library: texte, text: un ovale}
        dropZones: [1]
        x: 2
        y: 70
        width: 5.5
        height: 2
    dropZones:
      - label: Polygones
        showLabel: true
        correctElements: [0, 1, 3]
        autoAlign: true
        x: 40
        y: 12
        width: 11
        height: 16
        tipsAndFeedback:
          tip: Un polygone n'a que des côtés **droits**.
      - label: Non polygones
        showLabel: true
        correctElements: [2, 4]
        autoAlign: true
        x: 70
        y: 12
        width: 11
        height: 16
        tipsAndFeedback:
          feedbackOnIncorrect: Une figure avec un bord courbe n'est pas un polygone.
```
