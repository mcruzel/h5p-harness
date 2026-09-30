# Guess the Answer — `devinette`

H5P.GuessTheAnswer 1.5 · alias : devinette, guesstheanswer, guess-the-answer · syntaxe Markdown simplifiée : oui

## Syntaxe Markdown

Consigne en Markdown, une ligne `![description](image ou vidéo)`, puis `Réponse: …` (texte révélé au clic) et, facultatif, `Bouton: …` (libellé du bouton).

```markdown
Quel est cet organe ?
![Radiographie](images/radio.png)
Réponse: Le cœur.
```

## Champs (bloc ```yaml, noms H5P)

`*` = obligatoire ; les autres champs ont une valeur par défaut ou sont facultatifs. Libellés et descriptions : ceux de la bibliothèque (anglais) ; valeurs par défaut : en français.

- taskDescription : texte riche (Markdown: a code em h2 h3 hr li ol pre strong u ul) — Task description (Describe how the user should solve the task.)
- media : groupe — Media (groupe à un champ: écrire directement la valeur)
  - type : sous-contenu, library: image | video — Type (Optional media to display above the question.)
- solutionLabel : texte multiligne, défaut Cliquer pour voir la réponse. — Descriptive solution label (Clickable text area where the solution will be displayed.)
- solutionText* : texte multiligne — Solution text (The solution for the picture.)

## Exemple complet (validé : validateur officiel H5P + affichage)

Fichier `sources/exemples/devinette.md` (médias dans `sources/exemples/media/`).

````markdown
---
type: devinette
title: Devinette – Quelle est cette figure ?
language: fr
license: CC BY-SA 4.0
---
```yaml
taskDescription: |
  Observe bien la figure ci-dessous.

  Combien a-t-elle de **côtés** et comment s'appelle-t-elle ?
media:
  library: image
  file: media/hexagone-gris.png
  alt: Une figure géométrique grise
solutionLabel: Clique pour voir la réponse
solutionText: "C'est un hexagone régulier : il a 6 côtés de même longueur."
```
````
