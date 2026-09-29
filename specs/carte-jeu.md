# Game Map — `carte-jeu`

H5P.GameMap 1.9 · alias : carte-jeu, gamemap, game-map · syntaxe Markdown simplifiée : non (bloc ```yaml)

## Champs (bloc ```yaml, noms H5P)

`*` = obligatoire ; les autres champs ont une valeur par défaut ou sont facultatifs.

- showTitleScreen : booléen, défaut false — Afficher l'écran titre (Si cette case est cochée, un écran titre s'affichera au démarrage.)
- titleScreen : groupe — Écran titre
  - titleScreenIntroduction : texte riche (Markdown: a code del em hr li ol pre s strong sub sup u ul), défaut  — Introduction
  - titleScreenMedium : sous-contenu, library: image | video — Média de l'écran titre
- headline : texte — En-tête (Titre facultatif pour la barre de titre.)
- gamemaps* : liste (min 1) — Cartes de jeu
  chaque élément :
    - elements : liste — Eléments
      chaque élément :
        - label* : texte — Étiquette de l'étape (Cette étiquette sera affichée au-dessus de votre exercice et vous aidera à relier les différentes étapes entr…)
        - time : réglages — Limite de temps (Définissez les paramètres liés à la minuterie.)
          timeLimit=…, timeoutWarning=…
        - accessRestrictions : groupe — Restrictions d'accès (Définissez les restrictions de déverrouillage.)
          - allOrAnyRestrictionSet : choix all|any, défaut all — All or any restriction set (Choisissez si toutes les restrictions suivantes doivent être respectées ou seulement l'une d'entre elles.)
          - restrictionSetList : liste — Restriction sets
            chaque élément :
              - allOrAnyRestriction : choix all|any, défaut any — All or any restriction (Choisissez si toutes les restrictions suivantes doivent être respectées ou seulement l'une d'entre elles.)
              - restrictionList : liste — Restrictions
                chaque élément :
                  - restrictionType : choix totalScore|stageScore|stageScorePercentage|stageProgress|time, défaut totalScore — Type de restriction
                  - totalScoreGroup : réglages — Score total
                    totalScoreOperator=greaterThan (lessThan|equalTo|notEqualT…, totalScoreValue=…
                  - stageScoreGroup : réglages — Score d'étape
                    stageScoreId= (), stageScoreOperator=before (lessThan|equalTo|notEqualTo|gre…, stageScoreValue=…
                  - stageScorePercentageGroup : réglages — Stage score percentage
                    stageScorePercentageId= (), stageScorePercentageOperator=before (lessThan|equalTo|notEqualTo|gre…, stageScorePercentageValue=…
                  - stageProgressGroup : réglages — Progression d'étape
                    stageProgressId= (), stageProgressOperator=is (is|isNot), stageProgressValue=open (unstarted|opened|completed|cleare…
                  - timeGroup : groupe — Temps
                    - timeOperator : choix before|is|is not|after, défaut before — Opérateur pour le temps
                    - timeValue : texte — Temps à comparer à
        - contentsList* : liste (min 1) — Contenus
          chaque élément :
            - contentType* : sous-contenu, library: accordeon | agamotto | audio | enregistreur-audio | explorateur-choix | cadenas | presentation | mots-croises | cartes | glisser-deposer | glisser-mots | redaction | trous | trouver-zone | image | choix-images | image-interactive | carrousel | video-interactive | marquer-mots | memory | qcm | quiz | choix-unique | onglets | texte | transcription | vf | video | rayons-x — Contenu de l'étape (Choisissez le type de contenu que vous souhaitez ajouter.)
            - livesSettings : réglages — Vies
              livesMode=useBehavioural (useBehavioural|never|cu…, passPercentage=100
        - specialStageType* : choix finish|extra-life|extra-time|link|teleport — Type d'étape spéciale
        - specialStageExtraLives : nombre, min 1, défaut 1 — Nombre de vies supplémentaires (Définissez le nombre de vies que l'utilisateur obtiendra en entrant dans cette étape.)
        - specialStageExtraTime : nombre, min 1, défaut 1 — Nombre de secondes supplémentaires (Définissez le nombre de secondes que l'utilisateur gagnera en entrant dans cette étape.)
        - specialStageLinkURL* : texte — URL vers laquelle renvoyer (Définissez où l'utilisateur doit être renvoyé lors de l'ouverture de cette étape.)
        - specialStageLinkTarget : choix _blank|_parent, défaut _blank — Endroit pour ouvrir le lien dans
        - specialStageTeleportTarget : choix  — Teleport stage to teleport to (Note that you always need to pair two teleport stages and that the following list only shows teleport stages …)
        - alwaysVisible : booléen, défaut false — Toujours visible (Si cette case est cochée, cette étape sera toujours visible, même si les paramètres de plage de visibilité de…)
        - overrideSymbol : booléen, défaut false — Remplacer le symbole de verrouillage (Si cette case est cochée, les épreuves verrouillées n'utiliseront pas le symbole du cadenas, mais le symbole …)
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
        - neighbors* : choix  (plusieurs) — Etapes connectées
    - paths : liste — Chemins
      chaque élément :
        - visualsType : choix global|custom, défaut global — Paramètres visuels
        - customVisuals : réglages — Paramètres visuels personnalisés
          colorPath=rgba(0, 0, 0, 0.7), pathWidth=0.2 (0.1|0.2|0.3), pathStyle=dotted (solid|dotted|dashed|double)
    - mapOptions : groupe — Options for this map
      - name : texte — Name (Name for identifying the map.)
      - backgroundSettings : groupe — Arrière-plan
        - backgroundImage : image (chemin ou URL) — Image d'arrière-plan (Sélectionnez une image à utiliser comme arrière-plan de la carte du jeu.)
        - backgroundDescription : texte — Background description (If the background is not just illustration but contains relevant information, describe the image here.)
        - backgroundColor : couleur #rrggbb, défaut rgb(255, 255, 255) — Couleur d'arrière-plan (Choisissez une couleur à utiliser comme arrière-plan de la carte du jeu.)
      - audioSettings : groupe — Audio settings
        - music : audio (chemin ou URL) — Individual background music
- endScreen : groupe — Écran de fin
  - noSuccess : groupe — L'utilisateur n'a pas réussi
    - endScreenTextNoSuccess : texte riche (Markdown: a code del em hr li ol pre s strong sub sup u ul), défaut  — Message (l'utilisateur n'a pas réussi)
    - endScreenMediumNoSuccess : sous-contenu, library: image | video — Média de l'écran de fin (l'utilisateur n'a pas réussi)
  - success : groupe — Utilisateur réussi
    - endScreenTextSuccess : texte riche (Markdown: a code del em hr li ol pre s strong sub sup u ul), défaut  — Message (Utilisateur réussi)
    - endScreenMediumSuccess : sous-contenu, library: image | video — Média de l'écran de fin (utilisateur réussi)
  - overallFeedback : groupe — Commentaires globaux (groupe à un champ: écrire directement la valeur)
    - overallFeedback : liste (min 1) — Définir des commentaires personnalisés pour n’importe quelle plage de… (Clique le "Ajouter une plage" bouton pour ajouter autant de plages que nécessaire. Exemple: 0-20% Mauvais sco…)
      chaque élément :
        - from : nombre, min 0, max 100, défaut 0 — Plage de scores
        - to : nombre, min 0, max 100, défaut 100
        - feedback : texte — Commentaires pour une plage de scores définie
- visual : réglages — Paramètres visuels
  
- audio : groupe — Paramètres audio
  - music : audio (chemin ou URL) — Musique de fond
  - muteDuringExercise : booléen, défaut true — Couper la musique de fond pendant l'exercice
  - ambient : groupe — Événements
    - clickStageLocked : audio (chemin ou URL) — Clic sur une étape verrouillée (Sera joué sur la carte lors d'un clic sur une étape verrouillée.)
    - checkExerciseNotFullScore : audio (chemin ou URL) — Vérification de  l'exercice (exercice incomplet) (Sera joué lorsqu'une réponse est vérifiée et que l'utilisateur n'a pas obtenu le score total.)
    - checkExerciseFullScore : audio (chemin ou URL) — Vérification de l'exercice (exercice complet) (Sera joué lorsqu'une réponse est vérifiée et que l’utilisateur a obtenu le score total.)
    - teleport : audio (chemin ou URL) — Teleport to a different stage (Will be played on the map when the user teleports to another stage.)
    - unlockStage : audio (chemin ou URL) — Déverrouillage d'une étape (Sera joué sur la carte lorsqu'une étape est déverrouillée.)
    - openExercise : audio (chemin ou URL) — Ouverture d'un exercice (Sera joué lorsqu'un exercice est ouvert.)
    - closeExercise : audio (chemin ou URL) — Finalisation d'un exercice (Sera joué lorsqu'un exercice est terminé.)
    - showDialog : audio (chemin ou URL) — Affichage d'une boîte de dialogue (Sera joué lorsqu'une boîte de dialogue de confirmation est affichée.)
    - fullScore : audio (chemin ou URL) — Score parfait (Sera joué lorsque l'utilisateur atteint le score parfait.)
    - lostLife : audio (chemin ou URL) — Vie perdue (Sera joué lorsque l'utilisateur perd une vie.)
    - gainedLife : audio (chemin ou URL) — Vie gagnée (Sera joué lorsque l'utilisateur gagne une vie.)
    - gameOver : audio (chemin ou URL) — Jeu terminé (Sera joué lorsque le jeu sera terminé et que l'utilisateur ne pourra pas continuer.)
    - extraTime : audio (chemin ou URL) — Gain de temps supplémentaire (Sera joué lorsque l'utilisateur gagne du temps supplémentaire.)
    - timeoutWarning : audio (chemin ou URL) — Avertissement d'expiration du temps (Sera joué lorsque l'utilisateur manque de temps pour un exercice ou si le temps total est écoulé.)
    - endscreenNoSuccess : audio (chemin ou URL) — Écran de fin (partie incomplète) (Sera joué sur l'écran de fin si l'utilisateur n'a pas obtenu le score total.)
    - endscreenSuccess : audio (chemin ou URL) — Écran de fin (partie complète) (Sera joué sur l'écran de fin si l'utilisateur a obtenu le score total.)
- behaviour : réglages — Paramètres comportementaux
  lives=…, timeLimitGlobal=…, timeoutWarningGlobal=…, finishScore=…, enableRetry=true, enableSolutionsButton=true

Textes d'interface pré-remplis en français (ne pas fournir sauf besoin) : l10n, a11y.

## Exemple complet (validé : validateur officiel H5P + affichage)

Fichier `tests/examples/carte-jeu.md` (médias dans `tests/media/`).

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
        backgroundImage: ../media/paysage.jpg
        backgroundDescription: Une vallée avec une maison et un arbre
    # chemins explicites : sinon le harnais génère un chemin sans from/to (plantage JS)
    paths:
      - {from: 0, to: 1}
      - {from: 1, to: 2}
    # KO harnais : specialStageType / specialStageLinkURL exigés pour chaque étape, alors que
    # toute valeur transforme l'étape en « étape spéciale » (exercices ignorés).
    elements:
      - id: etape-vocabulaire
        type: stage
        label: Le vocabulaire
        telemetry: {x: "10", y: "70", width: "6", height: "9"}
        neighbors: ["1"]
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
        type: stage
        label: Le pont
        telemetry: {x: "45", y: "55", width: "6", height: "9"}
        neighbors: ["0", "2"]
        contentsList:
          - contentType:
              library: trous
              md: |
                Complète.

                La moitié d'un gâteau correspond à la fraction 1/{{2}}.
      - id: etape-chateau
        type: stage
        label: Le château
        telemetry: {x: "80", y: "30", width: "6", height: "9"}
        neighbors: ["1"]
        contentsList:
          - contentType:
              library: vf
              md: |
                La fraction 2/4 est égale à la fraction 1/2.
                - [x] Vrai
                - [ ] Faux
          - contentType:
              library: image
              file: ../media/etoile-orange.png
              alt: Une étoile, récompense de fin de parcours
endScreen:
  success:
    endScreenTextSuccess: Bravo, tu as traversé le pays des fractions !
  noSuccess:
    endScreenTextNoSuccess: Tu peux recommencer pour améliorer ton score.
```
````
