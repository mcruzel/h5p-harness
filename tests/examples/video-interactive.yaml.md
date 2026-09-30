---
type: video-interactive
title: Les états de l'eau – vidéo interactive
language: fr
preset: entrainement
---
```yaml
interactiveVideo:
  video:
    files: ../media/clip.webm
    startScreenOptions:
      title: Les états de l'eau
      shortStartDescription: Regarde la vidéo et réponds aux questions.
  assets:
    bookmarks:
      - time: 0
        label: Introduction
      - time: 1
        label: Question
    # temps en secondes (ou m:ss) ; x, y en % de la vidéo ; width, height en em (facultatifs)
    interactions:
      - duration: {from: 0, to: 1}
        x: 3
        y: 5
        width: 12
        height: 6
        pause: false
        displayType: poster
        label: Rappel
        action:
          library: texte-simple
          text: "L'eau existe sous trois états : **solide**, **liquide** et **gazeux**."
      - duration: {from: 1, to: 2}
        x: 3
        y: 5
        width: 20
        height: 17
        pause: true
        displayType: poster
        action:
          library: qcm
          md: |
            À quelle température l'eau pure bout-elle (au niveau de la mer) ?
            - [x] 100 °C
            - [ ] 0 °C
              > Non : 0 °C est la température de fusion de la glace.
            - [ ] 50 °C
        adaptivity:
          correct: {seekTo: 2, message: "**Bravo !** Tu peux continuer.", seekLabel: Continuer}
          wrong: {seekTo: 0, message: Revois le début de la vidéo., seekLabel: Revoir la vidéo}
      - duration: {from: 1, to: 2}
        x: 80
        y: 10
        pause: false
        displayType: button
        label: Vrai ou faux ?
        action:
          library: vf
          md: |
            La glace est de l'eau à l'état solide.
            - [x] Vrai
            - [ ] Faux
  summary:
    displayAt: 1
    task:
      library: resume
      md: |
        Choisis l'affirmation correcte.

        - [x] La vapeur d'eau est de l'eau à l'état gazeux.
        - [ ] La vapeur d'eau est de l'eau à l'état liquide.
```
