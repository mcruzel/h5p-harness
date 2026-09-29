# ChoiceExplorer — `explorateur-choix`

H5P.ChoiceExplorer 1.0 · alias : explorateur-choix, choiceexplorer, choice-explorer · syntaxe Markdown simplifiée : non (bloc ```yaml)

## Champs (bloc ```yaml, noms H5P)

`*` = obligatoire ; les autres champs ont une valeur par défaut ou sont facultatifs.

- media : groupe — Media
  - type : sous-contenu, library: image | video | audio — Type
  - disableImageZooming : booléen, défaut false, conditionnel — Disable image zooming
- taskDescription* : texte riche (Markdown: a code em h2 h3 hr li ol pre strong u ul) — Task description
- decisions* : liste (min 1) — Decision parameters
  chaque élément :
    - label* : texte — Label
    - id* : texte — Id
    - unit : texte — Unit
    - min : nombre, min 0 — Minimum value
    - max : nombre, min 0 — Maximum value
- targets* : liste (min 1, max 5) — Target parameters
  chaque élément :
    - label* : texte — Label
    - id* : texte — Id
    - unit : texte — Unit
    - min : nombre — Minimum value
    - max : nombre — Maximum value
- weights : liste — Weights
  chaque élément :
    - decisionId* : texte — Id
    - targets : liste — Targets
      chaque élément :
        - targetId* : texte — Id
        - weight* : nombre — Weight
- behaviour : réglages — Behavioural settings
  maxTotalDecisions=…, givesLiveFeedback=false

Textes d'interface pré-remplis en français (ne pas fournir sauf besoin) : l10n.
