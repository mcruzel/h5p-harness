# Agamotto — `agamotto`

H5P.Agamotto 1.7 · alias : agamotto · syntaxe Markdown simplifiée : oui

## Syntaxe Markdown

`# Titre` facultatif, puis une étape par section `## Libellé`, contenant une image `![description](image)` et une description Markdown facultative. Au moins 2 étapes (images de même taille de préférence).

## Champs (bloc ```yaml, noms H5P)

`*` = obligatoire ; les autres champs ont une valeur par défaut ou sont facultatifs.

- title : texte — Rubrique (La rubrique que vous souhaiteriez afficher au-dessus de l'image)
- items* : liste (min 2, max 50) — Éléments
  chaque élément :
    - image* : sous-contenu, library: image — Image
    - labelText : texte — Vignette (Vignette facultative pour une coche. Assurez-vous qu'elle n'est pas trop longue, sinon elle sera cachée.)
    - description : texte riche (Markdown: a code em h3 h4 li ol pre strong sub sup ul) — Description (Description facultative pour l’image)
    - audio : audio (chemin ou URL) — Audio (Audio facultatif qui joue lorsqu'une image est affichée.)
- behaviour : réglages — Paramètres comportementaux (Ces options vous permettront de contrôler le déroulement de la tâche.)
  startImage=1, snap=true, ticks=false, labels=false, transparencyReplacementColor=#000000, imagesDescriptionsRatio=70

Textes d'interface pré-remplis en français (ne pas fournir sauf besoin) : a11y.

## Exemple complet (validé : validateur officiel H5P + affichage)

Fichier `tests/examples/agamotto.md` (médias dans `tests/media/`).

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
![Un triangle équilatéral vert](../media/triangle-vert.png)

Le **triangle équilatéral** est le polygone régulier qui a le moins de côtés. Chaque angle mesure 60°.

## 4 côtés
![Un carré rouge](../media/carre-rouge.png)

Le **carré** a 4 angles droits (90°).

## 6 côtés
![Un hexagone régulier gris](../media/hexagone-gris.png)

Dans l'**hexagone régulier**, chaque angle mesure 120°. On en trouve dans les alvéoles des ruches.

## le cercle
![Un cercle bleu](../media/cercle-bleu.png)

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
