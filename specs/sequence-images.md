# Image Sequencing — `sequence-images`

H5P.ImageSequencing 1.1 · alias : sequence-images, imagesequencing, image-sequencing · syntaxe Markdown simplifiée : non (bloc ```yaml)

## Champs (bloc ```yaml, noms H5P)

`*` = obligatoire ; les autres champs ont une valeur par défaut ou sont facultatifs.

- taskDescription : texte, défaut Drag to arrange the images in… — Task Description
- altTaskDescription : texte, défaut Make the following list be or… — Alternate Task Description
- sequenceImages* : liste (min 3) — Images
  chaque élément :
    - image : image (chemin ou URL) — Image
    - imageDescription* : texte — Image Description
    - audio : audio (chemin ou URL) — Audio files
- behaviour : réglages — Behavioural settings
  enableSolution=true, enableRetry=true, enableResume=true

Textes d'interface pré-remplis en français (ne pas fournir sauf besoin) : l10n.
