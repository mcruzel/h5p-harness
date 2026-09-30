# Virtual Tour (360) — `visite-360`

H5P.ThreeImage 0.5 · alias : visite-360, threeimage, three-image · syntaxe Markdown simplifiée : non (bloc ```yaml)

## Points d'attention

- Chaque scène a un `sceneId` (nombre) ; une interaction « aller à la scène » pointe vers `gotoscene.nextSceneId`.
- `cameraStartPosition` (obligatoire) et `interactionpos` : `"lacet,tangage"` en **radians** pour une scène 360 (ex. `"-2.1,0.3"`), `"x%,y%"` pour une scène statique (ex. `"45%,30%"`).
- Image de scène 360 : panorama équirectangulaire (rapport 2:1).

## Champs (bloc ```yaml, noms H5P)

`*` = obligatoire ; les autres champs ont une valeur par défaut ou sont facultatifs. Libellés et descriptions : ceux de la bibliothèque (anglais) ; valeurs par défaut : en français.

- threeImage : groupe — Three Image Editor
  - scenes : liste (min 0) — Scenes
    chaque élément :
      - sceneType : choix 360|static, défaut 360 — Scene type
      - showBackButton : booléen, défaut true, si sceneType = static — Display "Back" button (Display button for navigating back to your previous scene)
      - sceneId* : nombre
      - scenename* : texte — Scene Title (Used to identify the scene)
      - scenesrc* : image (chemin ou URL) — Scene Background
      - scenedescription : texte riche (Markdown: code em strong) — Scene Description (A text that can describe the scene for the end-user)
      - cameraStartPosition* : texte
      - interactions : liste (min 0)
        chaque élément :
          - labelText : texte — Label (If left blank no label will be displayed and we'll try to use the title field for screen readers)
          - label : réglages — Label Settings
            labelPosition=inherit (inherit|right|left|top|bottom), showLabel=inherit (inherit|show|hide)
          - action* : sous-contenu, library: gotoscene | texte | image | audio | video | resume | choix-unique
          - interactionpos* : texte
      - iconType : choix arrow|plus, défaut arrow — Button style (Decide how buttons pointing to this scene should look. For scenes that are static and does not lead to new scenes, we recommend the "More information" button.)
      - audio : audio (chemin ou URL) — Audio Track (Add an audio track that's specific for this scene.)
  - startSceneId : nombre, défaut 0
  - audio : audio (chemin ou URL) — Audio track
- behaviour : groupe — Behavioral settings (These options will let you control how the world behaves.)
  - audio : audio (chemin ou URL) — Global Audio (Add an audio track that's available for all of the scenes by default.)
  - sceneRenderingQuality : choix high|medium|low, défaut high — Scene rendering quality (Choose the amount of width and height segments used to render a scene. This directly affects the quality level of the scene, try increasing the quality if a scene looks "blocky" or "waves" are seen within the scenes. No…)
  - label : réglages — Label settings
    labelPosition=right (right|left|top|bottom), showLabel=true

Textes d'interface pré-remplis en français (ne pas fournir sauf besoin) : l10n.

## Exemple complet (validé : validateur officiel H5P + affichage)

Fichier `sources/exemples/visite-360.md` (médias dans `sources/exemples/media/`).

````markdown
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
````
