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

`*` = obligatoire ; les autres champs ont une valeur par défaut ou sont facultatifs.

- media : groupe — Média
  - type : sous-contenu, library: image | video | audio — Type (Média facultatif pour afficher au-dessus de la question.)
  - disableImageZooming : booléen, défaut false, conditionnel — Bloquer le zoom d’image
- taskDescription* : texte riche (Markdown: a code em h2 h3 hr li ol pre strong u ul) — Description de la tâche (Ce que vos élèves devraient savoir.)
- paragraphs* : liste (min 3) — Paragraphes
  chaque élément = texte riche (Markdown: code em h2 h3 hr li ol pre strong u ul) — Paragraphe
- overallFeedback : groupe — Feedback général (groupe à un champ: écrire directement la valeur)
  - overallFeedback : liste (min 1) — Définir un feedback personnalisé pour n'importe quelle gamme de note (Cliquez sur la touche « Ajouter une gamme » pour ajouter autant de gammes que nécessaire. Exemple : 0-20 % ma…)
    chaque élément :
      - from : nombre, min 0, max 100, défaut 0 — Gamme de notes
      - to : nombre, min 0, max 100, défaut 100
      - feedback : texte — Feedback pour une gamme de notes définie
- behaviour : réglages — Paramètres comportementaux (Ces options vous permettront de contrôler le déroulement de la tâche.)
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
