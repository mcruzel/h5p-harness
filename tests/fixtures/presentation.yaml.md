---
type: presentation
title: Les formes géométriques – diaporama de révision
language: fr
preset: entrainement
---
```yaml
presentation:
  keywordListEnabled: true
  globalBackgroundSelector:
    fillGlobalBackground: "#f5f7fa"
  slides:
    # x, y, width, height : en % de la diapo (facultatifs : sans eux, mise en page automatique)
    - keywords:
        - main: Introduction
      elements:
        - x: 5
          y: 5
          width: 55
          height: 85
          action:
            library: texte
            text: |
              ## Les figures planes

              Une **figure plane** est une forme dessinée sur une surface plate.
              Dans ce diaporama, tu vas revoir :

              - le **cercle** ;
              - le **carré** ;
              - le **triangle**.
        - x: 62
          y: 20
          width: 33
          height: 49
          action:
            library: image
            file: /sources/exemples/media/cercle-bleu.png
            alt: Un cercle bleu
    - keywords:
        - main: Le cercle
      slideBackgroundSelector:
        fillSlideBackground: "#eef6ff"
      elements:
        - x: 3
          y: 4
          width: 62
          height: 92
          action:
            library: qcm
            md: |
              Quelles affirmations sont vraies pour un **cercle** de rayon 3 cm ?
              - [x] Son diamètre mesure 6 cm.
              - [ ] Son diamètre mesure 1,5 cm.
                > Non : le diamètre est le double du rayon.
              - [x] Tous ses points sont à 3 cm du centre.
        - x: 72
          y: 28
          width: 22
          height: 43
          action:
            library: forme
            type: circle
            shape:
              fillColor: "#3b82f6"
              borderColor: "#1e3a8a"
              borderWidth: 2
    - keywords:
        - main: Le triangle
      slideBackgroundSelector:
        fillSlideBackground: "#fff8e6"
      elements:
        - x: 3
          y: 4
          width: 46
          height: 92
          action:
            library: vf
            md: |
              La somme des angles d'un triangle est égale à 180°.
              - [x] Vrai
                > Exact : c'est une propriété de tous les triangles.
              - [ ] Faux
        - x: 51
          y: 4
          width: 46
          height: 92
          action:
            library: trous
            md: |
              Complète.

              Un triangle qui a trois côtés de même longueur est {{équilatéral}}.
          solution: Un triangle **équilatéral** a aussi trois angles de 60°.
```
