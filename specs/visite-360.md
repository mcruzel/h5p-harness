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
