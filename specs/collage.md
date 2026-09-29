# Collage — `collage`

H5P.Collage 0.3 · alias : collage · syntaxe Markdown simplifiée : non (bloc ```yaml)

## Champs (bloc ```yaml, noms H5P)

`*` = obligatoire ; les autres champs ont une valeur par défaut ou sont facultatifs.

- collage : groupe — Aperçu
  - template : choix 1|1-1|2|2-1|1-2|2-2|3-1|1-3|2-3|3-2|…, défaut 2-1 — Modèle
  - options : réglages — Options d'affichage
    heightRatio=0.75, spacing=0.5, frame=true
  - clips* : liste (min 1) — Découpes
    chaque élément :
      - image : image (chemin ou URL) — Image
      - offset : réglages — Décalage (offset)
        top=0, left=0
      - alt* : texte — Alternative text
      - title : texte — Hover text
      - scale : nombre, min 0.01, défaut 1 — Echelle

## Exemple complet (validé : validateur officiel H5P + affichage)

Fichier `tests/examples/collage.md` (médias dans `tests/media/`).

````markdown
---
type: collage
title: Un quartier qui change
language: fr
preset: decouverte
license: CC BY-SA 4.0
authors: Équipe d'histoire-géographie
---
```yaml
collage:
  template: 1-2
  options: {heightRatio: 0.6, spacing: 0.5, frame: true}
  clips:
    - image: ../media/paysage.jpg
      alt: Le paysage rural d'origine, avec une maison et un arbre
      title: Le site en 1950
    - image: ../media/avant.jpg
      alt: Le quartier avant sa rénovation
      title: Le quartier en 1990
    - image: ../media/apres.jpg
      alt: Le quartier après sa rénovation
      title: Le quartier en 2020
      scale: 1.2
      offset: {top: -10, left: -5}
```
````
