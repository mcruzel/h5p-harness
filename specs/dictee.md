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

`*` = obligatoire ; les autres champs ont une valeur par défaut ou sont facultatifs.

- media : groupe — Média
  - type : sous-contenu, library: image | video | audio — Type (Média à afficher au-dessus de la question (facultatif).)
  - disableImageZooming : booléen, défaut false, conditionnel — Désactiver le zoom sur les images
- taskDescription* : texte riche (Markdown: a code em h2 h3 hr li ol pre strong u ul) — Consigne (Décrivez votre tâche ici.)
- sentences* : liste (min 1) — Phrases
  chaque élément :
    - description : texte — Description (Vous pouvez éventuellement placer une simple description au-dessus du champ de saisie de texte, utile par exe…)
    - sample : audio (chemin ou URL) — Échantillon sonore (Phrase prononcée à vitesse normale)
    - sampleAlternative : audio (chemin ou URL) — Échantillon sonore lent (Phrase prononcée à vitesse lente)
    - text* : texte — Texte (Texte qui doit être écrit. Vous pouvez ajouter des orthographes alternatives à un mot en ajoutant une ligne v…)
- overallFeedback : groupe — Feedback général (groupe à un champ: écrire directement la valeur)
  - overallFeedback : liste (min 1) — Définissez le feedback pour chaque intervalle de score (Cliquez sur le bouton "Ajouter Intervalle" pour ajouter autant d'intervalles de score que vous souhaitez. Exe…)
    chaque élément :
      - from : nombre, min 0, max 100, défaut 0 — Intervalle de scores
      - to : nombre, min 0, max 100, défaut 100
      - feedback : texte — Feedback pour l'intervalle de score défini
- behaviour : réglages — Paramètres de comportement (Ces options vous permettent de contrôler le déroulement de vos activités.)
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
