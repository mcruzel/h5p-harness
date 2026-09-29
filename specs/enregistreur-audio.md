# Audio Recorder — `enregistreur-audio`

H5P.AudioRecorder 1.0 · alias : enregistreur-audio, audiorecorder, audio-recorder · syntaxe Markdown simplifiée : non (bloc ```yaml)

## Champs (bloc ```yaml, noms H5P)

`*` = obligatoire ; les autres champs ont une valeur par défaut ou sont facultatifs.

- title : texte multiligne — Consigne

Textes d'interface pré-remplis en français (ne pas fournir sauf besoin) : l10n.

## Exemple complet (validé : validateur officiel H5P + affichage)

Fichier `tests/examples/enregistreur-audio.md` (médias dans `tests/media/`).

````markdown
---
type: enregistreur-audio
title: Lire une fable à voix haute
language: fr
preset: entrainement
license: CC BY-SA 4.0
authors: Équipe de lettres
---
```yaml
title: |
  Enregistre-toi en train de lire les quatre premiers vers de « La Cigale et la Fourmi » de La Fontaine.
  Soigne l'articulation et respecte la ponctuation, puis télécharge ton enregistrement et dépose-le dans le devoir Moodle.
```
````
