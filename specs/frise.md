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

## Champs (bloc ```yaml, noms H5P)

`*` = obligatoire ; les autres champs ont une valeur par défaut ou sont facultatifs.

- timeline : groupe — Chronologie
  - headline* : texte — Titre
  - text : texte riche (Markdown: a code del em hr li ol s strong ul) — Corps du texte
  - defaultZoomLevel : texte, défaut 0 — Niveau de zoom par défaut
  - backgroundImage : image (chemin ou URL) — Image d'arrière-plan'
  - height : nombre, défaut 600 — Hauteur
  - asset : groupe — Média
    - media : texte — Adresse URL du média
    - credit : texte — Crédits
    - caption : texte — Légende
  - date* : liste (min 1) — Dates
    chaque élément :
      - startDate* : texte — Date de début
      - endDate : texte — Date de fin
      - headline* : texte — Titre
      - text : texte riche (Markdown: a code del em h2 h3 hr li ol pre s strong ul) — Texte
      - tag : texte — Etiquettes
      - asset : groupe — Média
        - media : texte — Adresse URL du média
        - thumbnail : image (chemin ou URL) — Image miniature
        - credit : texte — Crédits
        - caption : texte — Légende
  - era : liste (min 0) — Périodes
    chaque élément :
      - startDate* : texte — Date de début
      - endDate : texte — Date de fin
      - headline* : texte — Titre
      - text : texte riche (Markdown: a code del em hr li ol s strong ul) — Contenu
      - tag : texte — Etiquette
  - language : choix af|ar|hy|eu|bg|ca|zh-cn|hr|cz|da|…, défaut en — Langue

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
