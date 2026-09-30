# Agamotto — `agamotto`

H5P.Agamotto 1.7 · alias : agamotto · syntaxe Markdown simplifiée : oui

## Syntaxe Markdown

`# Titre` facultatif, puis une étape par section `## Libellé`, contenant une image `![description](image)` et une description Markdown facultative. Au moins 2 étapes (images de même taille de préférence).

## Champs (bloc ```yaml, noms H5P)

`*` = obligatoire ; les autres champs ont une valeur par défaut ou sont facultatifs. Libellés et descriptions : ceux de la bibliothèque (anglais) ; valeurs par défaut : en français.

- title : texte — Heading (The heading you'd like to show above the image)
- items* : liste (min 2, max 50) — Items
  chaque élément :
    - image* : sous-contenu, library: image — Image
    - labelText : texte — Label (Optional label for a tick. Please make sure it's not too long, or it will be hidden.)
    - description : texte riche (Markdown: a code em h3 h4 li ol pre strong sub sup ul) — Description (Optional description for the image)
    - audio : audio (chemin ou URL) — Audio (Optional audio that plays when an image is shown.)
- behaviour : réglages — Behavioural settings (These options will let you control how the task behaves.)
  startImage=1, snap=true, ticks=false, labels=false, transparencyReplacementColor=#000000, imagesDescriptionsRatio=70

Textes d'interface pré-remplis en français (ne pas fournir sauf besoin) : a11y.

## Exemple complet (validé : validateur officiel H5P + affichage)

Fichier `sources/exemples/agamotto.md` (médias dans `sources/exemples/media/`).

````markdown
---
type: agamotto
title: Des polygones au cercle
language: fr
preset: decouverte
license: CC BY-SA 4.0
authors: Équipe de mathématiques
---
# Quand le nombre de côtés augmente…

## 3 côtés
![Un triangle équilatéral vert](media/triangle-vert.png)

Le **triangle équilatéral** est le polygone régulier qui a le moins de côtés. Chaque angle mesure 60°.

## 4 côtés
![Un carré rouge](media/carre-rouge.png)

Le **carré** a 4 angles droits (90°).

## 6 côtés
![Un hexagone régulier gris](media/hexagone-gris.png)

Dans l'**hexagone régulier**, chaque angle mesure 120°. On en trouve dans les alvéoles des ruches.

## le cercle
![Un cercle bleu](media/cercle-bleu.png)

Avec de plus en plus de côtés, le polygone régulier ressemble à un **cercle** :

- son périmètre se rapproche de 2 × π × r ;
- son aire se rapproche de π × r².

```yaml
behaviour:
  ticks: true
  labels: true
  transparencyReplacementColor: "#ffffff"
```
````
