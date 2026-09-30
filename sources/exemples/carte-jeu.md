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
