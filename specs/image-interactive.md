# Image Hotspots — `image-interactive`

H5P.ImageHotspots 1.11 · alias : image-interactive, imagehotspots, image-hotspots · syntaxe Markdown simplifiée : oui

## Syntaxe Markdown

Une ligne `![description](image de fond)`, puis un point par section `## x,y Titre` (position du point en % de l'image, depuis le coin haut-gauche), suivie de son contenu : texte Markdown, et/ou lignes `![…](image ou vidéo)`.

```markdown
![Schéma d'une cellule](images/cellule.png)

## 45,50 Le noyau
Il contient l'ADN.

## 70,30 Une mitochondrie
Elle produit l'énergie de la cellule.
```

## Champs (bloc ```yaml, noms H5P)

`*` = obligatoire ; les autres champs ont une valeur par défaut ou sont facultatifs. Libellés et descriptions : ceux de la bibliothèque (anglais) ; valeurs par défaut : en français.

- image* : image (chemin ou URL) — Background image (Image shown on background.)
- backgroundImageAltText : texte — Alternative text for background image (If the browser can't load the image this text will be displayed instead. Also used by assistive technologies.)
- globalIconType : choix icon|image|numbers, défaut icon — Global hotspot Icon
- globalIcon : choix plus|minus|times|check|question|info|exclamation, défaut plus, si globalIconType = icon — Predefined icon (Using a predefined icon for the hotspots.)
- globalIconImage : image (chemin ou URL), si globalIconType = image — Uploaded image (Use your own image for the hotspots icon. 75px by 75px is recommended for your image.)
- globalColor : texte, défaut #981d99, si globalIconType = icon|numbers — Hotspot color (The color of the hotspots)
- hotspots* : liste (min 1) — Hotspots
  chaque élément :
    - position : groupe — Hotspot position (Click on the thumbnail image to place the hotspot)
      - x* : nombre
      - y* : nombre
      - legacyPositioning : booléen
    - hotspotIconType : choix default|icon|image, défaut default — Custom hotspot icon
    - hotspotIcon : choix plus|minus|times|check|question|info|exclamation, défaut plus, si hotspotIconType = icon — Predefined icon (Using a predefined icon for the hotspot.)
    - hotspotIconImage : image (chemin ou URL), si hotspotIconType = image — Uploaded image (Use your own image for the hotspot icon. 75px by 75px is recommended for your image.)
    - hotspotColor : texte, défaut #981d99, si hotspotIconType = icon — Hotspot color (The color of the hotspot)
    - alwaysFullscreen : booléen — Cover entire background image (When the user clicks the hotspot the popup will cover the entire background image)
    - header : texte — Header (Optional header for the popup. This is used by assistive technologies.)
    - content : liste — Popup content
      chaque élément = sous-contenu, library: texte-simple | video | image | audio — Content Item

Textes d'interface pré-remplis en français (ne pas fournir sauf besoin) : untitledHotspotLabel, closeButtonLabel, containsAudioVideoLabel.

## Exemple complet (validé : validateur officiel H5P + affichage)

Fichier `sources/exemples/image-interactive.md` (médias dans `sources/exemples/media/`).

````markdown
---
type: image-interactive
title: Lire un paysage rural
language: fr
preset: decouverte
license: CC BY-SA 4.0
authors: Équipe de SVT
---
![Paysage rural avec une maison, un arbre, une prairie et le Soleil](media/paysage.jpg)

## 85,19 Le Soleil
Le **Soleil** est une étoile. Il fournit l'**énergie lumineuse** que les végétaux
chlorophylliens utilisent pour la *photosynthèse*.

## 60,47 L'arbre
Un arbre est un **producteur primaire** :

- il absorbe le CO₂ de l'air ;
- il rejette du dioxygène (O₂) le jour.

![Schéma simplifié de la silhouette d'un conifère](media/triangle-vert.png)

## 23,55 La maison
Quelles traces de l'**activité humaine** repères-tu dans ce paysage ? Écoute le signal puis réponds dans ton cahier.

![Signal sonore](media/bip.wav)

## 50,88 La prairie
![Photographie aérienne du même paysage](media/avant.jpg)

```yaml
globalIconType: icon
globalIcon: info
globalColor: "#1e6fb8"
```
````
