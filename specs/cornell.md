# Cornell Notes — `cornell`

H5P.Cornell 0.5 · alias : cornell, notes-cornell · syntaxe Markdown simplifiée : non (bloc ```yaml)

## Champs (bloc ```yaml, noms H5P)

`*` = obligatoire ; les autres champs ont une valeur par défaut ou sont facultatifs. Libellés et descriptions : ceux de la bibliothèque (anglais) ; valeurs par défaut : en français.

- headline : texte — Headline (If set, will be used for the headline of the exercise instead of the content title.)
- instructions : texte riche (Markdown: a em h2 h3 hr li ol strong u ul) — Instructions (Students will see these instructions on top of the notes.)
- exerciseContent* : sous-contenu, library: modele-3d | audio | image | texte | video — Exercise content

Textes d'interface pré-remplis en français (ne pas fournir sauf besoin) : notesFields, l10n, a11y.

## Exemple complet (validé : validateur officiel H5P + affichage)

Fichier `tests/examples/cornell.md` (médias dans `tests/media/`).

````markdown
---
type: cornell
title: Prise de notes Cornell – la photosynthèse
language: fr
---
```yaml
headline: Lis le texte puis prends des notes selon la méthode Cornell.
instructions: |
  1. Dans la colonne de gauche, note les **mots-clés** et les questions.
  2. À droite, écris tes **notes** avec tes propres mots.
  3. En bas, rédige un **résumé** de trois phrases maximum.
exerciseContent:
  library: texte
  text: |
    ## La photosynthèse

    Les plantes vertes fabriquent leur propre matière organique grâce à la **photosynthèse**.
    Ce processus a lieu dans les **chloroplastes**, qui contiennent un pigment vert : la chlorophylle.

    Pour réaliser la photosynthèse, la plante utilise :

    - de l'**eau**, prélevée dans le sol par les racines ;
    - du **dioxyde de carbone**, absorbé par les feuilles ;
    - l'**énergie lumineuse** du Soleil.

    Elle produit du **glucose**, qui lui sert de réserve d'énergie, et rejette du **dioxygène**.
```
````
