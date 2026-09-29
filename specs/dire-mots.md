# Speak the Words — `dire-mots`

H5P.SpeakTheWords 1.5 · alias : dire-mots, speakthewords, speak-the-words · syntaxe Markdown simplifiée : non (bloc ```yaml)

## Champs (bloc ```yaml, noms H5P)

`*` = obligatoire ; les autres champs ont une valeur par défaut ou sont facultatifs.

- media : groupe — Media
  - type : sous-contenu, library: image | video | audio — Type
  - disableImageZooming : booléen, défaut false, conditionnel — Disable image zooming
- question* : texte — Décrire la tâche
- acceptedAnswers* : liste (min 1) — Réponses acceptées
  chaque élément = texte — Réponse acceptée
- incorrectAnswerText : texte, défaut Réponse incorrecte — Texte pour une réponse incorrecte
- correctAnswerText : texte, défaut Réponse correcte — Texte pour une réponse correcte
- inputLanguage : choix af-ZA|am-ET|ar-DZ|ar-BH|ar-EG|ar-IQ|ar-JO|ar-KW|ar-LB|ar-LY|…, défaut en-US — Langue de la saisie vocale

Textes d'interface pré-remplis en français (ne pas fournir sauf besoin) : l10n.
