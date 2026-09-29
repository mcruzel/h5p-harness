# Interactive Video — `video-interactive`

H5P.InteractiveVideo 1.28 · alias : video-interactive, interactivevideo, interactive-video · syntaxe Markdown simplifiée : oui

## Syntaxe Markdown

Une ligne `![titre](vidéo)` (fichier MP4/WebM, URL, ou lien YouTube/Vimeo), une courte description facultative, puis une section par moment de la vidéo : `## <temps> <type>` avec le temps en `m:ss` (ou secondes). Types : questions (`qcm`, `vf: faux`, `trous`, `glisser-mots`, `marquer-mots`, `choix-unique`, `resume`…) affichées en carte et mettant la vidéo en pause ; `texte` (bouton d'information, sans pause) ; `signet: Titre` (chapitre) ; `fin: Titre` (écran de fin). Positions et durées fines : bloc ```yaml (`interactiveVideo.assets.interactions[n]`).

```markdown
![La photosynthèse](videos/photosynthese.mp4)
Regarde la vidéo et réponds aux questions.

## 0:00 signet: Introduction

## 0:45 texte
Observe la couleur des feuilles.

## 1:30 qcm
Quel gaz est rejeté ?
- [x] Le dioxygène
- [ ] Le dioxyde de carbone
```

## Champs (bloc ```yaml, noms H5P)

`*` = obligatoire ; les autres champs ont une valeur par défaut ou sont facultatifs.

- interactiveVideo : groupe — Éditeur de vidéo interactive
  - video : groupe — Téléverser / intégrer une vidéo
    - files : vidéo (URL YouTube/Vimeo, chemin ou URL) — Ajouter une vidéo
    - startScreenOptions : groupe — Options de l'écran de démarrage (cette option n'est pas disponible po…
      - title : texte, défaut Vidéo interactive — Titre de la vidéo interactive
      - hideStartTitle : booléen, défaut false — Cacher le titre sur l'écran de lancement de la vidéo
      - shortStartDescription : texte — Courte description
      - poster : image (chemin ou URL) — Image à la une
    - textTracks : groupe — Pistes de textes (ne fonctionne pas avec les vidéos YouTube)
      - videoTrack : liste (min 0) — Pistes de textes disponibles
        chaque élément :
          - label : texte, défaut Sous-titres — Intitulé de la piste
          - kind : choix subtitles|captions|descriptions, défaut subtitles — Type de texte
          - srcLang : texte, défaut en — Langue source, obligatoire pour les sous-titres
          - track : fichier (chemin ou URL) — Source de texte (fichier WebVTT)
      - defaultTrackLabel : texte — Texte par défaut de la première piste
  - assets : groupe — Ajouter des activités
    - interactions : liste
      chaque élément :
        - duration : groupe — Plage d'apparition
          - from* : nombre
          - to* : nombre
        - pause : booléen — Mettre la vidéo sur pause
        - displayType : choix button|poster, défaut button — Afficher sous forme de
        - buttonOnMobile : booléen, défaut false — Devient Bouton sur de petits écrans
        - label : texte riche (Markdown) — Étiquette
        - action* : sous-contenu, library: nil | texte-simple | tableau | lien | image | resume | choix-unique | qcm | vf | trous | glisser-deposer | marquer-mots | glisser-mots | aller-a-question | zone-video | questionnaire | question-libre | choix-images
        - adaptivity : groupe — Adaptativité
          - correct : groupe — Action sur une bonne réponse
            - seekTo* : nombre — Aller vers
            - allowOptOut : booléen — Autoriser l'utilisateur à se retirer et continuer
            - message* : texte riche (Markdown: a code del em s strong) — Message
            - seekLabel* : texte — Étiquette pour le bouton "Aller vers"
          - wrong : groupe — Action sur mauvaise réponse
            - seekTo* : nombre — Aller vers
            - allowOptOut : booléen — Autoriser l'utilisateur à se retirer et continuer
            - message* : texte riche (Markdown: a code del em s strong) — Message
            - seekLabel* : texte — Étiquette pour le bouton "Aller vers"
          - requireCompletion : booléen — Exiger la complétude de la tâche avant d'avancer
        - visuals : réglages — Images
          backgroundColor=rgb(255, 255, 255), boxShadow=true
        - goto : groupe — Au clic, aller vers
          - type : choix timecode|url — Type de média
          - time : nombre — Aller à
          - url : groupe — URL
            - protocol : choix http://|https://|/|other, défaut http:// — Protocole
            - url : texte — URL
          - visualize : booléen — Aperçu
    - bookmarks : liste
      chaque élément :
        - time* : nombre
        - label* : texte
    - endscreens : liste
      chaque élément :
        - time* : nombre
        - label* : texte
  - summary : groupe — Récapitulatif
    - task : sous-contenu, library: resume, défaut {'library': 'H5P.Summary 1.10…
    - displayAt : nombre, défaut 3 — Afficher à
- override : groupe — Options générales
  - startVideoAt : nombre — Démarrer la vidéo à
  - autoplay : booléen, défaut false — Démarrage automatique
  - loop : booléen, défaut false — Vidéo en boucle
  - hasNoAutoPause : booléen, défaut false — Deactivate auto-pause
  - showSolutionButton : choix on|off — Cacher le bouton "Voir la solution"
  - retryButton* : choix on|off — Cacher le bouton "Recommencer"
  - showBookmarksmenuOnLoad : booléen, défaut false — Démarrer avec le menu des Signets ouvert
  - showRewind10 : booléen, défaut false — Afficher le bouton pour revenir en arrière de 10 secondes
  - preventSkippingMode : choix none|forward|both, défaut none — Désactiver la navigation
  - deactivateSound : booléen, défaut false — Désactiver le son

Textes d'interface pré-remplis en français (ne pas fournir sauf besoin) : l10n.

## Exemple complet (validé : validateur officiel H5P + affichage)

Fichier `tests/examples/video-interactive.md` (médias dans `tests/media/`).

````markdown
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
        # contournement : adaptivity exigée par le harnais même pour un simple texte
        adaptivity:
          correct: {seekTo: 1, message: Bien, seekLabel: Continuer}
          wrong: {seekTo: 0, message: Revois le début, seekLabel: Revoir}
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
          requireCompletion: false
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
        adaptivity:
          correct: {seekTo: 2, message: Exact !, seekLabel: Continuer}
          wrong: {seekTo: 0, message: Revois le début de la vidéo., seekLabel: Revoir la vidéo}
  summary:
    displayAt: 1
    task:
      library: resume
      md: |
        Choisis l'affirmation correcte.

        - [x] La vapeur d'eau est de l'eau à l'état gazeux.
        - [ ] La vapeur d'eau est de l'eau à l'état liquide.
override:
  retryButton: "on"
```
````
