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
