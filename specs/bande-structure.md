# Structure Strip — `bande-structure`

H5P.StructureStrip 1.1 · alias : bande-structure, structurestrip, structure-strip · syntaxe Markdown simplifiée : non (bloc ```yaml)

## Champs (bloc ```yaml, noms H5P)

`*` = obligatoire ; les autres champs ont une valeur par défaut ou sont facultatifs.

- media : groupe — Média
  - type : sous-contenu, library: image | video | audio — Type (Média facultatif pour afficher au-dessus de la question.)
  - disableImageZooming : booléen, défaut false, conditionnel — Bloquer le zoom d’image
- taskDescription : texte riche (Markdown: a em h2 h3 hr li ol strong u ul) — Description de la tâche (Expliquez à vos élèves ce qu'on attend d'eux.)
- sections* : liste (min 1) — Sections
  chaque élément :
    - title* : texte — Titre
    - description : texte riche (Markdown: a em h2 h3 hr li ol strong u ul) — Indices (Ajouter éventuellement des indices ou des instructions particulières pour cette section.)
    - weight : nombre, min 1, défaut 1 — Poids (Saisir le poids de cette section par rapport aux autres sections. Le poids détermine la longueur qu'une secti…)
    - colorBackground : couleur #rrggbb, défaut #96ceb4 — Couleur de fond
    - colorText : couleur #rrggbb, défaut #1c1c1c — Couleur du texte
- behaviour : réglages — Paramètres comportementaux (Ces options vous permettront de contrôler le déroulement de la tâche.)
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
