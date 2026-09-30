# Accordion — `accordeon`

H5P.Accordion 1.0 · alias : accordeon, accordion · syntaxe Markdown simplifiée : oui

## Syntaxe Markdown

Une section `## Titre du panneau` par panneau, suivie de son contenu Markdown.

```markdown
## Définition
La cellule est l'unité du vivant.

## Exemples
- cellule animale
- cellule végétale
```

## Champs (bloc ```yaml, noms H5P)

`*` = obligatoire ; les autres champs ont une valeur par défaut ou sont facultatifs. Libellés et descriptions : ceux de la bibliothèque (anglais) ; valeurs par défaut : en français.

- panels* : liste (min 1, max 100) — Panels
  chaque élément :
    - title* : texte — Title
    - content* : sous-contenu, library: texte — Content type
- hTag : choix h2|h3|h4, défaut h2 — H tags for labels (does not affect the size of the label) (The h tag used on the labels. Normally H2 but if this belongs under an H2 heading use H3. Does not affect the size of the labels, only used for semantical purposes.)

## Exemple complet (validé : validateur officiel H5P + affichage)

Fichier `tests/examples/accordeon.md` (médias dans `tests/media/`).

```markdown
---
type: accordeon
title: Fiche mémo – Le théorème de Pythagore
language: fr
license: CC BY-SA 4.0
---
## Énoncé
Dans un triangle **rectangle**, le carré de la longueur de l'hypoténuse est égal à la somme des carrés des longueurs des deux autres côtés :

*BC*² = *AB*² + *AC*²

## Méthode de rédaction
1. On repère l'hypoténuse (le plus grand côté).
2. On écrit l'égalité de Pythagore.
3. On remplace par les valeurs et on calcule.

## Triplets à connaître
- 3, 4 et 5 : 3² + 4² = 9 + 16 = 25 = 5²
- 5, 12 et 13
- 8, 15 et 17

## Pour aller plus loin
La **réciproque** permet de prouver qu'un triangle est rectangle. Voir aussi [Pythagore sur Wikipédia](https://fr.wikipedia.org/wiki/Pythagore).
```
