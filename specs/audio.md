# Audio — `audio`

H5P.Audio 1.5 · alias : audio · syntaxe Markdown simplifiée : oui

## Syntaxe Markdown

Une ou plusieurs lignes `![titre](fichier .mp3/.m4a/.ogg/.wav ou URL)`.

## Champs (bloc ```yaml, noms H5P)

`*` = obligatoire ; les autres champs ont une valeur par défaut ou sont facultatifs.

- files : audio (chemin ou URL) — Fichiers sources
- playerMode : choix minimalistic|full|transparent, défaut minimalistic — Mode d'affichage du lecteur (Selectionnez le mode d'affichage du lecteur.)
- fitToWrapper : booléen, défaut false, conditionnel — Remplir le contenant
- controls : booléen, défaut true, conditionnel — Activer les contrôles (Les contrôles permettent, par exemple, à l'utilisateur de mettre le son sur pause)
- autoplay : booléen — Activer le démarrage automatique (Avec la lecture automatique, l'audio démarre immédiatement. Noter que cela n'est pas compatible avec tous les…)

Textes d'interface pré-remplis en français (ne pas fournir sauf besoin) : playAudio, pauseAudio, contentName, audioNotSupported.

## Exemple complet (validé : validateur officiel H5P + affichage)

Fichier `tests/examples/audio.md` (médias dans `tests/media/`).

````markdown
---
type: audio
title: Le signal sonore de l'expérience
language: fr
preset: decouverte
license: CC BY-SA 4.0
authors: Équipe de physique-chimie
---
![Signal sonore de 440 Hz (la du diapason)](../media/bip.wav)

```yaml
playerMode: full
```
````
