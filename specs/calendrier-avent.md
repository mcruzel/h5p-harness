# Advent Calendar (beta) — `calendrier-avent`

H5P.AdventCalendar 0.4 · alias : calendrier-avent, adventcalendar, advent-calendar · syntaxe Markdown simplifiée : non (bloc ```yaml)

## Champs (bloc ```yaml, noms H5P)

`*` = obligatoire ; les autres champs ont une valeur par défaut ou sont facultatifs. Libellés et descriptions : ceux de la bibliothèque (anglais) ; valeurs par défaut : en français.

- modeDoorImage : choix manual|automatic, défaut automatic — Mode for door images (Select whether you want to set each custom door image yourself or let H5P do the work for you based on the calendar background image set in the behavioural settings.)
- doors* : liste (min 24, max 24) — Doors
  chaque élément :
    - type* : choix audio|image|link|text|video — Content type (Content type that shoud optionally pop up when the door is opened.)
    - audio : audio (chemin ou URL), si type = audio — Audio
    - image : sous-contenu, library: image, si type = image — Image
    - link : sous-contenu, library: lien, si type = link — Link
    - text : sous-contenu, library: texte, si type = text — Text
    - video : vidéo (URL YouTube/Vimeo, chemin ou URL), si type = video — Video
    - autoplay : booléen, défaut false, si type = audio et type = video — Autoplay
    - doorCover : image (chemin ou URL), si modeDoorImage = manual — Door image (Image that will be used for the door. Needs to have a size ratio of 1:1 if you want the left half fit the right half.)
    - previewImage : image (chemin ou URL) — Background image (Image that should appear inside the door. Will be the door's number by default.)
- visuals : groupe — Visual settings (These options will let you configure the visual appearance.)
  - backgroundImage : image (chemin ou URL) — Calendar background image
  - doorImageTemplate : image (chemin ou URL), si modeDoorImage = manual — Door image template (If an image is set, it will be used for every door unless a specific door image is set for a single door.)
  - hideDoorBorder : booléen, défaut false — Hide door border
  - hideNumbers : booléen, défaut false — Hide door numbers
  - hideDoorKnobs : booléen, défaut false — Hide door knobs
  - hideDoorFrame : booléen, défaut false — Hide door frame
  - snow : booléen, défaut false — Let it snow (Will add some snow falling in front of the calendar. It never rains in Southern California, it never snows on IE11.)
- audio : groupe — Audio settings (These options will let you configure the audio appearance.)
  - backgroundMusic : audio (chemin ou URL) — Background music
  - autoplay : booléen, défaut false — Autoplay background music (If set, the background music will play automatically once the content is opened. Please note: Some browsers' media policy may prevent autoplay.)
- behaviour : réglages — Behavioural settings (These options will let you override behaviour settings.)
  modeDoorPlacement=dynamic (fixed|dynamic), doorPlacementRatio=6x4 (6x4|4x6), randomize=false, keepImageOrder=false, designMode=true

Textes d'interface pré-remplis en français (ne pas fournir sauf besoin) : l10n, a11y.

## Exemple complet (validé : validateur officiel H5P + affichage)

Fichier `sources/exemples/calendrier-avent.md` (médias dans `sources/exemples/media/`).

````markdown
---
type: calendrier-avent
title: Calendrier de l'Avent des sciences
language: fr
---
```yaml
modeDoorImage: automatic
visuals:
  backgroundImage: media/paysage.jpg
  snow: true
doors:
  - {type: text, text: {library: texte, text: "**Jour 1** – L'eau bout à 100 °C au niveau de la mer."}}
  - {type: image, image: {library: image, file: media/etoile-orange.png, alt: Une étoile orange}}
  - {type: text, text: {library: texte, text: "**Jour 3** – La Terre fait le tour du Soleil en environ 365,25 jours."}}
  - {type: audio, audio: media/bip.wav}
  - {type: text, text: {library: texte, text: "**Jour 5** – Un triangle a toujours trois angles dont la somme vaut 180°."}}
  - {type: text, text: {library: texte, text: "**Jour 6** – La lumière du Soleil met environ 8 minutes à nous parvenir."}}
  - {type: link, link: {library: lien, title: Le système solaire, linkWidget: {protocol: "https://", url: fr.wikipedia.org/wiki/Système_solaire}}}
  - {type: text, text: {library: texte, text: "**Jour 8** – Le cœur humain bat environ 100 000 fois par jour."}}
  - {type: image, image: {library: image, file: media/hexagone-gris.png, alt: "Un hexagone, forme des alvéoles d'abeilles"}}
  - {type: text, text: {library: texte, text: "**Jour 10** – Les abeilles construisent des alvéoles hexagonales."}}
  - {type: text, text: {library: texte, text: "**Jour 11** – Le dioxygène représente environ 21 % de l'air."}}
  - {type: text, text: {library: texte, text: "**Jour 12** – 12 est divisible par 1, 2, 3, 4, 6 et 12."}}
  - {type: video, video: media/clip.webm}
  - {type: text, text: {library: texte, text: "**Jour 14** – La glace flotte car elle est moins dense que l'eau liquide."}}
  - {type: text, text: {library: texte, text: "**Jour 15** – Le son ne se propage pas dans le vide."}}
  - {type: text, text: {library: texte, text: "**Jour 16** – Un losange a quatre côtés de même longueur."}}
  - {type: image, image: {library: image, file: media/losange-violet.png, alt: Un losange violet}}
  - {type: text, text: {library: texte, text: "**Jour 18** – La Lune n'émet pas de lumière : elle réfléchit celle du Soleil."}}
  - {type: text, text: {library: texte, text: "**Jour 19** – Le nombre π vaut environ 3,14."}}
  - {type: text, text: {library: texte, text: "**Jour 20** – Les plantes vertes produisent du dioxygène par photosynthèse."}}
  - {type: text, text: {library: texte, text: "**Jour 21** – Le 21 décembre est le jour le plus court de l'année dans l'hémisphère Nord."}}
  - {type: text, text: {library: texte, text: "**Jour 22** – Un cube possède 6 faces, 12 arêtes et 8 sommets."}}
  - {type: text, text: {library: texte, text: "**Jour 23** – La vitesse de la lumière est d'environ 300 000 km/s."}}
  - {type: image, image: {library: image, file: media/cercle-bleu.png, alt: Un cercle bleu comme la planète Terre}}
behaviour:
  randomize: false
```
````
