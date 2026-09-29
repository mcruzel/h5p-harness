# Advent Calendar (beta) — `calendrier-avent`

H5P.AdventCalendar 0.4 · alias : calendrier-avent, adventcalendar, advent-calendar · syntaxe Markdown simplifiée : non (bloc ```yaml)

## Champs (bloc ```yaml, noms H5P)

`*` = obligatoire ; les autres champs ont une valeur par défaut ou sont facultatifs.

- modeDoorImage : choix manual|automatic, défaut automatic — Mode for door images
- doors* : liste (min 24, max 24) — Doors
  chaque élément :
    - type* : choix audio|image|link|text|video — Content type
    - audio : audio (chemin ou URL), conditionnel — Audio
    - image : sous-contenu, library: image, conditionnel — Image
    - link : sous-contenu, library: lien, conditionnel — Link
    - text : sous-contenu, library: texte, conditionnel — Text
    - video : vidéo (URL YouTube/Vimeo, chemin ou URL), conditionnel — Video
    - autoplay : booléen, défaut false, conditionnel — Autoplay
    - doorCover : image (chemin ou URL), conditionnel — Door image
    - previewImage : image (chemin ou URL) — Background image
- visuals : groupe — Visual settings
  - backgroundImage : image (chemin ou URL) — Calendar background image
  - doorImageTemplate : image (chemin ou URL), conditionnel — Door image template
  - hideDoorBorder : booléen, défaut false — Hide door border
  - hideNumbers : booléen, défaut false — Hide door numbers
  - hideDoorKnobs : booléen, défaut false — Hide door knobs
  - hideDoorFrame : booléen, défaut false — Hide door frame
  - snow : booléen, défaut false — Let it snow
- audio : groupe — Audio settings
  - backgroundMusic : audio (chemin ou URL) — Background music
  - autoplay : booléen, défaut false — Autoplay background music
- behaviour : réglages — Behavioural settings
  modeDoorPlacement=dynamic (fixed|dynamic), doorPlacementRatio=6x4 (6x4|4x6), randomize=false, keepImageOrder=false, designMode=true

Textes d'interface pré-remplis en français (ne pas fournir sauf besoin) : l10n, a11y.

## Exemple complet (validé : validateur officiel H5P + affichage)

Fichier `tests/examples/calendrier-avent.md` (médias dans `tests/media/`).

````markdown
---
type: calendrier-avent
title: Calendrier de l'Avent des sciences
language: fr
---
```yaml
modeDoorImage: automatic
visuals:
  backgroundImage: ../media/paysage.jpg
  snow: true
doors:
  - {type: text, text: {library: texte, text: "**Jour 1** – L'eau bout à 100 °C au niveau de la mer."}}
  - {type: image, image: {library: image, file: ../media/etoile-orange.png, alt: Une étoile orange}}
  - {type: text, text: {library: texte, text: "**Jour 3** – La Terre fait le tour du Soleil en environ 365,25 jours."}}
  - {type: audio, audio: ../media/bip.wav}
  - {type: text, text: {library: texte, text: "**Jour 5** – Un triangle a toujours trois angles dont la somme vaut 180°."}}
  - {type: text, text: {library: texte, text: "**Jour 6** – La lumière du Soleil met environ 8 minutes à nous parvenir."}}
  - {type: link, link: {library: lien, title: Le système solaire, linkWidget: {protocol: "https://", url: fr.wikipedia.org/wiki/Système_solaire}}}
  - {type: text, text: {library: texte, text: "**Jour 8** – Le cœur humain bat environ 100 000 fois par jour."}}
  - {type: image, image: {library: image, file: ../media/hexagone-gris.png, alt: "Un hexagone, forme des alvéoles d'abeilles"}}
  - {type: text, text: {library: texte, text: "**Jour 10** – Les abeilles construisent des alvéoles hexagonales."}}
  - {type: text, text: {library: texte, text: "**Jour 11** – Le dioxygène représente environ 21 % de l'air."}}
  - {type: text, text: {library: texte, text: "**Jour 12** – 12 est divisible par 1, 2, 3, 4, 6 et 12."}}
  - {type: video, video: ../media/clip.webm}
  - {type: text, text: {library: texte, text: "**Jour 14** – La glace flotte car elle est moins dense que l'eau liquide."}}
  - {type: text, text: {library: texte, text: "**Jour 15** – Le son ne se propage pas dans le vide."}}
  - {type: text, text: {library: texte, text: "**Jour 16** – Un losange a quatre côtés de même longueur."}}
  - {type: image, image: {library: image, file: ../media/losange-violet.png, alt: Un losange violet}}
  - {type: text, text: {library: texte, text: "**Jour 18** – La Lune n'émet pas de lumière : elle réfléchit celle du Soleil."}}
  - {type: text, text: {library: texte, text: "**Jour 19** – Le nombre π vaut environ 3,14."}}
  - {type: text, text: {library: texte, text: "**Jour 20** – Les plantes vertes produisent du dioxygène par photosynthèse."}}
  - {type: text, text: {library: texte, text: "**Jour 21** – Le 21 décembre est le jour le plus court de l'année dans l'hémisphère Nord."}}
  - {type: text, text: {library: texte, text: "**Jour 22** – Un cube possède 6 faces, 12 arêtes et 8 sommets."}}
  - {type: text, text: {library: texte, text: "**Jour 23** – La vitesse de la lumière est d'environ 300 000 km/s."}}
  - {type: image, image: {library: image, file: ../media/cercle-bleu.png, alt: Un cercle bleu comme la planète Terre}}
behaviour:
  randomize: false
```
````
