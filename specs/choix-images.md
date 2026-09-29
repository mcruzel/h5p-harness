# Multimedia Choice — `choix-images`

H5P.MultiMediaChoice 0.3 · alias : choix-images, multimediachoice, multi-media-choice · syntaxe Markdown simplifiée : oui

## Syntaxe Markdown

Question en Markdown, puis une option par ligne : `- [x] ![description](image)` (bonne) ou `- [ ] ![description](image)` ; plusieurs `[x]` = plusieurs bonnes réponses.

## Champs (bloc ```yaml, noms H5P)

`*` = obligatoire ; les autres champs ont une valeur par défaut ou sont facultatifs.

- media : groupe — Média
  - type : sous-contenu, library: image | video | audio — Type
  - disableImageZooming : booléen, défaut false, conditionnel — Bloquer le zoom d’image
- question* : texte riche (Markdown: code em h2 h3 pre strong sub sup) — Question
- options* : liste (min 2, max 20) — Options disponibles
  chaque élément :
    - media* : sous-contenu, library: image | video | audio — Média
    - poster : image (chemin ou URL), conditionnel — Poster image
    - correct : booléen — Correcte
- overallFeedback : groupe — Feedback général (groupe à un champ: écrire directement la valeur)
  - overallFeedback : liste (min 1) — Définir un feedback personnalisé pour n'importe quelle gamme de note
    chaque élément :
      - from : nombre, min 0, max 100, défaut 0 — Gamme de notes
      - to : nombre, min 0, max 100, défaut 100
      - feedback : texte — Feedback pour une gamme de notes définie
- behaviour : réglages — Paramètres comportementaux
  enableRetry=true, enableSolutionsButton=true, confirmCheckDialog=false, confirmRetryDialog=false, singlePoint=false, showSolutionsRequiresInput=true, questionType=auto (auto|multi|single), aspectRatio=auto (auto|16to9|4to3|3to2|1to1), maxAlternativesPerRow=4 (1|2|3|4), passPercentage=100

Textes d'interface pré-remplis en français (ne pas fournir sauf besoin) : l10n.

## Exemple complet (validé : validateur officiel H5P + affichage)

Fichier `tests/examples/choix-images.md` (médias dans `tests/media/`).

````markdown
---
type: choix-images
title: Reconnaître les quadrilatères
language: fr
preset: entrainement
license: CC BY-SA 4.0
authors: Équipe de mathématiques
---
Sélectionne **toutes** les figures qui sont des **quadrilatères**.

- [x] ![Un carré rouge](../media/carre-rouge.png)
- [x] ![Un losange violet](../media/losange-violet.png)
- [ ] ![Un triangle vert](../media/triangle-vert.png)
- [ ] ![Un hexagone gris](../media/hexagone-gris.png)
- [ ] ![Un cercle bleu](../media/cercle-bleu.png)

```yaml
overallFeedback:
  - {from: 0, to: 49, feedback: Relis la définition d'un quadrilatère (polygone à 4 côtés).}
  - {from: 50, to: 99, feedback: "Presque : il manque une figure ou une figure est en trop."}
  - {from: 100, to: 100, feedback: Parfait !}
behaviour:
  aspectRatio: 4to3
  maxAlternativesPerRow: 3
```
````
