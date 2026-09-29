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

`*` = obligatoire ; les autres champs ont une valeur par défaut ou sont facultatifs.

- panels* : liste (min 1, max 100) — Panneaux
  chaque élément :
    - title* : texte — Titre
    - content* : sous-contenu, library: texte — Type de contenu
- hTag : choix h2|h3|h4, défaut h2 — Balise H pour les sections (ne modifie pas la taille du bloc de l'en-…
