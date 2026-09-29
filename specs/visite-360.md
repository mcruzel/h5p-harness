# Virtual Tour (360) — `visite-360`

H5P.ThreeImage 0.5 · alias : visite-360, threeimage, three-image · syntaxe Markdown simplifiée : non (bloc ```yaml)

## Champs (bloc ```yaml, noms H5P)

`*` = obligatoire ; les autres champs ont une valeur par défaut ou sont facultatifs.

- threeImage : groupe — Editeur Three Image
  - scenes : liste (min 0) — Scènes
    chaque élément :
      - sceneType : choix 360|static, défaut 360 — Type de scène
      - showBackButton : booléen, défaut true, conditionnel — Afficher un bouton "Retour"
      - sceneId* : nombre
      - scenename* : texte — Titre de la scène
      - scenesrc : image (chemin ou URL) — Image de fond de la scène
      - scenedescription : texte riche (Markdown: code em strong) — Description de la scène
      - cameraStartPosition* : texte
      - interactions : liste (min 0)
        chaque élément :
          - labelText : texte — Vignette
          - label : réglages — Label Settings
            labelPosition=inherit (inherit|right|left|top|bottom), showLabel=inherit (inherit|show|hide)
          - action* : sous-contenu, library: gotoscene | texte | image | audio | video | resume | choix-unique
          - interactionpos* : texte
      - iconType : choix arrow|plus, défaut arrow — Style du bouton
      - audio : audio (chemin ou URL) — Piste audio
  - startSceneId : nombre, défaut 0
  - audio : audio (chemin ou URL) — Piste audio
- behaviour : groupe — Paramètres comportementaux
  - audio : audio (chemin ou URL) — Piste audio globale
  - sceneRenderingQuality : choix high|medium|low, défaut high — Qualité de rendu de la scène
  - label : réglages — Paramètres de vignette
    labelPosition=right (right|left|top|bottom), showLabel=true

Textes d'interface pré-remplis en français (ne pas fournir sauf besoin) : l10n.

## Exemple complet (validé : validateur officiel H5P + affichage)

Fichier `tests/examples/visite-360.md` (médias dans `tests/media/`).

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
      scenesrc: ../media/panorama.jpg
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
          action: {library: image, file: ../media/paysage.jpg, alt: Plan simplifié du village et de ses abords}
        - labelText: Descendre au village
          interactionpos: "2.4,-0.1"
          action: {library: gotoscene, nextSceneId: 1}
    - sceneId: 1
      sceneType: static
      scenename: Le village
      scenesrc: ../media/paysage.jpg
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
