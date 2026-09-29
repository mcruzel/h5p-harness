# Transcript — `transcription`

H5P.Transcript 1.3 · alias : transcription, transcript · syntaxe Markdown simplifiée : non (bloc ```yaml)

## Champs (bloc ```yaml, noms H5P)

`*` = obligatoire ; les autres champs ont une valeur par défaut ou sont facultatifs.

- mediumGroup : groupe — Medium
  - medium* : sous-contenu, library: audio | video-interactive | video — Medium
- transcriptFiles* : liste (min 1) — Transcript files
  chaque élément :
    - transcriptFile : fichier (chemin ou URL) — Transcript (WebVTT file)
    - label* : texte — Label
    - languageCode : texte — Language code
- behaviour : réglages — Behavioural settings
  maxLines=10, showOnLoad=true
- chapters : groupe — Chapters
  - useIVBookmarks : booléen, défaut false, conditionnel — Use bookmarks of Interactive Video
  - chapterMarks : texte multiligne — Chapter marks

Textes d'interface pré-remplis en français (ne pas fournir sauf besoin) : l10n, a11y.

## Exemple complet (validé : validateur officiel H5P + affichage)

Fichier `tests/examples/transcription.md` (médias dans `tests/media/`).

````markdown
---
type: transcription
title: Transcription – le compte à rebours
language: fr
---
```yaml
mediumGroup:
  medium:
    library: video
    md: "![Compte à rebours](../media/clip.webm)"
transcriptFiles:
  # pas de .vtt dans tests/media : transcription écrite à côté de l'exemple
  - transcriptFile: transcription.vtt
    label: Français
    languageCode: fr
behaviour:
  maxLines: 6
chapters:
  chapterMarks: |
    00:00:00 Début du compte
    00:00:01 Fin du compte
```
````
