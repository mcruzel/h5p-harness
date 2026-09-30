# Game Map — `carte-jeu`

H5P.GameMap 1.9 · alias : carte-jeu, gamemap, game-map · syntaxe Markdown simplifiée : non (bloc ```yaml)

## Points d'attention

- Chaque étape : `label` + `contentsList` (ses exercices). Le harnais complète comme l'éditeur de carte : identifiants, positions (`telemetry`, étapes réparties le long d'un chemin sinueux si absentes), voisinage symétrique (parcours linéaire dans l'ordre si aucun `neighbors`), chemins (`paths`) et étape de départ (la première).
- `neighbors` : indices des étapes voisines, **à partir de 0**.
- Étape spéciale (fin, vie ou temps en plus, lien, téléportation) : uniquement avec `specialStageType` ; toute valeur rend l'étape spéciale et ses exercices sont ignorés.
- Une image de fond (`mapOptions.backgroundSettings.backgroundImage`) donne sa forme à la carte ; `telemetry` x, y, width, height sont des textes en % de cette image.

## Champs (bloc ```yaml, noms H5P)

`*` = obligatoire ; les autres champs ont une valeur par défaut ou sont facultatifs. Libellés et descriptions : ceux de la bibliothèque (anglais) ; valeurs par défaut : en français.

- showTitleScreen : booléen, défaut false — Show title screen (If checked, a title screen will show up when starting.)
- titleScreen : groupe — Title screen
  - titleScreenIntroduction : texte riche (Markdown: a code del em hr li ol pre s strong sub sup u ul), défaut  — Introduction
  - titleScreenMedium : sous-contenu, library: image | video — Title screen media
- headline : texte — Headline (Optional headline for the titlebar.)
- gamemaps* : liste (min 1) — Game maps
  chaque élément :
    - elements : liste — Elements
      chaque élément :
        - id : texte, facultatif — identifiant unique de l'étape (généré)
        - label* : texte — Stage label (This label will be displayed on top of your exercise and will help you to connect different stages with one another.)
        - time : réglages — Time limit (Define timer related settings.)
          timeLimit=…, timeoutWarning=…
        - accessRestrictions : groupe — Access restrictions (Define restrictions for unlocking.)
          - allOrAnyRestrictionSet : choix all|any, défaut all — All or any restriction set (Choose if all or any of the following restrictions need to be met.)
          - restrictionSetList : liste — Restriction sets
            chaque élément :
              - allOrAnyRestriction : choix all|any, défaut any — All or any restriction (Choose if all or any of the following restrictions need to be met.)
              - restrictionList : liste — Restrictions
                chaque élément :
                  - restrictionType : choix totalScore|stageScore|stageScorePercentage|stageProgress|time, défaut totalScore — Restriction type
                  - totalScoreGroup : réglages — Total score
                    totalScoreOperator=greaterThan (lessThan|equalTo|notEqualT…, totalScoreValue=…
                  - stageScoreGroup : réglages — Stage score
                    stageScoreId= (), stageScoreOperator=before (lessThan|equalTo|notEqualTo|gre…, stageScoreValue=…
                  - stageScorePercentageGroup : réglages — Stage score percentage
                    stageScorePercentageId= (), stageScorePercentageOperator=before (lessThan|equalTo|notEqualTo|gre…, stageScorePercentageValue=…
                  - stageProgressGroup : réglages — Stage progress
                    stageProgressId= (), stageProgressOperator=is (is|isNot), stageProgressValue=open (unstarted|opened|completed|cleare…
                  - timeGroup : groupe — Time
                    - timeOperator : choix before|is|is not|after, défaut before — Operator for time
                    - timeValue : texte — Time to compare to
        - contentsList* : liste (min 1) — Contents
          chaque élément :
            - contentType* : sous-contenu, library: accordeon | agamotto | audio | enregistreur-audio | explorateur-choix | cadenas | presentation | mots-croises | cartes | glisser-deposer | glisser-mots | redaction | trous | trouver-zone | image | choix-images | image-interactive | carrousel | video-interactive | marquer-mots | memory | qcm | quiz | choix-unique | onglets | texte | transcription | vf | video | rayons-x — Stage content (Choose the type of content you would like to add.)
            - livesSettings : réglages — Lives
              livesMode=useBehavioural (useBehavioural|never|cu…, passPercentage=100
        - specialStageType : choix finish|extra-life|extra-time|link|teleport — Special stage type — **à omettre pour une étape normale : toute valeur en fait une étape spéciale dont les exercices sont ignorés**
        - specialStageExtraLives : nombre, min 1, défaut 1, si specialStageType = extra-life — Number of extra lives (Set how many lives the user will get when entering this stage.)
        - specialStageExtraTime : nombre, min 1, défaut 1, si specialStageType = extra-time — Number of seconds of extra time (Set how many seconds the user will gain for the global time limit when entering this stage.)
        - specialStageLinkURL : texte, si specialStageType = link — URL to link to (Set where the user should be sent to when opening this stage.)
        - specialStageLinkTarget : choix _blank|_parent, défaut _blank, si specialStageType = link — Place to open link in
        - specialStageTeleportTarget : choix , si specialStageType = teleport — Teleport stage to teleport to (Note that you always need to pair two teleport stages and that the following list only shows teleport stages that are not linked to another teleport stage yet.)
        - alwaysVisible : booléen, défaut false — Always visible (If checked, this stage will always be visible, even if the map's visibility range settings dictate otherwise.)
        - overrideSymbol : booléen, défaut false — Override lock symbol (If checked, locked stages will not use the lock symbol, but the symbol for the special stage type.)
        - stageBehaviour : réglages — Stage behaviour
          canBeStartStage=false, randomExercises=false, randomExerciseCount=1, randomExerciseTotalScore=…
        - scoreScaling : groupe — Score scaling
          - scalingMode : choix totalScore|maxScore|weightedExercises, défaut weightedExercises — Scaling mode (Choose what scaling should be based on)
          - scoreScalingList : liste — Content score customizations (Adjust the weights/total scores of exercises to customize scoring)
            chaque élément :
              - subContentId* : texte — Subcontent id
              - weight : texte, défaut 1 — Weight
              - isTask : booléen, défaut false — Is task
          - weightIsPercentage : booléen, défaut false — Weight is percentage
        - neighbors : choix  (plusieurs) — Connected stages — **indices des étapes voisines, à partir de 0 (voisinage rendu symétrique) ; absent partout : parcours linéaire dans l'ordre**
        - telemetry : groupe facultatif — position de l'étape x, y, width, height (textes, en % de la carte) ; défaut : étapes réparties le long d'un chemin sinueux
    - paths : liste — Paths — **généré à partir de `neighbors` : ne donner (avec from/to) que pour un style de chemin particulier**
      chaque élément :
        - from : nombre — indice de l'étape de départ du chemin (0 = première)
        - to : nombre — indice de l'étape d'arrivée du chemin
        - visualsType : choix global|custom, défaut global — Visual settings
        - customVisuals : réglages — Custom visual settings
          colorPath=rgba(0, 0, 0, 0.7), pathWidth=0.2 (0.1|0.2|0.3), pathStyle=dotted (solid|dotted|dashed|double)
    - mapOptions : groupe — Options for this map
      - name : texte — Name (Name for identifying the map.)
      - backgroundSettings : groupe — Background
        - backgroundImage : image (chemin ou URL) — Background image (Select an image to use as the background of the game map.)
        - backgroundDescription : texte — Background description (If the background is not just illustration but contains relevant information, describe the image here.)
        - backgroundColor : couleur #rrggbb, défaut rgb(255, 255, 255) — Background color (Choose a color to use as the background of the game map.)
      - audioSettings : groupe — Audio settings
        - music : audio (chemin ou URL) — Individual background music
- endScreen : groupe — End screen
  - noSuccess : groupe — User not successful
    - endScreenTextNoSuccess : texte riche (Markdown: a code del em hr li ol pre s strong sub sup u ul), défaut  — Message (user not successful)
    - endScreenMediumNoSuccess : sous-contenu, library: image | video — End screen media (user not successful)
  - success : groupe — User successful
    - endScreenTextSuccess : texte riche (Markdown: a code del em hr li ol pre s strong sub sup u ul), défaut  — Message (user successful)
    - endScreenMediumSuccess : sous-contenu, library: image | video — End screen media (user successful)
  - overallFeedback : groupe — Overall Feedback (groupe à un champ: écrire directement la valeur)
    - overallFeedback : liste (min 1) — Define custom feedback for any score range (Click the "Add range" button to add as many ranges as you need. Example: 0-20% Bad score, 21-91% Average Score, 91-100% Great Score!)
      chaque élément :
        - from : nombre, min 0, max 100, défaut 0 — Score Range
        - to : nombre, min 0, max 100, défaut 100
        - feedback : texte — Feedback for defined score range
- visual : réglages — Visual settings
  
- audio : groupe — Audio settings
  - music : audio (chemin ou URL) — Background music
  - muteDuringExercise : booléen, défaut true — Mute background music when taking exercises
  - ambient : groupe — Events
    - clickStageLocked : audio (chemin ou URL) — Click on locked stage (Will be played on the map when clicking on a locked stage.)
    - checkExerciseNotFullScore : audio (chemin ou URL) — Check exercise (not full score) (Will be played when an answer is checked and the user did not get full score.)
    - checkExerciseFullScore : audio (chemin ou URL) — Check exercise (full score) (Will be played when an answer is checked and the user did get full score.)
    - teleport : audio (chemin ou URL) — Teleport to a different stage (Will be played on the map when the user teleports to another stage.)
    - unlockStage : audio (chemin ou URL) — Unlocking a stage (Will be played on the map when a stage gets unlocked.)
    - openExercise : audio (chemin ou URL) — Open exercise (Will be played when an exercise is opened.)
    - closeExercise : audio (chemin ou URL) — Close exercise (Will be played when an exercise is closed.)
    - showDialog : audio (chemin ou URL) — Show dialog (Will be played when a confirmation dialog is shown.)
    - fullScore : audio (chemin ou URL) — Full score (Will be played when the user reaches full score for the map.)
    - lostLife : audio (chemin ou URL) — Lost a life (Will be played when the user loses a life.)
    - gainedLife : audio (chemin ou URL) — Gained life (Will be played when the user gains a life.)
    - gameOver : audio (chemin ou URL) — Game over (Will be played when the user is game over.)
    - extraTime : audio (chemin ou URL) — Gained extra time (Will be played when the user gains extra time.)
    - timeoutWarning : audio (chemin ou URL) — Timeout warning (Will be played when the user is running out of time for an exercise or if the global time runs out.)
    - endscreenNoSuccess : audio (chemin ou URL) — End screen (not full score) (Will be played on the end screen if the user did not get full score.)
    - endscreenSuccess : audio (chemin ou URL) — End screen (full score) (Will be played on the end screen if the user got full score.)
- behaviour : réglages — Behavioural settings
  lives=…, timeLimitGlobal=…, timeoutWarningGlobal=…, finishScore=…, enableRetry=true, enableSolutionsButton=true

Textes d'interface pré-remplis en français (ne pas fournir sauf besoin) : l10n, a11y.

## Exemple complet (validé : validateur officiel H5P + affichage)

Fichier `sources/exemples/carte-jeu.md` (médias dans `sources/exemples/media/`).

````markdown
---
type: carte-jeu
title: Voyage au pays des fractions
language: fr
preset: entrainement
---
```yaml
showTitleScreen: true
titleScreen:
  titleScreenIntroduction: |
    **Voyage au pays des fractions**

    Traverse la carte en réussissant chaque étape !
headline: Voyage au pays des fractions
gamemaps:
  - mapOptions:
      name: La vallée
      backgroundSettings:
        backgroundImage: media/paysage.jpg
        backgroundDescription: Une vallée avec une maison et un arbre
    # positions en % de l'image ; sans « neighbors », les étapes forment un parcours dans l'ordre
    elements:
      - id: etape-vocabulaire
        label: Le vocabulaire
        telemetry: {x: "10", y: "70", width: "6", height: "9"}
        stageBehaviour: {canBeStartStage: true}
        contentsList:
          - contentType:
              library: qcm
              md: |
                Dans la fraction 3/4, comment s'appelle le nombre 4 ?
                - [x] Le dénominateur
                - [ ] Le numérateur
                  > Non : le numérateur est le nombre du haut (3).
                - [ ] Le quotient
      - id: etape-pont
        label: Le pont
        telemetry: {x: "45", y: "55", width: "6", height: "9"}
        contentsList:
          - contentType:
              library: trous
              md: |
                Complète.

                La moitié d'un gâteau correspond à la fraction 1/{{2}}.
      - id: etape-chateau
        label: Le château
        telemetry: {x: "80", y: "30", width: "6", height: "9"}
        contentsList:
          - contentType:
              library: vf
              md: |
                La fraction 2/4 est égale à la fraction 1/2.
                - [x] Vrai
                - [ ] Faux
          - contentType:
              library: image
              file: media/etoile-orange.png
              alt: Une étoile, récompense de fin de parcours
endScreen:
  success:
    endScreenTextSuccess: Bravo, tu as traversé le pays des fractions !
  noSuccess:
    endScreenTextNoSuccess: Tu peux recommencer pour améliorer ton score.
```
````
