# Image Sequencing — `sequence-images`

H5P.ImageSequencing 1.1 · alias : sequence-images, imagesequencing, image-sequencing · syntaxe Markdown simplifiée : oui

## Syntaxe Markdown

Consigne, puis les images **dans l'ordre correct**, une par ligne `- ![description](image)` (au moins 3) ; elles sont mélangées à l'affichage.

## Champs (bloc ```yaml, noms H5P)

`*` = obligatoire ; les autres champs ont une valeur par défaut ou sont facultatifs. Libellés et descriptions : ceux de la bibliothèque (anglais) ; valeurs par défaut : en français.

- taskDescription : texte, défaut Faites glisser les images pou… — Task Description (A guide telling the user how to solve this task.)
- altTaskDescription : texte, défaut Remettez la liste suivante da… — Alternate Task Description (A guide intended for visually impaired users on how to solve this task.)
- sequenceImages* : liste (min 3) — Images
  chaque élément :
    - image : image (chemin ou URL) — Image
    - imageDescription* : texte — Image Description (An image description for users who cannot recognize the image)
    - audio : audio (chemin ou URL) — Audio files (An optional audio for the card to play)
- behaviour : réglages — Behavioural settings (These options will let you control how the game behaves.)
  enableSolution=true, enableRetry=true, enableResume=true

Textes d'interface pré-remplis en français (ne pas fournir sauf besoin) : l10n.

## Exemple complet (validé : validateur officiel H5P + affichage)

Fichier `tests/examples/sequence-images.md` (médias dans `tests/media/`).

````markdown
---
type: sequence-images
title: Ranger les figures selon leur nombre de côtés
language: fr
preset: entrainement
license: CC BY-SA 4.0
authors: Équipe de mathématiques
---
Range les figures de celle qui a le moins de côtés à celle qui en a le plus.

- ![Cercle (aucun côté)](../media/cercle-bleu.png)
- ![Triangle (3 côtés)](../media/triangle-vert.png)
- ![Carré (4 côtés)](../media/carre-rouge.png)
- ![Hexagone (6 côtés)](../media/hexagone-gris.png)
- ![Étoile (10 côtés)](../media/etoile-orange.png)

```yaml
altTaskDescription: Range la liste suivante de la figure qui a le moins de côtés à celle qui en a le plus.
behaviour: {enableSolution: true, enableRetry: true}
```
````
