# Image Pair — `paires-images`

H5P.ImagePair 1.4 · alias : paires-images, imagepair, image-pair · syntaxe Markdown simplifiée : oui

## Syntaxe Markdown

Consigne, puis une paire par ligne : `- ![a](image1) = ![b](image2)` (ou `- ![a](image)` pour deux images identiques). Au moins 2 paires.

## Champs (bloc ```yaml, noms H5P)

`*` = obligatoire ; les autres champs ont une valeur par défaut ou sont facultatifs.

- taskDescription : texte, défaut Faites glisser les images de … — Task Description
- cards* : liste (min 2, max 100) — Cards
  chaque élément :
    - image : image (chemin ou URL) — Image
    - imageAlt* : texte — Alternative text for Image
    - match : image (chemin ou URL) — Matching Image
    - matchAlt : texte — Alternative text for Matching Image
- behaviour : réglages — Behavioural settings
  allowRetry=true

Textes d'interface pré-remplis en français (ne pas fournir sauf besoin) : l10n.

## Exemple complet (validé : validateur officiel H5P + affichage)

Fichier `tests/examples/paires-images.md` (médias dans `tests/media/`).

````markdown
---
type: paires-images
title: Associer figures et formes
language: fr
preset: entrainement
license: CC BY-SA 4.0
authors: Équipe de mathématiques
---
Associe chaque figure à la figure qui possède le même nombre de côtés ou la même famille.

- ![Un carré rouge (4 côtés égaux, 4 angles droits)](../media/carre-rouge.png) = ![Un losange violet (4 côtés égaux)](../media/losange-violet.png)
- ![Un triangle vert (3 côtés)](../media/triangle-vert.png)
- ![Un hexagone gris (6 côtés)](../media/hexagone-gris.png)
- ![Un cercle bleu (aucun côté)](../media/cercle-bleu.png) = ![Un disque bleu](../media/cercle-bleu.webp)

```yaml
behaviour: {allowRetry: true}
```
````
