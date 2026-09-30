# Audio — `audio`

H5P.Audio 1.5 · alias : audio · syntaxe Markdown simplifiée : oui

## Syntaxe Markdown

Une ou plusieurs lignes `![titre](fichier .mp3/.m4a/.ogg/.wav ou URL)`.

## Champs (bloc ```yaml, noms H5P)

`*` = obligatoire ; les autres champs ont une valeur par défaut ou sont facultatifs. Libellés et descriptions : ceux de la bibliothèque (anglais) ; valeurs par défaut : en français.

- files* : audio (chemin ou URL) — Source files
- playerMode : choix minimalistic|full|transparent, défaut minimalistic — Player mode (Select the layout of the player.)
- fitToWrapper : booléen, défaut false, si playerMode = minimalistic et playerMode = full — Fit to wrapper
- controls : booléen, défaut true, si playerMode = full — Enable controls (Controls allow the user to for instance pause the audio)
- autoplay : booléen — Enable autoplay (With autoplay the audio starts to play immediately. Do note that this is not supported by all browsers)

Textes d'interface pré-remplis en français (ne pas fournir sauf besoin) : playAudio, pauseAudio, contentName, audioNotSupported.

## Exemple complet (validé : validateur officiel H5P + affichage)

Fichier `sources/exemples/audio.md` (médias dans `sources/exemples/media/`).

````markdown
---
type: audio
title: Le signal sonore de l'expérience
language: fr
preset: decouverte
license: CC BY-SA 4.0
authors: Équipe de physique-chimie
---
![Signal sonore de 440 Hz (la du diapason)](media/bip.wav)

```yaml
playerMode: full
```
````
