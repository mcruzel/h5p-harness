# Chart — `graphique`

H5P.Chart 1.2 · alias : graphique, chart · syntaxe Markdown simplifiée : oui

## Syntaxe Markdown

Ligne facultative `type: barres` (ou `secteurs`, par défaut), puis une donnée par ligne : `- Libellé : valeur` (couleur facultative `#rrggbb` en fin de ligne).

```markdown
type: barres
- Chats : 12
- Chiens : 8
- Poissons : 3 #1f77b4
```

## Champs (bloc ```yaml, noms H5P)

`*` = obligatoire ; les autres champs ont une valeur par défaut ou sont facultatifs.

- graphMode : choix pieChart|barChart, défaut pieChart — Type de graphique
- listOfTypes* : liste (min 1) — Données
  chaque élément :
    - text* : texte — Nom
    - value : nombre, min 0.0001, défaut 1 — Valeur
    - color : couleur #rrggbb, défaut #000 — Couleur
    - fontColor : couleur #rrggbb, défaut #fff — Couleur de la police

Textes d'interface pré-remplis en français (ne pas fournir sauf besoin) : figureDefinition.

## Exemple complet (validé : validateur officiel H5P + affichage)

Fichier `tests/examples/graphique.md` (médias dans `tests/media/`).

```markdown
---
type: graphique
title: La production d'électricité en France (2023)
language: fr
preset: decouverte
license: CC BY-SA 4.0
authors: Équipe de physique-chimie
---
type: barres
- Nucléaire : 65 #f2c200
- Hydraulique : 12 #1e6fb8
- Éolien : 10 #2ca02c
- Gaz : 6 #7f7f7f
- Solaire : 5,5 #ff7f0e
- Autres : 1,5 #8c564b
```
