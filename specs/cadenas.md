# Combination Lock — `cadenas`

H5P.CombinationLock 1.0 · alias : cadenas, combinationlock, combination-lock · syntaxe Markdown simplifiée : non (bloc ```yaml)

## Champs (bloc ```yaml, noms H5P)

`*` = obligatoire ; les autres champs ont une valeur par défaut ou sont facultatifs. Libellés et descriptions : ceux de la bibliothèque (anglais) ; valeurs par défaut : en français.

- introduction : texte riche (Markdown: a code col colgroup del em figcaption figure h1 h2 h3 h4 h5 h6 hr li ol pre s strong sub sup table tbody td tfoot th thead tr u ul), défaut  — Introduction (Optionally set some introduction.)
- solution : texte, défaut 0123 — Solution (Enter the desired solution for the lock. Please note that using long solutions may be suboptimal on small devices.)
- alphabet : texte, défaut 0123456789 — Symbols for each segment (Choose the symbols that each segment should bear. The symbols will appear in the order defined here.)
- behaviour : réglages — Behavioural settings
  autoCheck=true, maxAttempts=…, enableRetry=true, enableSolutionsButton=true

Textes d'interface pré-remplis en français (ne pas fournir sauf besoin) : l10n, a11y.

## Exemple complet (validé : validateur officiel H5P + affichage)

Fichier `sources/exemples/cadenas.md` (médias dans `sources/exemples/media/`).

````markdown
---
type: cadenas
title: Le cadenas des polygones
language: fr
preset: entrainement
---
```yaml
introduction: |
  ## Ouvre le cadenas !
  Le code a **4 chiffres**. Chaque chiffre est le nombre de côtés d'un polygone :

  1. un triangle ;
  2. un carré ;
  3. un hexagone ;
  4. un octogone.
# un code peut commencer par 0 (0472 reste « 0472 »)
solution: "3468"
alphabet: "0123456789"
behaviour:
  maxAttempts: 5
```
````
