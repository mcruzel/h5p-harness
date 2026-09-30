# Information Wall — `mur-infos`

H5P.InfoWall 0.6 · alias : mur-infos, infowall, info-wall · syntaxe Markdown simplifiée : non (bloc ```yaml)

## Points d'attention

- `panelTitle` n'est **pas affiché** (il sert de titre dans l'éditeur ; le harnais le remplit avec la première entrée). Pour montrer un nom, en faire la première propriété (`properties`) et la première entrée de chaque panneau.
- `entries` : une valeur par propriété, dans l'ordre de `properties`.

## Champs (bloc ```yaml, noms H5P)

`*` = obligatoire ; les autres champs ont une valeur par défaut ou sont facultatifs. Libellés et descriptions : ceux de la bibliothèque (anglais) ; valeurs par défaut : en français.

- infoWall : groupe
  - header : texte — Header (Optional header for the information wall.)
  - propertiesGroup : groupe — Properties
    - properties* : liste (min 1) — Properties (Properties for the entries)
      chaque élément :
        - label : texte, défaut Anonyme — Label
        - showLabel : booléen, défaut false — Show property label
        - searchInProperty : booléen, défaut true — Enable searching in the property
        - styling : réglages — Styling override
          bold=false, italic=false
  - panels* : liste (min 1) — Panels (Panels for the wall)
    chaque élément :
      - panelTitle : texte — Title for panel — **non affiché (titre dans l'éditeur) ; défaut : la première entrée**
      - image : sous-contenu, library: image — Image
      - entries* : liste (min 1) — Entries (Entries for the properties)
        chaque élément = texte riche (Markdown: a code col colgroup del em figcaption figure h1 h2 h3 h4 h5 h6 hr li ol pre s strong sub sup table tbody td tfoot th thead tr u ul) — Label to be changed automatically
      - keywords : texte — Additional keywords (Add additional keywords separated by a blank space that will be used for filtering but not be visible to the user.)
  - behaviour : groupe — Behavioural settings (These options will let you control how the task behaves.)
    - useFallbackImage : booléen, défaut false — Use fallback for missing images
    - fallbackImage : sous-contenu, library: image, si useFallbackImage = True — Image
    - imageWidth : nombre, défaut 150 — Image width (Image width in px.)
    - imageHeight : nombre, défaut 150 — Image height (Image height in px.)
    - alternateBackground : booléen, défaut true — Alternate panel background (If checked, each 2nd panel will have slightly darker background than the others.)
    - offerFilterField : booléen, défaut true — Offer filter field (If checked, users will be able to filter the info wall.)
    - modeFilterField : choix and|or, défaut or, si offerFilterField = True — Mode for filter field (Choose whether the filter should narrow down or broaden the search with every new keyword.)

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
