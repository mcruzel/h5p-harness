# Structure Strip — `bande-structure`

H5P.StructureStrip 1.1 · alias : bande-structure, structurestrip, structure-strip · syntaxe Markdown simplifiée : non (bloc ```yaml)

## Champs (bloc ```yaml, noms H5P)

`*` = obligatoire ; les autres champs ont une valeur par défaut ou sont facultatifs. Libellés et descriptions : ceux de la bibliothèque (anglais) ; valeurs par défaut : en français.

- media : groupe — Media
  - type : sous-contenu, library: image | video | audio — Type (Optional media to display above the question.)
  - disableImageZooming : booléen, défaut false, si type = H5P.Image — Disable image zooming
- taskDescription : texte riche (Markdown: a em h2 h3 hr li ol strong u ul) — Task description (Explain to your students what's expected of them.)
- sections* : liste (min 1) — Sections
  chaque élément :
    - title* : texte — Title
    - description : texte riche (Markdown: a em h2 h3 hr li ol strong u ul) — Hints (Optionally add hints or particular instructions for this section.)
    - weight : nombre, min 1, défaut 1 — Weight (Determine how long each section is expected to be in relation to the other sections. Example: Section 1 = 1; Section 2 = 3 (triple the length of 1); Section 3 = 1 (same length as section 1).)
    - colorBackground : couleur #rrggbb, défaut #96ceb4 — Background color
    - colorText : couleur #rrggbb, défaut #1c1c1c — Text color
- behaviour : réglages — Behavioural settings (These options will let you control how the task behaves.)
  enableRetry=true, slack=10, textLengthMin=…, textLengthMax=…, feedbackMode=onRequest (onRequest|whileTyping)

Textes d'interface pré-remplis en français (ne pas fournir sauf besoin) : l10n, a11y.

## Exemple complet (validé : validateur officiel H5P + affichage)

Fichier `tests/examples/bande-structure.md` (médias dans `tests/media/`).

````markdown
---
type: bande-structure
title: Rédiger un paragraphe argumentatif
language: fr
---
```yaml
taskDescription: |
  Rédige un paragraphe argumentatif pour répondre à la question :
  **« Faut-il interdire les téléphones portables au collège ? »**
  Respecte la structure proposée par les bandes de couleur.
sections:
  - title: Argument
    description: Énonce ton **idée principale** en une phrase.
    weight: 1
    colorBackground: "#96ceb4"
  - title: Explication
    description: |
      Développe ton argument :

      - pourquoi est-il valable ?
      - quelles en sont les conséquences ?
    weight: 2
    colorBackground: "#ffeead"
  - title: Exemple
    description: Donne un **exemple précis** tiré de ton expérience ou de l'actualité.
    weight: 1
    colorBackground: "#ffcc5c"
behaviour:
  textLengthMin: 200
  textLengthMax: 800
  feedbackMode: whileTyping
```
````
