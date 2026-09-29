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

`*` = obligatoire ; les autres champs ont une valeur par défaut ou sont facultatifs.

- media : groupe — Média
  - type : sous-contenu, library: image | video | audio — Type
  - disableImageZooming : booléen, défaut false, conditionnel — Disable image zooming
- taskDescription* : texte riche (Markdown: a code em h2 h3 hr li ol pre strong u ul) — Task description
- placeholderText : texte — Texte d'aide
- solution : groupe — Exemple de solution
  - introduction : texte riche (Markdown: a code em hr li ol strong u ul) — Introduction
  - sample : texte riche (Markdown: a strong) — Texte pour la solution
- keywords* : liste (min 1) — Mots clés
  chaque élément :
    - keyword* : texte — Mot clé
    - alternatives : liste (min 0) — Réponses alternatives
      chaque élément = texte — mot clé
    - options : groupe — Points, Options et Feedback
      - points : nombre, min 0, défaut 1 — Points
      - occurrences : nombre, min 1, défaut 1 — Apparitions
      - caseSensitive : booléen, défaut true — Sensible à la casse
      - forgiveMistakes : booléen — Accepter de petites fautes d'orthographe
      - feedbackIncluded : texte — Feedback si le mot clé est inclus
      - feedbackMissed : texte — Feedback si le mot clé est absent
      - feedbackIncludedWord : choix keyword|alternative|answer|none, défaut keyword — Feedback word shown if keyword included
      - feedbackMissedWord : choix keyword|none, défaut none — Feedback word shown if keyword missing
- overallFeedback : groupe — Feedback Global (groupe à un champ: écrire directement la valeur)
  - overallFeedback : liste (min 1) — Définit le feedback pour chaque intervalle de scores
    chaque élément :
      - from : nombre, min 0, max 100, défaut 0 — Intervalle de scores
      - to : nombre, min 0, max 100, défaut 100
      - feedback : texte — Feedback de l'intervalle de scores défini
- behaviour : réglages — Behavioural settings
  minimumLength=…, maximumLength=…, inputFieldSize=10 (1|3|10), enableRetry=true, ignoreScoring=false, pointsHost=1, percentagePassing=…, percentageMastering=…, overrideCaseSensitive= (on|off), overrideForgiveMistakes= (on|off), linebreakReplacement=  ( |
)

Textes d'interface pré-remplis en français (ne pas fournir sauf besoin) : checkAnswer, submitAnswer, tryAgain, showSolution, feedbackHeader, solutionTitle, remainingChars, notEnoughChars, messageSave, ariaYourResult, ariaNavigatedToSolution, ariaCheck, ariaShowSolution, ariaRetry.

## Exemple complet (validé : validateur officiel H5P + affichage)

Fichier `tests/examples/redaction.md` (médias dans `tests/media/`).

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
