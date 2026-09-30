# Sort the Paragraphs — `trier-paragraphes`

H5P.SortParagraphs 0.12 · alias : trier-paragraphes, sortparagraphs, sort-paragraphs · syntaxe Markdown simplifiée : oui

## Syntaxe Markdown

Consigne facultative, puis les paragraphes **dans l'ordre correct**, un par ligne `- …` (lignes suivantes indentées pour continuer un paragraphe). Ils sont mélangés à l'affichage.

```markdown
Remets les étapes de la mitose dans l'ordre.

- Prophase : les chromosomes se condensent.
- Métaphase : ils s'alignent au centre.
- Anaphase : les chromatides se séparent.
- Télophase : deux noyaux se forment.
```

## Champs (bloc ```yaml, noms H5P)

`*` = obligatoire ; les autres champs ont une valeur par défaut ou sont facultatifs. Libellés et descriptions : ceux de la bibliothèque (anglais) ; valeurs par défaut : en français.

- media : groupe — Media
  - type : sous-contenu, library: image | video | audio — Type (Optional media to display above the question.)
  - disableImageZooming : booléen, défaut false, si type = H5P.Image — Disable image zooming
- taskDescription* : texte riche (Markdown: a code em h2 h3 hr li ol pre strong u ul) — Task description (What your students should know.)
- paragraphs* : liste (min 3) — Paragraphs
  chaque élément = texte riche (Markdown: code em h2 h3 hr li ol pre strong u ul) — Paragraph
- overallFeedback : groupe — Overall Feedback (groupe à un champ: écrire directement la valeur)
  - overallFeedback : liste (min 1) — Define custom feedback for any score range (Click the "Add range" button to add as many ranges as you need. Example: 0-20% Bad score, 21-91% Average Score, 91-100% Great Score!)
    chaque élément :
      - from : nombre, min 0, max 100, défaut 0 — Score Range
      - to : nombre, min 0, max 100, défaut 100
      - feedback : texte — Feedback for defined score range
- behaviour : réglages — Behavioural settings (These options will let you control how the task behaves.)
  scoringMode=positions (positions|transitions), applyPenalties=true, duplicatesInterchangeable=true, addButtonsForMovement=true, enableRetry=true, enableSolutionsButton=true

Textes d'interface pré-remplis en français (ne pas fournir sauf besoin) : l10n, a11y.

## Exemple complet (validé : validateur officiel H5P + affichage)

Fichier `tests/examples/trier-paragraphes.md` (médias dans `tests/media/`).

````markdown
---
type: trier-paragraphes
title: Remettre en ordre – La digestion
language: fr
license: CC BY-SA 4.0
---
Remets dans l'ordre les étapes du trajet des aliments dans le **tube digestif**.

- Dans la **bouche**, les dents broient les aliments et la salive commence la digestion.
- L'**œsophage** conduit les aliments jusqu'à l'estomac.
- Dans l'**estomac**, le suc gastrique poursuit la digestion.
  Les aliments y restent plusieurs heures.
- Dans l'**intestin grêle**, les nutriments passent dans le sang.
- Le **gros intestin** récupère l'eau ; les déchets forment les selles.

```yaml
behaviour:
  scoringMode: transitions
overallFeedback:
  - {from: 0, to: 79, feedback: "Relis le schéma du tube digestif."}
  - {from: 80, to: 100, feedback: "Excellent !"}
```
````
