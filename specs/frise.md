# Timeline — `frise`

H5P.Timeline 1.1 · alias : frise, timeline · syntaxe Markdown simplifiée : oui

## Syntaxe Markdown

`# Titre` de la frise, introduction facultative, puis un événement par section `## date : titre` (dates `1789`, `1789-07-14`, `14/07/1789`, `-500` ; période `## 1939 → 1945 : titre`) suivie d'un texte facultatif. Remarque : ce type charge jQuery et des polices depuis les serveurs de Google à l'affichage (réseau de l'établissement).

```markdown
# La Révolution française
Quelques dates clés.

## 1789-07-14 : Prise de la Bastille
Symbole de la fin de l'Ancien Régime.

## 1792 → 1804 : Première République
```

## Points d'attention

- En YAML, les dates peuvent s'écrire `1789-07-14`, `14/07/1789` ou `1789` : le harnais les convertit au format TimelineJS `AAAA,MM,JJ`.
- `language` vaut `fr` par défaut.

## Champs (bloc ```yaml, noms H5P)

`*` = obligatoire ; les autres champs ont une valeur par défaut ou sont facultatifs. Libellés et descriptions : ceux de la bibliothèque (anglais) ; valeurs par défaut : en français.

- timeline : groupe — Timeline
  - headline* : texte — Headline (Main timeline heading goes here (first page))
  - text : texte riche (Markdown: a code del em hr li ol s strong ul) — Body Text (The main timeline body goes here (first page).)
  - defaultZoomLevel : texte, défaut 0 — Default zoom level (This will tweak the default zoom level. Equivilent to pressing the zoom in or zoom out button the specified number of times. Negative numbers zoom out. default is 0)
  - backgroundImage : image (chemin ou URL) — Background image (An image to display as background.)
  - height : nombre, défaut 600 — Height (The height in pixels)
  - asset : groupe — Asset (Here you can add an asset to your timeline "front page")
    - media : texte — Media (Link to media URL (Twitter, YouTube, Flickr, Vimeo, Google Maps and SoundCloud are currently supported))
    - credit : texte — Credits (Credits to the media)
    - caption : texte — Caption (Caption description goes here)
  - date* : liste (min 1) — Dates (Add some dates to your timeline!)
    chaque élément :
      - startDate* : texte — Start date (YYYY,MM,DD (Minimum YYYY required))
      - endDate : texte — End date (YYYY,MM,DD (Minimum YYYY required))
      - headline* : texte — Headline (Headline for the date entry)
      - text : texte riche (Markdown: a code del em h2 h3 hr li ol pre s strong ul) — Body text (Body for the date entry)
      - tag : texte — Tags (Enter Tags (categories))
      - asset : groupe — Asset
        - media : texte — Media (URL to the media (Twitter, YouTube, Flickr, Vimeo, Wikipedia, Google Maps and SoundCloud are currently supported).)
        - thumbnail : image (chemin ou URL) — Thumbnail (Add a thumbnail if needed, 32x32)
        - credit : texte — Credit (Credits to the media)
        - caption : texte — Caption (Caption text)
  - era : liste (min 0) — Eras (Add an era to your timeline)
    chaque élément :
      - startDate* : texte — Start date (YYYY,MM,DD (Minimum YYYY required))
      - endDate : texte — End date (YYYY,MM,DD (Minimum YYYY required))
      - headline* : texte — Headline (Era headline)
      - text : texte riche (Markdown: a code del em hr li ol s strong ul) — Text (Era body)
      - tag : texte — Tag (Era tags (categories))
  - language : choix af|ar|hy|eu|bg|ca|zh-cn|hr|cz|da|…, défaut en — Language (The language of the user interface)

## Exemple complet (validé : validateur officiel H5P + affichage)

Fichier `tests/examples/frise.md` (médias dans `tests/media/`).

````markdown
---
type: frise
title: La Révolution française (1789-1794)
language: fr
preset: decouverte
license: CC BY-SA 4.0
authors: Équipe d'histoire-géographie
---
# La Révolution française
Les grandes étapes de la Révolution, de la réunion des **états généraux** à la chute de Robespierre.

## 1789-05-05 : Ouverture des états généraux
Le roi Louis XVI réunit à Versailles les députés des trois ordres.

## 14/07/1789 : Prise de la Bastille
Le peuple de Paris s'empare de la forteresse, symbole de l'**arbitraire royal**.

## 1789-08-26 : Déclaration des droits de l'homme et du citoyen
« Les hommes naissent et demeurent libres et égaux en droits. »

## 1792-09-21 : Abolition de la monarchie
La Convention proclame l'abolition de la royauté ; la Iʳᵉ République commence le lendemain.

## 1793-01-21 : Exécution de Louis XVI

## 1793-09-05 → 1794-07-27 : La Terreur
Le gouvernement révolutionnaire suspend les libertés pour faire face aux dangers intérieurs et extérieurs.

```yaml
timeline:
  era:
    - {startDate: "1789,05,05", endDate: "1792,09,21", headline: Monarchie constitutionnelle}
    - {startDate: "1792,09,21", endDate: "1794,07,27", headline: Première République}
```
````
