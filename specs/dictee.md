# Dictation — `dictee`

H5P.Dictation 1.4 · alias : dictee, dictation · syntaxe Markdown simplifiée : non (bloc ```yaml)

## Champs (bloc ```yaml, noms H5P)

`*` = obligatoire ; les autres champs ont une valeur par défaut ou sont facultatifs.

- media : groupe — Média
  - type : sous-contenu, library: image | video | audio — Type
  - disableImageZooming : booléen, défaut false, conditionnel — Désactiver le zoom sur les images
- taskDescription* : texte riche (Markdown: a code em h2 h3 hr li ol pre strong u ul) — Consigne
- sentences* : liste (min 1) — Phrases
  chaque élément :
    - description : texte — Description
    - sample : audio (chemin ou URL) — Échantillon sonore
    - sampleAlternative : audio (chemin ou URL) — Échantillon sonore lent
    - text* : texte — Texte
- overallFeedback : groupe — Feedback général (groupe à un champ: écrire directement la valeur)
  - overallFeedback : liste (min 1) — Définissez le feedback pour chaque intervalle de score
    chaque élément :
      - from : nombre, min 0, max 100, défaut 0 — Intervalle de scores
      - to : nombre, min 0, max 100, défaut 100
      - feedback : texte — Feedback pour l'intervalle de score défini
- behaviour : réglages — Paramètres de comportement
  tries=…, triesAlternative=…, disablePause=false, playButtonDelay=…, shuffleSentences=never (never|once|onRetry), enableRetry=true, enableSolutionsButton=true, enableSolutionOnCheck=false

Textes d'interface pré-remplis en français (ne pas fournir sauf besoin) : l10n, a11y.
