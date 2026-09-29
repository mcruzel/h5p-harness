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

`*` = obligatoire ; les autres champs ont une valeur par défaut ou sont facultatifs.

- taskDescription : texte riche (Markdown: a code em h2 h3 hr li ol pre strong u ul) — Consigne (Décrivez votre tâche ici.)
- words* : liste (min 2) — mots
  chaque élément :
    - clue* : texte — Indice (Indice permettant de trouver la réponse.)
    - answer* : texte — Réponse (Réponse correspondant à l'indice.)
    - extraClue : sous-contenu, library: texte | image | audio | video — Indice supplémentaire
    - fixWord : booléen, défaut false — Fixer le mot sur la grille (Cochez si vous souhaitez fixer le mot à une position particulière sur la grille. Les mots avec le même aligne…)
    - row : nombre, min 1, max 100, conditionnel — Ligne (Index de la ligne où la réponse doit commencer.)
    - column : nombre, min 1, max 100, conditionnel — Colonne (Index de la colonne où la réponse doit commencer.)
    - orientation : choix across|down, défaut across, conditionnel — Orientation (Orientation de la réponse.)
- solutionWord : texte — Mot solution (Ajouter un mot solution optionnel qui peut être découvert à partir de certaines lettres sur la grille. Sera s…)
- overallFeedback : groupe — Feedback général (groupe à un champ: écrire directement la valeur)
  - overallFeedback : liste (min 1) — Définissez le feedback pour chaque intervalle de score (Cliquez sur le bouton "Ajouter Intervalle" pour ajouter autant d'intervalles de score que vous souhaitez. Exe…)
    chaque élément :
      - from : nombre, min 0, max 100, défaut 0 — Intervalle de score
      - to : nombre, min 0, max 100, défaut 100
      - feedback : texte — Feedback pour l'intervalle de score défini
- theme : groupe — Thème
  - backgroundImage : image (chemin ou URL) — Image d'arrière-plan (Sélectionnez une image d'arrière-plan pour votre activité (facultatif). Elle sera mise à l’échelle pour s'ada…)
  - backgroundColor : couleur #rrggbb, défaut #173354 — Couleur d'arrière-plan (Choisir une couleur d'arrière-plan. Elle sera utilisée soit pour remplacer l'image de fond ou comme arrière-p…)
- behaviour : réglages — Paramètres de comportement (Ces options permettent de contrôler le comportement de l'activité.)
  poolSize=…, enableInstantFeedback=false, scoreWords=true, applyPenalties=false, enableRetry=true, enableSolutionsButton=true, keepCorrectAnswers=false, addExtraMarkerForEmptyCells=false

Textes d'interface pré-remplis en français (ne pas fournir sauf besoin) : l10n, a11y.

## Exemple complet (validé : validateur officiel H5P + affichage)

Fichier `tests/examples/mots-croises.md` (médias dans `tests/media/`).

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
