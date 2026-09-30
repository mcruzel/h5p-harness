- Fichier de transcription **WebVTT obligatoire** (`transcriptFiles[n].transcriptFile` : chemin ou URL d'un `.vtt`) ; sans lui, le lecteur affiche « Aucune transcription n'a été fournie ». Exemple minimal :

  ```
  WEBVTT

  00:00.000 --> 00:02.000
  Première phrase.
  ```
- `chapters.chapterMarks` : une ligne `hh:mm:ss Titre` par chapitre (`m:ss Titre` accepté, complété par le harnais).
