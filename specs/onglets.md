# Tabs — `onglets`

H5P.Tabs 1.3 · alias : onglets, tabs · syntaxe Markdown simplifiée : oui

## Syntaxe Markdown

Un onglet par section `## Titre`, avec un contenu comme une colonne : texte Markdown, images, sous-contenus `::: type` … `:::`.

## Champs (bloc ```yaml, noms H5P)

`*` = obligatoire ; les autres champs ont une valeur par défaut ou sont facultatifs.

- tabs* : liste (min 1, max 100) — Tabs
  chaque élément = sous-contenu, library: colonne — Content
- behaviour : réglages — Behavioural settings
  tabPlacement=dynamic (dynamic|top|left), tabSpread=70
- a11y : groupe — Accessibility texts
  - tabList : texte, défaut Choisissez un onglet. — Choose a tab

Textes d'interface pré-remplis en français (ne pas fournir sauf besoin) : l10n.
