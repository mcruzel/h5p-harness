# Information Wall — `mur-infos`

H5P.InfoWall 0.6 · alias : mur-infos, infowall, info-wall · syntaxe Markdown simplifiée : non (bloc ```yaml)

## Champs (bloc ```yaml, noms H5P)

`*` = obligatoire ; les autres champs ont une valeur par défaut ou sont facultatifs.

- infoWall : groupe
  - header : texte — En-tête (En-tête facultatif pour le mur d'information.)
  - propertiesGroup : groupe — Propriétés
    - properties* : liste (min 1) — Propriétés (Propriétés des entrées)
      chaque élément :
        - label : texte, défaut Anonyme — Vignette
        - showLabel : booléen, défaut false — Afficher la vignette de la propriété
        - searchInProperty : booléen, défaut true — Activer la recherche dans la propriété
        - styling : réglages — Contourner le style
          bold=false, italic=false
  - panels* : liste (min 1) — Panneaux (Panneaux pour le mur)
    chaque élément :
      - panelTitle* : texte — Titre pour le panneau
      - image : sous-contenu, library: image — Image
      - entries* : liste (min 1) — Entrées (Entées pour les propriétés)
        chaque élément = texte riche (Markdown: a code col colgroup del em figcaption figure h1 h2 h3 h4 h5 h6 hr li ol pre s strong sub sup table tbody td tfoot th thead tr u ul) — Vignette à changer automatiquement
      - keywords : texte — Mots-clés supplémentaires (Ajouter des mots-clés supplémentaires séparés par un espace qui seront utilisés pour le filtrage mais ne sero…)
  - behaviour : groupe — Paramètres comportementaux (Ces options vous permettront de contrôler le déroulement de la tâche.)
    - useFallbackImage : booléen, défaut false — Utiliser un texte de remplacement pour les images manquantes
    - fallbackImage : sous-contenu, library: image, conditionnel — Image
    - imageWidth : nombre, défaut 150 — Largeur de l’image (Largeur de l’image en px.)
    - imageHeight : nombre, défaut 150 — Hauteur de l’image (Hauteur de l’image en px.)
    - alternateBackground : booléen, défaut true — Fond du panneau alternatif (Si coché, chaque 2e panneau aura un fond légèrement plus foncé que les autres.)
    - offerFilterField : booléen, défaut true — Champ de filtre d'offre (Si cette case est cochée, les utilisateurs pourront filtrer le mur d'informations.)
    - modeFilterField : choix and|or, défaut or, conditionnel — Mode du champ de filtre (Choisir si le filtre doit restreindre ou élargir la recherche à chaque nouveau mot-clé.)

Textes d'interface pré-remplis en français (ne pas fournir sauf besoin) : l10n.

## Exemple complet (validé : validateur officiel H5P + affichage)

Fichier `tests/examples/mur-infos.md` (médias dans `tests/media/`).

````markdown
---
type: mur-infos
title: Mur d'infos – les planètes telluriques
language: fr
---
```yaml
infoWall:
  header: Les planètes telluriques du système solaire
  propertiesGroup:
    properties:
      # panelTitle n'est pas affiché par H5P : le nom de la planète est une propriété
      - label: Planète
        showLabel: false
        styling: {bold: true}
      - label: Type
        showLabel: true
      - label: Distance moyenne au Soleil
        showLabel: true
      - label: Nombre de satellites naturels
        showLabel: true
        styling: {bold: true}
  panels:
    - panelTitle: Mercure
      entries:
        - Mercure
        - Planète rocheuse
        - 58 millions de km
        - "0"
      keywords: chaude, petite
    - panelTitle: Vénus
      entries:
        - Vénus
        - Planète rocheuse
        - 108 millions de km
        - "0"
      keywords: étoile du berger, effet de serre
    - panelTitle: La Terre
      image: {library: image, file: ../media/cercle-bleu.png, alt: La planète bleue}
      entries:
        - La Terre
        - Planète rocheuse
        - 150 millions de km
        - 1 (la Lune)
      keywords: vie, eau liquide
    - panelTitle: Mars
      image: {library: image, file: ../media/carre-rouge.png, alt: La planète rouge}
      entries:
        - Mars
        - Planète rocheuse
        - 228 millions de km
        - 2 (Phobos et Déimos)
      keywords: planète rouge
  behaviour:
    imageWidth: 100
    imageHeight: 75
```
````
