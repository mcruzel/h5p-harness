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

## Exemple complet (validé : validateur officiel H5P + affichage)

Fichier `tests/examples/dire-mots.md` (médias dans `tests/media/`).

````markdown
---
type: dire-mots
title: Dis le mot – les couleurs en anglais
language: fr
---
```yaml
media:
  type:
    library: image
    file: ../media/carre-rouge.png
    alt: Un carré rouge
question: Quelle est la couleur de ce carré ? Réponds à voix haute en anglais.
acceptedAnswers:
  - red
  - it's red
  - it is red
correctAnswerText: Well done! C'est bien « red ».
incorrectAnswerText: Essaie encore, pense à la couleur des tomates.
inputLanguage: en-GB
```
````
