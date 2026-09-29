# Interactive Video — `video-interactive`

H5P.InteractiveVideo 1.28 · alias : video-interactive, interactivevideo, interactive-video · syntaxe Markdown simplifiée : non (bloc ```yaml)

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
