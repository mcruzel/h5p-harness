# Speak the Words Set — `dire-mots-serie`

H5P.SpeakTheWordsSet 1.3 · alias : dire-mots-serie, speakthewordsset, speak-the-words-set · syntaxe Markdown simplifiée : non (bloc ```yaml)

## Champs (bloc ```yaml, noms H5P)

`*` = obligatoire ; les autres champs ont une valeur par défaut ou sont facultatifs.

- introduction : groupe — Introduction
  - showIntroPage : booléen, défaut false — Montrer l'introduction
  - introductionImage : image (chemin ou URL), conditionnel — Image d'introduction
  - introductionImageAltText : texte, conditionnel — Texte alternatif pour l'image d'introduction
  - introductionTitle : texte, conditionnel — Titre
  - introductionText : texte riche (Markdown: code em strong sub sup), conditionnel — Texte d'introduction
- questions* : liste (min 1) — Questions
  chaque élément = sous-contenu, library: dire-mots — Question
- overallFeedback : groupe — Feedback global (groupe à un champ: écrire directement la valeur)
  - overallFeedback : liste (min 1) — Définissez le feedback pour chaque intervalle de score
    chaque élément :
      - from : nombre, min 0, max 100, défaut 0 — Intervalle de score
      - to : nombre, min 0, max 100, défaut 100
      - feedback : texte — Feedback une intervalle de score

Textes d'interface pré-remplis en français (ne pas fournir sauf besoin) : l10n.
