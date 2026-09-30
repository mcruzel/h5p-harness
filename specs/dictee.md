# Dictation — `dictee`

H5P.Dictation 1.4 · alias : dictee, dictation · syntaxe Markdown simplifiée : oui

## Syntaxe Markdown

Consigne, puis une phrase par ligne : `- ![](audio.mp3) Phrase attendue` (le son est lu, l'élève écrit la phrase) ; indication facultative après ` :: `.

```markdown
Écoute et écris chaque phrase.
- ![](audios/phrase1.mp3) Le chat dort sur le canapé. :: présent de l'indicatif
- ![](audios/phrase2.mp3) Nous irons à la plage demain.
```

## Champs (bloc ```yaml, noms H5P)

`*` = obligatoire ; les autres champs ont une valeur par défaut ou sont facultatifs. Libellés et descriptions : ceux de la bibliothèque (anglais) ; valeurs par défaut : en français.

- media : groupe — Media
  - type : sous-contenu, library: image | video | audio — Type (Optional media to display above the question.)
  - disableImageZooming : booléen, défaut false, si type = H5P.Image — Disable image zooming
- taskDescription* : texte riche (Markdown: a code em h2 h3 hr li ol pre strong u ul) — Task description (Describe your task here.)
- sentences* : liste (min 1) — Sentences
  chaque élément :
    - description : texte — Description (You can optionally put a simple description above the text input field, useful e.g. for dialogues.)
    - sample* : audio (chemin ou URL) — Sound sample (Sentence spoken in normal speed)
    - sampleAlternative : audio (chemin ou URL) — Sound sample slow (Sentence spoken in slow speed)
    - text* : texte — Text (Text that should be written. You can add alternate spellings to a word by adding a vertical line (|) behind followed by an alternative.)
- overallFeedback : groupe — Overall Feedback (groupe à un champ: écrire directement la valeur)
  - overallFeedback : liste (min 1) — Define custom feedback for any score range (Click the "Add range" button to add as many ranges as you need. Example: 0-20% Bad score, 21-91% Average Score, 91-100% Great Score!)
    chaque élément :
      - from : nombre, min 0, max 100, défaut 0 — Score Range
      - to : nombre, min 0, max 100, défaut 100
      - feedback : texte — Feedback for defined score range
- behaviour : réglages — Behavioural settings (These options will let you control how the task behaves.)
  tries=…, triesAlternative=…, disablePause=false, playButtonDelay=…, shuffleSentences=never (never|once|onRetry), enableRetry=true, enableSolutionsButton=true, enableSolutionOnCheck=false

Textes d'interface pré-remplis en français (ne pas fournir sauf besoin) : l10n, a11y.

## Exemple complet (validé : validateur officiel H5P + affichage)

Fichier `tests/examples/dictee.md` (médias dans `tests/media/`).

````markdown
---
type: dictee
title: Dictée flash – les accords du participe passé
language: fr
preset: entrainement
license: CC BY-SA 4.0
authors: Équipe de lettres
---
Écoute chaque phrase puis **écris-la** dans la zone de saisie. Attention aux accords du participe passé !

- ![](../media/bip.wav) Les feuilles sont tombées dans la cour. :: participe passé employé avec « être »
- ![](../media/bip.wav) Les pommes que j'ai cueillies étaient mûres. :: participe passé employé avec « avoir »
- ![](../media/bip.wav) Fatiguées, les élèves se sont assises. :: participe passé employé comme adjectif

```yaml
overallFeedback:
  - {from: 0, to: 50, feedback: Revois la règle d'accord du participe passé.}
  - {from: 51, to: 99, feedback: "C'est bien, mais relis attentivement tes accords."}
  - {from: 100, to: 100, feedback: "Excellent, aucune faute !"}
behaviour:
  tries: 3
  shuffleSentences: once
```
````
