# Essay — `redaction`

H5P.Essay 1.6 · alias : redaction, essay · syntaxe Markdown simplifiée : oui

## Syntaxe Markdown

Consigne en Markdown, puis les mots-clés attendus : `- mot-clé | variante (2 pts)` (points facultatifs). Paragraphe optionnel introduit par une ligne `Exemple:` = réponse modèle montrée à la fin.

```markdown
Explique le rôle de la chlorophylle.

- lumière | lumineuse (2 pts)
- chloroplaste
- photosynthèse (2 pts)

Exemple:
La chlorophylle capte l'énergie lumineuse dans les chloroplastes…
```

## Champs (bloc ```yaml, noms H5P)

`*` = obligatoire ; les autres champs ont une valeur par défaut ou sont facultatifs. Libellés et descriptions : ceux de la bibliothèque (anglais) ; valeurs par défaut : en français.

- media : groupe — Media
  - type : sous-contenu, library: image | video | audio — Type (Optional media to display above the question.)
  - disableImageZooming : booléen, défaut false, si type = H5P.Image — Disable image zooming
- taskDescription* : texte riche (Markdown: a code em h2 h3 hr li ol pre strong u ul) — Task description (Describe your task here. The task description will appear above text input area.)
- placeholderText : texte — Help text (This text should help the user to get started.)
- solution : groupe — Sample solution (You can optionally add a sample solution that's shown after the student created a text. It's called sample solution because there probably is not only one solution.)
  - introduction : texte riche (Markdown: a code em hr li ol strong u ul) — Introduction (You can optionally leave the students some explanations about your example. The explanation will only show up if you add an example, too.)
  - sample : texte riche (Markdown: a strong) — Sample solution text (The student will see a "Show solution" button after submitting if you provide some text here.)
- keywords* : liste (min 1) — Keywords
  chaque élément :
    - keyword* : texte — Keyword (Keyword or phrase to look for. Use an asterisk '*' as a wildcard for one or more characters. Use a slash '/' at the beginning and the end to use a regular expression.)
    - alternatives : liste (min 0) — Variations (Add optional variations for this keyword. Example: For a 'city' add alternatives 'town', 'municipality' etc. Points will be awarded if the user includes any of the specified alternatives.)
      chaque élément = texte — Keyword variation
    - options : groupe — Points, Options and Feedback
      - points : nombre, min 0, défaut 1 — Points (Points that the user will get if he/she includes this keyword or its alternatives in the answer.)
      - occurrences : nombre, min 1, défaut 1 — Occurrences (Define how many occurrences of the keyword or its variations should be awarded with points.)
      - caseSensitive : booléen, défaut true — Case sensitive (Makes sure the user input has to be exactly the same as the answer.)
      - forgiveMistakes : booléen — Forgive minor mistakes (This will accept minor spelling mistakes (3-9 characters: 1 mistake, more than 9 characters: 2 mistakes).)
      - feedbackIncluded : texte — Feedback if keyword included (This feedback will be displayed if the user includes this keyword or its alternatives in the answer.)
      - feedbackMissed : texte — Feedback if keyword missing (This feedback will be displayed if the user doesn’t include this keyword or its alternatives in the answer.)
      - feedbackIncludedWord : choix keyword|alternative|answer|none, défaut keyword — Feedback word shown if keyword included (This option allows you to specify which word should be shown in front of your feedback if a keyword was found in the text.)
      - feedbackMissedWord : choix keyword|none, défaut none — Feedback word shown if keyword missing (This option allows you to specify which word should be shown in front of your feedback if a keyword was not found in the text.)
- overallFeedback : groupe — Overall Feedback (groupe à un champ: écrire directement la valeur)
  - overallFeedback : liste (min 1) — Define custom feedback for any score range (Click the "Add range" button to add as many ranges as you need. Example: 0-20% Bad score, 21-91% Average Score, 91-100% Great Score!)
    chaque élément :
      - from : nombre, min 0, max 100, défaut 0 — Score Range
      - to : nombre, min 0, max 100, défaut 100
      - feedback : texte — Feedback for defined score range
- behaviour : réglages — Behavioural settings (These options will let you control how the task behaves.)
  minimumLength=…, maximumLength=…, inputFieldSize=10 (1|3|10), enableRetry=true, ignoreScoring=false, pointsHost=1, percentagePassing=…, percentageMastering=…, overrideCaseSensitive= (on|off), overrideForgiveMistakes= (on|off), linebreakReplacement=  ( |
)

Textes d'interface pré-remplis en français (ne pas fournir sauf besoin) : checkAnswer, submitAnswer, tryAgain, showSolution, feedbackHeader, solutionTitle, remainingChars, notEnoughChars, messageSave, ariaYourResult, ariaNavigatedToSolution, ariaCheck, ariaShowSolution, ariaRetry.

## Exemple complet (validé : validateur officiel H5P + affichage)

Fichier `sources/exemples/redaction.md` (médias dans `sources/exemples/media/`).

````markdown
---
type: redaction
title: Rédaction – La photosynthèse
language: fr
license: CC BY-SA 4.0
---
En **cinq lignes maximum**, explique comment une plante verte fabrique sa matière organique.

- lumière | lumineuse (2 pts)
- chlorophylle
- dioxyde de carbone | CO2 (2 pts)
- eau | H2O

Exemple:
Grâce à la **chlorophylle** contenue dans ses chloroplastes, la plante capte l'énergie lumineuse. Elle l'utilise pour fabriquer du glucose à partir de l'eau puisée par les racines et du dioxyde de carbone de l'air : c'est la photosynthèse.

```yaml
placeholderText: "Rédige ta réponse ici…"
behaviour:
  minimumLength: 100
  maximumLength: 600
  percentagePassing: 50
  percentageMastering: 90
```
````
