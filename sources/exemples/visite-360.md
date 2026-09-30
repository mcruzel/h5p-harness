---
type: visite-360
title: Visite virtuelle d'un village de montagne
language: fr
preset: decouverte
license: CC BY-SA 4.0
authors: Équipe d'histoire-géographie
---
```yaml
threeImage:
  startSceneId: 0
  scenes:
    - sceneId: 0
      sceneType: 360
      scenename: Le belvédère
      scenesrc: media/panorama.jpg
      scenedescription: Tourne-toi pour observer les **éléments du paysage** autour du belvédère.
      cameraStartPosition: "0,0"
      interactions:
        - labelText: Le glacier
          interactionpos: "0.8,0.2"
          action:
            library: texte
            text: |
              Un **glacier** est une accumulation de glace qui s'écoule lentement.
              Il recule depuis la fin du XIXᵉ siècle.
        - labelText: Plan du site
          interactionpos: "-0.9,0"
          action: {library: image, file: media/paysage.jpg, alt: Plan simplifié du village et de ses abords}
        - labelText: Descendre au village
          interactionpos: "2.4,-0.1"
          action: {library: gotoscene, nextSceneId: 1}
    - sceneId: 1
      sceneType: static
      scenename: Le village
      scenesrc: media/paysage.jpg
      scenedescription: Le village se trouve au fond de la vallée.
      cameraStartPosition: "0,0"
      showBackButton: true
      iconType: plus
      interactions:
        - labelText: Question
          interactionpos: "45%,75%"
          action:
            library: choix-unique
            md: |
              ## Quelle activité humaine est visible au premier plan ?
              - [x] L'agriculture (une prairie)
              - [ ] L'industrie
              - [ ] Le tourisme de masse
        - labelText: Retour au belvédère
          interactionpos: "85%,20%"
          action: {library: gotoscene, nextSceneId: 0}
behaviour:
  sceneRenderingQuality: medium
```
