# Transcript — `transcription`

H5P.Transcript 1.3 · alias : transcription, transcript · syntaxe Markdown simplifiée : non (bloc ```yaml)

## Points d'attention

- Fichier de transcription **WebVTT obligatoire** (`transcriptFiles[n].transcriptFile` : chemin ou URL d'un `.vtt`) ; sans lui, le lecteur affiche « Aucune transcription n'a été fournie ». Exemple minimal :

  ```
  WEBVTT

  00:00.000 --> 00:02.000
  Première phrase.
  ```
- `chapters.chapterMarks` : une ligne `hh:mm:ss Titre` par chapitre (`m:ss Titre` accepté, complété par le harnais).

## Champs (bloc ```yaml, noms H5P)

`*` = obligatoire ; les autres champs ont une valeur par défaut ou sont facultatifs. Libellés et descriptions : ceux de la bibliothèque (anglais) ; valeurs par défaut : en français.

- mediumGroup : groupe — Medium
  - medium* : sous-contenu, library: audio | video-interactive | video — Medium
- transcriptFiles* : liste (min 1) — Transcript files
  chaque élément :
    - transcriptFile* : fichier (chemin ou URL) — Transcript (WebVTT file)
    - label* : texte — Label (Label to identify the transcript with. Not relevant if you only have one transcript file.)
    - languageCode : texte — Language code (The transcript library will try to automatically determine the language of the transcription text as information for screen readers. If that fails, you can manually set the "BCP 47 language tag" - e.g. "en" for English,…)
- behaviour : réglages — Behavioural settings
  maxLines=10, showOnLoad=true
- chapters : groupe — Chapters
  - useIVBookmarks : booléen, défaut false, si medium = H5P.InteractiveVideo — Use bookmarks of Interactive Video
  - chapterMarks : texte multiligne — Chapter marks (You can optionally add chapter marks in common mp4chaps format. The syntax is "hh:mm:ss Chapter title" or "hh:mm:ss.MMM Chapter title")

Textes d'interface pré-remplis en français (ne pas fournir sauf besoin) : l10n, a11y.

## Exemple complet (validé : validateur officiel H5P + affichage)

Fichier `sources/exemples/transcription.md` (médias dans `sources/exemples/media/`).

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
    md: "![Compte à rebours](media/clip.webm)"
transcriptFiles:
  - transcriptFile: media/transcription.vtt
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
