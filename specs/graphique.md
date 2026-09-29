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
