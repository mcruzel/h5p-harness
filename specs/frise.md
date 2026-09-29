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

`*` = obligatoire ; les autres champs ont une valeur par défaut ou sont facultatifs.

- timeline : groupe — Chronologie
  - headline* : texte — Titre (Entrez ici le titre principal de la chronologie (première page))
  - text : texte riche (Markdown: a code del em hr li ol s strong ul) — Corps du texte (Entrez ici le corps de texte principal de la chronologie (première page).)
  - defaultZoomLevel : texte, défaut 0 — Niveau de zoom par défaut (Cela va modifier le niveau de zoom par défaut. Equivalent à appuyer sur le bouton zoom avant ou zoom arrière …)
  - backgroundImage : image (chemin ou URL) — Image d'arrière-plan' (Affiche une image de fond.)
  - height : nombre, défaut 600 — Hauteur (La hauteur en pixels)
  - asset : groupe — Média (Here you can add an asset to your timeline "front page")
    - media : texte — Adresse URL du média (Lien vers l'URL du fichier média (Twitter, YouTube, Flickr, Vimeo, Google Maps et SoundCloud sont autorisés à…)
    - credit : texte — Crédits (Crédits du fichier média)
    - caption : texte — Légende (Saisissez ici la légende du fichier média)
  - date* : liste (min 1) — Dates (Ajoutez des dates à votre chronologie !)
    chaque élément :
      - startDate* : texte — Date de début (AAAA,MM,JJ (AAAA est un minimum obligatoire))
      - endDate : texte — Date de fin (AAAA,MM,JJ (AAAA est un minimum obligatoire))
      - headline* : texte — Titre (Titre de l'événement)
      - text : texte riche (Markdown: a code del em h2 h3 hr li ol pre s strong ul) — Texte (Texte associé à l'événement)
      - tag : texte — Etiquettes (Saisissez les étiquettes (catégories))
      - asset : groupe — Média
        - media : texte — Adresse URL du média (Lien vers l'URL du fichier média (Twitter, YouTube, Flickr, Vimeo, Wikipedia, Google Maps et SoundCloud sont …)
        - thumbnail : image (chemin ou URL) — Image miniature (Ajoutez au besoin une miniature 32x32)
        - credit : texte — Crédits (Crédits du fichier média)
        - caption : texte — Légende (Légende du fichier média)
  - era : liste (min 0) — Périodes (Ajoutez une période à votre chronologie)
    chaque élément :
      - startDate* : texte — Date de début (AAAA,MM,JJ (AAAA est un minimum obligatoire))
      - endDate : texte — Date de fin (AAAA,MM,JJ (AAAA est un minimum obligatoire))
      - headline* : texte — Titre (Titre de la période)
      - text : texte riche (Markdown: a code del em hr li ol s strong ul) — Contenu (Contenu de la période)
      - tag : texte — Etiquette (Etiquettes de la période (catégories))
  - language : choix af|ar|hy|eu|bg|ca|zh-cn|hr|cz|da|…, défaut en — Langue (Choisissez la langue de l'interface)

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
