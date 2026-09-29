# Summary — `resume`

H5P.Summary 1.10 · alias : resume, summary · syntaxe Markdown simplifiée : oui

## Syntaxe Markdown

Paragraphe(s) d'introduction, puis des séries d'affirmations (une section `##` par série, ou des listes séparées par une ligne vide). Dans chaque série, une seule `- [x]` correcte ; `? indice` indenté optionnel.

```markdown
Choisis l'affirmation correcte dans chaque série.

## Série 1
- [x] La Terre tourne autour du Soleil.
- [ ] Le Soleil tourne autour de la Terre.

## Série 2
- [x] L'eau bout à 100 °C au niveau de la mer.
- [ ] L'eau bout à 50 °C au niveau de la mer.
```

## Champs (bloc ```yaml, noms H5P)

`*` = obligatoire ; les autres champs ont une valeur par défaut ou sont facultatifs.

- intro : texte riche (Markdown: a code em h2 h3 hr li ol pre strong u ul), défaut Choisissez l'affirmation exac… — Texte d'introduction
- summaries* : liste (min 1, max 100) — Résumé
  chaque élément :
    - summary* : liste (min 2) — Liste des affirmations pour le résumé - la première affirmation de la…
      chaque élément = texte riche (Markdown) — affirmation
    - tip : groupe — Indice (groupe à un champ: écrire directement la valeur)
      - tip : texte riche (Markdown: code em strong) — Indice
- overallFeedback : groupe — Feedback général (groupe à un champ: écrire directement la valeur)
  - overallFeedback : liste (min 1) — Définissez le feedback pour chaque intervalle de score
    chaque élément :
      - from : nombre, min 0, max 100, défaut 0 — Intervalle de score
      - to : nombre, min 0, max 100, défaut 100
      - feedback : texte — Feedback pour l'intervalle de score défini

Textes d'interface pré-remplis en français (ne pas fournir sauf besoin) : solvedLabel, scoreLabel, resultLabel, labelCorrect, labelIncorrect, alternativeIncorrectLabel, labelCorrectAnswers, tipButtonLabel, scoreBarLabel, progressText.
