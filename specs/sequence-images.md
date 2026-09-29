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
