---
type: mur-infos
title: Mur d'infos – les planètes telluriques
language: fr
---
```yaml
infoWall:
  header: Les planètes telluriques du système solaire
  propertiesGroup:
    properties:
      # panelTitle n'est pas affiché par H5P : le nom de la planète est une propriété
      - label: Planète
        showLabel: false
        styling: {bold: true}
      - label: Type
        showLabel: true
      - label: Distance moyenne au Soleil
        showLabel: true
      - label: Nombre de satellites naturels
        showLabel: true
        styling: {bold: true}
  panels:
    - panelTitle: Mercure
      entries:
        - Mercure
        - Planète rocheuse
        - 58 millions de km
        - "0"
      keywords: chaude, petite
    - panelTitle: Vénus
      entries:
        - Vénus
        - Planète rocheuse
        - 108 millions de km
        - "0"
      keywords: étoile du berger, effet de serre
    - panelTitle: La Terre
      image: {library: image, file: ../media/cercle-bleu.png, alt: La planète bleue}
      entries:
        - La Terre
        - Planète rocheuse
        - 150 millions de km
        - 1 (la Lune)
      keywords: vie, eau liquide
    - panelTitle: Mars
      image: {library: image, file: ../media/carre-rouge.png, alt: La planète rouge}
      entries:
        - Mars
        - Planète rocheuse
        - 228 millions de km
        - 2 (Phobos et Déimos)
      keywords: planète rouge
  behaviour:
    imageWidth: 100
    imageHeight: 75
```
