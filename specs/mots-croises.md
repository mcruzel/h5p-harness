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

- taskDescription : texte riche (Markdown: a code em h2 h3 hr li ol pre strong u ul) — Consigne
- words* : liste (min 2) — mots
  chaque élément :
    - clue* : texte — Indice
    - answer* : texte — Réponse
    - extraClue : sous-contenu, library: texte | image | audio | video — Indice supplémentaire
    - fixWord : booléen, défaut false — Fixer le mot sur la grille
    - row : nombre, min 1, max 100, conditionnel — Ligne
    - column : nombre, min 1, max 100, conditionnel — Colonne
    - orientation : choix across|down, défaut across, conditionnel — Orientation
- solutionWord : texte — Mot solution
- overallFeedback : groupe — Feedback général (groupe à un champ: écrire directement la valeur)
  - overallFeedback : liste (min 1) — Définissez le feedback pour chaque intervalle de score
    chaque élément :
      - from : nombre, min 0, max 100, défaut 0 — Intervalle de score
      - to : nombre, min 0, max 100, défaut 100
      - feedback : texte — Feedback pour l'intervalle de score défini
- theme : groupe — Thème
  - backgroundImage : image (chemin ou URL) — Image d'arrière-plan
  - backgroundColor : couleur #rrggbb, défaut #173354 — Couleur d'arrière-plan
- behaviour : réglages — Paramètres de comportement
  poolSize=…, enableInstantFeedback=false, scoreWords=true, applyPenalties=false, enableRetry=true, enableSolutionsButton=true, keepCorrectAnswers=false, addExtraMarkerForEmptyCells=false

Textes d'interface pré-remplis en français (ne pas fournir sauf besoin) : l10n, a11y.
