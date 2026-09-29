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

`*` = obligatoire ; les autres champs ont une valeur par défaut ou sont facultatifs.

- taskDescription : texte riche (Markdown: a code em h2 h3 hr li ol pre strong u ul) — Description de l'activité
- media : groupe — Media (groupe à un champ: écrire directement la valeur)
  - type : sous-contenu, library: image | video — Type
- solutionLabel : texte multiligne, défaut Cliquer pour voir la réponse. — Intitulé de la description de la solution
- solutionText* : texte multiligne — Texte de la Solution

## Exemple complet (validé : validateur officiel H5P + affichage)

Fichier `tests/examples/devinette.md` (médias dans `tests/media/`).

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
  file: ../media/hexagone-gris.png
  alt: Une figure géométrique grise
solutionLabel: Clique pour voir la réponse
solutionText: "C'est un hexagone régulier : il a 6 côtés de même longueur."
```
````
