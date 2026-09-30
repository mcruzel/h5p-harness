# Crossword — `mots-croises`

H5P.Crossword 0.7 · alias : mots-croises, crossword · syntaxe Markdown simplifiée : oui

## Syntaxe Markdown

Consigne facultative, puis une ligne par mot : `- RÉPONSE : définition` (lettres uniquement, espaces tolérés). Au moins 2 mots qui partagent des lettres ; la grille est calculée à l'affichage.

```markdown
Retrouve les termes.

- NOYAU : Contient l'ADN
- MITOCHONDRIE : Siège de la respiration
- MEMBRANE : Enveloppe de la cellule
```

## Champs (bloc ```yaml, noms H5P)

`*` = obligatoire ; les autres champs ont une valeur par défaut ou sont facultatifs. Libellés et descriptions : ceux de la bibliothèque (anglais) ; valeurs par défaut : en français.

- taskDescription : texte riche (Markdown: a code em h2 h3 hr li ol pre strong u ul) — Task description (Describe your task here.)
- words* : liste (min 2) — words
  chaque élément :
    - clue* : texte — Clue (Clue that should point to the answer.)
    - answer* : texte — Answer (Answer to the clue.)
    - extraClue : sous-contenu, library: texte | image | audio | video — Extra clue
    - fixWord : booléen, défaut false — Fix word on grid (Check if you want to fix the word to a particular position on the grid. Words with the same alignment may not be placed touching each other.)
    - row : nombre, min 1, max 100, si fixWord = True — Row (Row index where the answer should start.)
    - column : nombre, min 1, max 100, si fixWord = True — Column (Column index where the answer should start.)
    - orientation : choix across|down, défaut across, si fixWord = True — Orientation (Orientation for the answer.)
- solutionWord : texte — Overall solution word (Optionally add a solution word that can be derived from particular characters on the grid. It will only be visible if all its characters can be found in the crossword. Please note: There's no accessibility support for t…)
- overallFeedback : groupe — Overall Feedback (groupe à un champ: écrire directement la valeur)
  - overallFeedback : liste (min 1) — Define custom feedback for any score range (Click the "Add range" button to add as many ranges as you need. Example: 0-20% Bad score, 21-91% Average Score, 91-100% Great Score!)
    chaque élément :
      - from : nombre, min 0, max 100, défaut 0 — Score Range
      - to : nombre, min 0, max 100, défaut 100
      - feedback : texte — Feedback for defined score range
- theme : groupe — Theme
  - backgroundImage : image (chemin ou URL) — Background image (Select an optional background image. It will be scaled to fit the background without stretching it.)
  - backgroundColor : couleur #rrggbb, défaut #173354 — Background color (Choose a background color. It will either be used instead of a background image or as background for transparent areas.)
- behaviour : réglages — Behavioural settings (These options will let you control how the task behaves.)
  poolSize=…, enableInstantFeedback=false, scoreWords=true, applyPenalties=false, enableRetry=true, enableSolutionsButton=true, keepCorrectAnswers=false, addExtraMarkerForEmptyCells=false

Textes d'interface pré-remplis en français (ne pas fournir sauf besoin) : l10n, a11y.

## Exemple complet (validé : validateur officiel H5P + affichage)

Fichier `sources/exemples/mots-croises.md` (médias dans `sources/exemples/media/`).

````markdown
---
type: mots-croises
title: Mots croisés – Les cours d'eau
language: fr
license: CC BY-SA 4.0
---
Complète la grille avec le vocabulaire des **cours d'eau**.

- SOURCE : Endroit où naît un cours d'eau
- AFFLUENT : Cours d'eau qui se jette dans un autre
- ESTUAIRE : Embouchure large où la mer remonte
- DELTA : Embouchure en forme de triangle, divisée en plusieurs bras
- MÉANDRE : Courbe décrite par un fleuve
- CRUE : Montée des eaux d'un cours d'eau

```yaml
solutionWord: SEINE
behaviour:
  enableInstantFeedback: true
theme:
  backgroundColor: "#1d4e89"
```
````
