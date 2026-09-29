# Image Sequencing — `sequence-images`

H5P.ImageSequencing 1.1 · alias : sequence-images, imagesequencing, image-sequencing · syntaxe Markdown simplifiée : oui

## Syntaxe Markdown

Consigne, puis les images **dans l'ordre correct**, une par ligne `- ![description](image)` (au moins 3) ; elles sont mélangées à l'affichage.

## Champs (bloc ```yaml, noms H5P)

`*` = obligatoire ; les autres champs ont une valeur par défaut ou sont facultatifs.

- taskDescription : texte, défaut Faites glisser les images pou… — Task Description
- altTaskDescription : texte, défaut Remettez la liste suivante da… — Alternate Task Description
- sequenceImages* : liste (min 3) — Images
  chaque élément :
    - image : image (chemin ou URL) — Image
    - imageDescription* : texte — Image Description
    - audio : audio (chemin ou URL) — Audio files
- behaviour : réglages — Behavioural settings
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
