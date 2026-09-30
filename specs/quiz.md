# Question Set — `quiz`

H5P.QuestionSet 1.21 · alias : quiz, questionset, question-set · syntaxe Markdown simplifiée : oui

## Syntaxe Markdown

Introduction facultative (page d'accueil ; une première ligne `# Titre` devient son titre), puis une section `## <type>` par question, écrite avec la syntaxe Markdown de ce type. Types acceptés par le quiz : `qcm`, `vf` (ou `vf: faux`), `trous`, `glisser-mots`, `marquer-mots`, `redaction`, `glisser-deposer`, `choix-images`.

```markdown
# Révisions
Révise les organites.

## qcm
Siège de la photosynthèse ?
- [x] Chloroplaste
- [ ] Noyau

## vf: faux
La mitochondrie contient de la chlorophylle.

## trous
L'ADN se trouve dans le {{noyau}}.
```

## Champs (bloc ```yaml, noms H5P)

`*` = obligatoire ; les autres champs ont une valeur par défaut ou sont facultatifs. Libellés et descriptions : ceux de la bibliothèque (anglais) ; valeurs par défaut : en français.

- introPage : groupe — Quiz introduction
  - showIntroPage : booléen — Display introduction
  - title : texte — Title (This title will be displayed above the introduction text.)
  - introduction : texte riche (Markdown: code em strong sub sup) — Introduction text (This text will be displayed before the quiz starts.)
  - startButtonText : texte, défaut Commencer — Start button text
  - backgroundImage : image (chemin ou URL) — Cover image (Optional image to display on the cover.)
  - backgroundImageAltText : texte — Alternative text (If the browser can't load the image this text will be displayed instead. Also used by "text-to-speech" readers.)
- progressType : choix textual|dots, défaut dots — Progress indicator (Question set progress indicator style. Will be Textual if backwards navigation is disabled.)
- passPercentage : nombre, min 0, max 100, défaut 50 — Pass percentage (Percentage of Total score required for passing the quiz.)
- questions* : liste (min 1) — Questions
  chaque élément = sous-contenu, library: qcm | glisser-deposer | trous | marquer-mots | glisser-mots | vf | redaction | choix-images — Question type (Library for this question.)
- disableBackwardsNavigation : booléen, défaut false — Disable backwards navigation (This option will only allow you to move forward in Question Set)
- randomQuestions : booléen, défaut false — Randomize questions (Enable to randomize the order of questions on display.)
- poolSize : nombre, min 1 — Number of questions to be shown: (Create a randomized batch of questions from the total.)
- endGame : groupe — Quiz finished
  - showResultPage : booléen, défaut true — Display results
  - showSolutionButton : booléen, défaut true — Display solution button
  - showRetryButton : booléen, défaut true — Display retry button
  - noResultMessage : texte, défaut Terminé — No results message (Text displayed on end page when "Display results" is disabled)
  - message : texte, défaut Résultats — Results heading (This heading will be displayed at the end of the quiz when the user has answered all questions.)
  - amountCorrect : texte, défaut Réponses correctes : @finals … — Amount correct heading (Header to show the final score to the user on the end screen)
  - scoreBarLabel : texte, défaut Vous avez obtenu @finals sur … — Score announcer (This label will be used for announcing the final score to the user on the end screen)
  - scoreHeader : texte, défaut Score — Score heading (Header for the score part of the results table)
  - overallFeedback : groupe — Overall Feedback (groupe à un champ: écrire directement la valeur)
    - overallFeedback : liste (min 1) — Define custom feedback for any score range (Click the "Add range" button to add as many ranges as you need. Example: 0-20% Bad score, 21-91% Average Score, 91-100% Great Score!)
      chaque élément :
        - from : nombre, min 0, max 100, défaut 0 — Score Range
        - to : nombre, min 0, max 100, défaut 100
        - feedback : texte — Feedback for defined score range
  - solutionButtonText : texte, défaut Voir la solution — Solution button label (Text for the solution button.)
  - retryButtonText : texte, défaut Recommencer — Retry button label (Text for the retry button.)
  - finishButtonText : texte, défaut Terminer — Finish button text
  - submitButtonText : texte, défaut Soumettre — Submit button text
  - showAnimations : booléen — Display video before quiz results
  - skippable : booléen — Enable skip video button
  - skipButtonText : texte, défaut Passer la vidéo — Skip video button label
  - successVideo : vidéo (URL YouTube/Vimeo, chemin ou URL) — Passed video (This video will be played if the user successfully passed the quiz.)
  - failVideo : vidéo (URL YouTube/Vimeo, chemin ou URL) — Fail video (This video will be played if the user fails the quiz.)
- override : groupe — Behavioural settings
  - checkButton : booléen, défaut true — Show "Check" buttons (This option determines if the "Check" button will be shown for all questions.)
  - showSolutionButton : choix on|off, si checkButton = True — Override "Show Solution" button (This option determines if the "Show Solution" button will be shown for all questions, disabled for all or configured for each question individually.)
  - retryButton : choix on|off, si checkButton = True — Override "Retry" button (This option determines if the "Retry" button will be shown for all questions, disabled for all or configured for each question individually.)
  - backgroundImage : image (chemin ou URL) — Background image (An optional background image for the Question set.)

Textes d'interface pré-remplis en français (ne pas fournir sauf besoin) : texts.

## Exemple complet (validé : validateur officiel H5P + affichage)

Fichier `tests/examples/quiz.md` (médias dans `tests/media/`).

````markdown
---
type: quiz
title: Quiz – La Seconde Guerre mondiale
language: fr
license: CC BY-SA 4.0
preset: evaluation
---
Réponds aux questions pour vérifier tes connaissances sur la période **1939-1945**.

## qcm
Quels pays faisaient partie des **Alliés** en 1944 ?
- [x] Le Royaume-Uni
- [x] Les États-Unis
- [ ] L'Italie de Mussolini
  > Non : l'Italie fasciste était alliée à l'Allemagne jusqu'en 1943.
- [ ] Le Japon

## vf: faux
Le débarquement de Normandie a eu lieu le 8 mai 1945.

## trous
Complète avec les bonnes dates.

La guerre commence en {{1939}} avec l'invasion de la {{Pologne}}.

## glisser-mots
Place les noms au bon endroit.

{{De Gaulle}} lance l'appel du 18 juin 1940 depuis {{Londres}}.
Distracteurs: Pétain, Vichy

## marquer-mots
Clique sur les noms des **dirigeants alliés**.

À Yalta, {{Roosevelt}}, {{Churchill}} et {{Staline}} discutent de l'après-guerre, tandis qu'Hitler est encore au pouvoir.

## redaction
En quelques lignes, explique pourquoi l'année 1942 est un tournant de la guerre.

- Stalingrad
- Midway
- El Alamein | El-Alamein

```yaml
passPercentage: 60
progressType: textual
endGame:
  amountCorrect: "@finals point(s) sur @totals"
  overallFeedback:
    - {from: 0, to: 59, feedback: "Relis ton cours et réessaie."}
    - {from: 60, to: 100, feedback: "Bon travail !"}
```
````
