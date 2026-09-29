# Iframe Embedder — `iframe`

H5P.IFrameEmbed 1.0 · alias : iframe, iframeembed, i-frame-embed · syntaxe Markdown simplifiée : non (bloc ```yaml)

## Champs (bloc ```yaml, noms H5P)

`*` = obligatoire ; les autres champs ont une valeur par défaut ou sont facultatifs.

- width* : texte — Largeur
- minWidth* : texte — Largeur minimale
- height* : texte — Hauteur
- source* : texte — Source
- resizeSupported : booléen, défaut true — Redimensionnement supporté

## Exemple complet (validé : validateur officiel H5P + affichage)

Fichier `tests/examples/iframe.md` (médias dans `tests/media/`).

````markdown
---
type: iframe
title: Simulation PhET – introduction aux fractions
language: fr
---
```yaml
source: https://phet.colorado.edu/sims/html/fractions-intro/latest/fractions-intro_fr.html
width: 100%
minWidth: 300px
height: 600px
resizeSupported: true
```
````
