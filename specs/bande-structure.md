# Structure Strip — `bande-structure`

H5P.StructureStrip 1.1 · alias : bande-structure, structurestrip, structure-strip · syntaxe Markdown simplifiée : non (bloc ```yaml)

## Champs (bloc ```yaml, noms H5P)

`*` = obligatoire ; les autres champs ont une valeur par défaut ou sont facultatifs.

- media : groupe — Média
  - type : sous-contenu, library: image | video | audio — Type
  - disableImageZooming : booléen, défaut false, conditionnel — Bloquer le zoom d’image
- taskDescription : texte riche (Markdown: a em h2 h3 hr li ol strong u ul) — Description de la tâche
- sections* : liste (min 1) — Sections
  chaque élément :
    - title* : texte — Titre
    - description : texte riche (Markdown: a em h2 h3 hr li ol strong u ul) — Indices
    - weight : nombre, min 1, défaut 1 — Poids
    - colorBackground : couleur #rrggbb, défaut #96ceb4 — Couleur de fond
    - colorText : couleur #rrggbb, défaut #1c1c1c — Couleur du texte
- behaviour : réglages — Paramètres comportementaux
  enableRetry=true, slack=10, textLengthMin=…, textLengthMax=…, feedbackMode=onRequest (onRequest|whileTyping)

Textes d'interface pré-remplis en français (ne pas fournir sauf besoin) : l10n, a11y.
