# Iframe Embedder — `iframe`

H5P.IFrameEmbed 1.0 · alias : iframe, iframeembed, i-frame-embed · syntaxe Markdown simplifiée : non (bloc ```yaml)

## Champs (bloc ```yaml, noms H5P)

`*` = obligatoire ; les autres champs ont une valeur par défaut ou sont facultatifs.

- width* : texte — Largeur (Largeur du cadre au format CSS standard. Défaut: "500px")
- minWidth* : texte — Largeur minimale (Largeur minimale du cadre au format CSS standard. Défaut: "300px")
- height* : texte — Hauteur (Hauteur du cadre au format CSS standard. Défaut: "500px")
- source* : texte — Source (URL du document externe, ou chemin vers un document H5P (dans /content))
- resizeSupported : booléen, défaut true — Redimensionnement supporté (Si cette option est activée, un bouton "Plein écran" apparaîtra, et le contenu H5P sera redimensionné afin d'…)

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
# largeur/hauteur en px : H5P en tire le rapport hauteur/largeur (un % fausse le calcul)
width: 800px
minWidth: 300px
height: 600px
resizeSupported: true
```
````
