# Audio — `audio`

H5P.Audio 1.5 · alias : audio · syntaxe Markdown simplifiée : oui

## Syntaxe Markdown

Une ou plusieurs lignes `![titre](fichier .mp3/.m4a/.ogg/.wav ou URL)`.

## Champs (bloc ```yaml, noms H5P)

`*` = obligatoire ; les autres champs ont une valeur par défaut ou sont facultatifs.

- files : audio (chemin ou URL) — Fichiers sources
- playerMode : choix minimalistic|full|transparent, défaut minimalistic — Mode d'affichage du lecteur
- fitToWrapper : booléen, défaut false, conditionnel — Remplir le contenant
- controls : booléen, défaut true, conditionnel — Activer les contrôles
- autoplay : booléen — Activer le démarrage automatique

Textes d'interface pré-remplis en français (ne pas fournir sauf besoin) : playAudio, pauseAudio, contentName, audioNotSupported.
