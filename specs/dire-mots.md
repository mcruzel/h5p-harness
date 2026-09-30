# Speak the Words — `dire-mots`

H5P.SpeakTheWords 1.5 · alias : dire-mots, speakthewords, speak-the-words · syntaxe Markdown simplifiée : non (bloc ```yaml)

## Points d'attention

- Reconnaissance vocale du navigateur (Web Speech API) : fonctionne dans Chrome et Edge, pas dans Firefox ; l'élève autorise le micro.
- `inputLanguage` = langue de la réponse attendue (défaut : langue du document, `fr` → `fr-FR`) ; pour une réponse en anglais : `en-GB` ou `en-US`.

## Champs (bloc ```yaml, noms H5P)

`*` = obligatoire ; les autres champs ont une valeur par défaut ou sont facultatifs. Libellés et descriptions : ceux de la bibliothèque (anglais) ; valeurs par défaut : en français.

- media : groupe — Media
  - type : sous-contenu, library: image | video | audio — Type (Optional media to display above the question.)
  - disableImageZooming : booléen, défaut false, si type = H5P.Image — Disable image zooming
- question* : texte — Describe task
- acceptedAnswers* : liste (min 1) — Accepted answers
  chaque élément = texte — Accepted answer
- incorrectAnswerText : texte, défaut Réponse incorrecte — Incorrect answer text
- correctAnswerText : texte, défaut Réponse correcte — Correct answer text
- inputLanguage : choix af-ZA|am-ET|ar-DZ|ar-BH|ar-EG|ar-IQ|ar-JO|ar-KW|ar-LB|ar-LY|…, défaut en-US — Language of speech input — **défaut : la langue du document (fr → fr-FR)**

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
