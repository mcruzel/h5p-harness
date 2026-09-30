---
type: onglets
title: Les trois états de l'eau
language: fr
preset: entrainement
---
```yaml
tabs:
  # metadata.title = titre de l'onglet
  - library: colonne
    metadata: {title: Solide}
    md: |
      ## L'état solide
      La **glace** a une forme propre : elle ne coule pas.
      L'eau devient solide en dessous de 0 °C.

      ![Un cube de glace (schéma)](/sources/exemples/media/carre-rouge.png)
  - library: colonne
    metadata: {title: Liquide}
    md: |
      ## L'état liquide
      L'eau **liquide** n'a pas de forme propre : elle prend la forme du récipient.

      ::: qcm
      Quelle est la particularité de l'eau liquide ?
      - [x] Elle prend la forme du récipient.
      - [ ] Elle garde toujours la même forme.
      - [ ] Elle est invisible.
      :::
  - library: colonne
    metadata: {title: Gazeux}
    md: |
      ## L'état gazeux
      La **vapeur d'eau** est un gaz invisible.

      ::: vf
      La buée sur une vitre est de la vapeur d'eau.
      - [ ] Vrai
        > Non : la buée est formée de fines gouttelettes d'eau liquide.
      - [x] Faux
      :::
behaviour:
  tabPlacement: top
```
