# Tabs — `onglets`

H5P.Tabs 1.3 · alias : onglets, tabs · syntaxe Markdown simplifiée : oui

## Syntaxe Markdown

Un onglet par section `## Titre`, avec un contenu comme une colonne : texte Markdown, images, sous-contenus `::: type` … `:::`.

## Champs (bloc ```yaml, noms H5P)

`*` = obligatoire ; les autres champs ont une valeur par défaut ou sont facultatifs. Libellés et descriptions : ceux de la bibliothèque (anglais) ; valeurs par défaut : en français.

- tabs* : liste (min 1, max 100) — Tabs
  chaque élément = sous-contenu, library: colonne — Content
- behaviour : réglages — Behavioural settings (These options will let you control how the task behaves.)
  tabPlacement=dynamic (dynamic|top|left), tabSpread=70
- a11y : groupe — Accessibility texts
  - tabList : texte, défaut Choisissez un onglet. — Choose a tab (Text for screenreaders.)

Textes d'interface pré-remplis en français (ne pas fournir sauf besoin) : l10n.

## Exemple complet (validé : validateur officiel H5P + affichage)

Fichier `sources/exemples/onglets.md` (médias dans `sources/exemples/media/`).

```markdown
---
type: onglets
title: Les trois états de l'eau
language: fr
preset: entrainement
---
## Solide
La **glace** a une forme propre : elle ne coule pas. L'eau devient solide en dessous de 0 °C.

![Un cube de glace (schéma)](media/carre-rouge.png)

## Liquide
L'eau **liquide** n'a pas de forme propre : elle prend la forme du récipient.

::: qcm
Quelle est la particularité de l'eau liquide ?
- [x] Elle prend la forme du récipient.
- [ ] Elle garde toujours la même forme.
- [ ] Elle est invisible.
:::

## Gazeux
La **vapeur d'eau** est un gaz invisible.

::: vf
La buée sur une vitre est de la vapeur d'eau.
- [ ] Vrai
  > Non : la buée est formée de fines gouttelettes d'eau liquide.
- [x] Faux
:::
```

Même activité entièrement en YAML (positions explicites) : `tests/fixtures/onglets.yaml.md`.
