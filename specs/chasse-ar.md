# AR Scavenger (beta) — `chasse-ar`

H5P.ARScavenger 1.6 · alias : chasse-ar, arscavenger, ar-scavenger · syntaxe Markdown simplifiée : non (bloc ```yaml)

## Champs (bloc ```yaml, noms H5P)

`*` = obligatoire ; les autres champs ont une valeur par défaut ou sont facultatifs.

- showTitleScreen : booléen, défaut false — Afficher l'écran d'accueil (Si coché, le guide pour les créateurs de contenu affichera l'écran titre au démarrage.)
- titleScreen : groupe, conditionnel — Écran d'accueil
  - titleScreenIntroduction : texte riche (Markdown: a code em h2 h3 hr li ol pre strong u ul) — Introduction
  - titleScreenImage : sous-contenu, library: image — Image de l'écran titre
- markers : groupe — Marqueurs (groupe à un champ: écrire directement la valeur)
  - markers* : liste (min 1) — Marqueurs
    chaque élément :
      - markerImage : image (chemin ou URL) — Image du marqueur (originale) (Téléchargez l'image pour laquelle vous souhaitez créer un marqueur. L'image doit être carrée, sinon elle sera…)
      - markerPattern : fichier (chemin ou URL) — Image du marqueur (motif) (Télécharger cette image pour l'utiliser comme marqueur affiché sur un écran ou imprimé sur papier.)
      - actionType : choix h5p|model, défaut h5p — Type d’action (Action qui doit être déclenchée lorsque le marqueur est trouvé.)
      - interaction : groupe, conditionnel — Interaction
        - interaction* : sous-contenu, library: modele-3d | accordeon | agamotto | audio | enregistreur-audio | graphique | collage | cadenas | presentation | mots-croises | cartes | outil-documentation | glisser-deposer | glisser-mots | redaction | trous | trouver-zone | devinette | image | choix-images | image-interactive | carrousel | video-interactive | lien | marquer-mots | memory | qcm | questionnaire | quiz | choix-unique | resume | tableau | texte | frise | vf | video — Interaction
      - model : groupe, conditionnel — Modèle 3D
        - file : fichier (chemin ou URL) — Fichier du modèle 3D (Télécharger un fichier gITF (.glb / .gltf) ici. Le format préféré est « glTF 2.0 binary » dans un seul fichie…)
        - geometry : groupe — Géométrie
          - scale : groupe — Échelle (Redimensionnez le modèle vers le haut ou vers le bas pour qu'il corresponde à la taille de votre marqueur.)
            - scale : nombre, min 1, défaut 100 — Pourcentage
          - position : réglages — Position (Définir la position de décalage du modèle par rapport au marqueur.)
            x=0, y=0, z=0
          - rotation : réglages — Rotation (Régler la rotation en degrés.)
            x=0, y=0, z=0
- showEndScreen : booléen, défaut false — Afficher l'écran de fin (Si coché, afficher un écran de fin lorsque toutes les interactions sont terminées. L'écran de fin ne sera pas…)
- endScreen : groupe, conditionnel — Écran de fin
  - endScreenImage : sous-contenu, library: image — image de l'écran de fin
  - endScreenOutro : texte riche (Markdown: a code em h2 h3 hr li ol pre strong u ul) — Texte de l'écran de fin
  - overallFeedback : groupe — Feedback général (groupe à un champ: écrire directement la valeur)
    - overallFeedback : liste (min 1) — Définir un feedback personnalisé pour n'importe quelle gamme de note (Cliquez sur la touche « Ajouter une gamme » pour ajouter autant de gammes que nécessaire. Exemple : 0-20 % ma…)
      chaque élément :
        - from : nombre, min 0, max 100, défaut 0 — Gamme de notes
        - to : nombre, min 0, max 100, défaut 100
        - feedback : texte — Feedback pour une gamme de notes définie
- behaviour : réglages — Paramètres comportementaux
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
markers:
  - markerImage: ../media/triangle-vert.png
    # contournement : motif ARToolkit (.txt) généré à partir de l'image, comme le fait l'éditeur H5P
    markerPattern: chasse-ar-triangle.txt
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
    markerPattern: chasse-ar-carre.txt
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
