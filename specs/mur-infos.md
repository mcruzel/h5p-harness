# Information Wall — `mur-infos`

H5P.InfoWall 0.6 · alias : mur-infos, infowall, info-wall · syntaxe Markdown simplifiée : non (bloc ```yaml)

## Champs (bloc ```yaml, noms H5P)

`*` = obligatoire ; les autres champs ont une valeur par défaut ou sont facultatifs.

- infoWall : groupe
  - header : texte — En-tête
  - propertiesGroup : groupe — Propriétés
    - properties* : liste (min 1) — Propriétés
      chaque élément :
        - label : texte, défaut Anonyme — Vignette
        - showLabel : booléen, défaut false — Afficher la vignette de la propriété
        - searchInProperty : booléen, défaut true — Activer la recherche dans la propriété
        - styling : réglages — Contourner le style
          bold=false, italic=false
  - panels* : liste (min 1) — Panneaux
    chaque élément :
      - panelTitle* : texte — Titre pour le panneau
      - image : sous-contenu, library: image — Image
      - entries* : liste (min 1) — Entrées
        chaque élément = texte riche (Markdown: a code col colgroup del em figcaption figure h1 h2 h3 h4 h5 h6 hr li ol pre s strong sub sup table tbody td tfoot th thead tr u ul) — Vignette à changer automatiquement
      - keywords : texte — Mots-clés supplémentaires
  - behaviour : groupe — Paramètres comportementaux
    - useFallbackImage : booléen, défaut false — Utiliser un texte de remplacement pour les images manquantes
    - fallbackImage : sous-contenu, library: image, conditionnel — Image
    - imageWidth : nombre, défaut 150 — Largeur de l’image
    - imageHeight : nombre, défaut 150 — Hauteur de l’image
    - alternateBackground : booléen, défaut true — Fond du panneau alternatif
    - offerFilterField : booléen, défaut true — Champ de filtre d'offre
    - modeFilterField : choix and|or, défaut or, conditionnel — Mode du champ de filtre

Textes d'interface pré-remplis en français (ne pas fournir sauf besoin) : l10n.
