# Iframe Embedder — `iframe`

H5P.IFrameEmbed 1.0 · alias : iframe, iframeembed, i-frame-embed · syntaxe Markdown simplifiée : non (bloc ```yaml)

## Points d'attention

- `width` et `height` en **px** (ex. `800px`, `600px`) : H5P en déduit le rapport hauteur/largeur ; un % déforme le cadre (le harnais le refuse).
- La page intégrée doit accepter l'intégration (beaucoup de sites l'interdisent par X-Frame-Options/CSP) et être en `https://` (Moodle est en HTTPS).

## Champs (bloc ```yaml, noms H5P)

`*` = obligatoire ; les autres champs ont une valeur par défaut ou sont facultatifs. Libellés et descriptions : ceux de la bibliothèque (anglais) ; valeurs par défaut : en français.

- width* : texte — Width (Width of iFrame in CSS compliant format. Default: "500px") — **en px (ex. 800px) : H5P en déduit le rapport hauteur/largeur**
- minWidth* : texte — Minimum width (Minimum width of iFrame in CSS compliant format. Default: "300px")
- height* : texte — Height (Height of iFrame in CSS compliant format. Default: "500px") — **en px (ex. 600px)**
- source* : texte — Source (URI to external document, or path to document found inside H5P (under /content))
- resizeSupported : booléen, défaut true — Resize supported (If enabled, fullscreen button will be displayed, and H5P will be resized to fit its surroundings)

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
