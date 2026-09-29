# Interactive Book — `livre`

H5P.InteractiveBook 1.15 · alias : livre, livre-interactif, interactivebook, interactive-book · syntaxe Markdown simplifiée : oui

## Syntaxe Markdown

Texte facultatif avant le premier chapitre = page de couverture (une image `![…](…)` y devient l'illustration). Chaque chapitre commence par `# Titre du chapitre` et contient des blocs comme une colonne : Markdown, tableaux, images, sous-contenus `::: type` … `:::` (mêmes types acceptés que la colonne).

```markdown
Un livre pour réviser la cellule.
![Couverture](images/cellule.png)

# La cellule
La cellule est l'unité du vivant.

::: vf: vrai
Tous les êtres vivants sont faits de cellules.
:::

# Les organites
::: glisser-mots
Complète.

Le {{noyau}} contient l'ADN.
:::
```

## Champs (bloc ```yaml, noms H5P)

`*` = obligatoire ; les autres champs ont une valeur par défaut ou sont facultatifs.

- showCoverPage : booléen, défaut false — Activer la couverture du livre
- bookCover : groupe, conditionnel — Page de couverture
  - coverDescription : texte riche (Markdown: a code col colgroup del em figcaption figure h1 h2 h3 h4 h5 h6 hr li ol pre s strong sub sup table tbody td tfoot th thead tr u ul), défaut  — Description de la couverture
  - coverMedium : sous-contenu, library: image | video — Cover media
- chapters* : liste (min 1, max 50) — Pages
  chaque élément = sous-contenu, library: colonne — Page
- behaviour : réglages — Paramètres comportementaux
  baseColor=#1768c4, defaultTableOfContents=true, progressIndicators=true, progressAuto=true, displaySummary=true, enableRetry=true

Textes d'interface pré-remplis en français (ne pas fournir sauf besoin) : read, displayTOC, hideTOC, page, next, nextPage, previous, previousPage, chapterCompleted, partCompleted, incompleteChapter, navigateToTop, markAsFinished, fullscreen, exitFullscreen, bookProgressSubtext, interactionsProgressSubtext, submitReport, restartLabel, summaryHeader, allInteractions, unansweredInteractions, scoreText, leftOutOfTotalCompleted, noInteractions, score, summaryAndSubmit, noChapterInteractionBoldText, noChapterInteractionText, yourAnswersAreSubmittedForReview, bookProgress, interactionsProgress, totalScoreLabel, a11y.

## Exemple complet (validé : validateur officiel H5P + affichage)

Fichier `tests/examples/livre.md` (médias dans `tests/media/`).

```markdown
---
type: livre
title: Livre – Les paysages de France
language: fr
license: CC BY-SA 4.0
---
Un petit livre pour découvrir et réviser les **paysages** de France.
![Un paysage de campagne](../media/paysage.jpg)

# Les paysages ruraux
La campagne française présente des paysages variés : **openfield** (champs ouverts) dans les grandes plaines, **bocage** (champs entourés de haies) dans l'Ouest.

![Vue panoramique d'une vallée](../media/panorama.jpg)

::: vf: vrai
Le bocage est caractérisé par des champs entourés de haies.
:::

# Les paysages urbains
En ville, on distingue le **centre-ville** ancien, les **banlieues** et le **périurbain**.

::: glisser-mots
Place chaque mot au bon endroit.

Le {{centre-ville}} regroupe souvent les monuments anciens. Autour s'étendent les {{banlieues}}, puis les espaces {{périurbains}}.
Distracteurs: bocage
:::

# Je révise
::: qcm
Quel paysage trouve-t-on surtout dans les grandes plaines céréalières ?
- [x] L'openfield
- [ ] Le bocage
- [ ] La montagne
:::

::: choix-unique
## Comment appelle-t-on les communes situées autour d'une ville, sous son influence ?
- [x] Le périurbain
- [ ] Le centre-ville
- [ ] L'openfield

## Quel paysage est typique de l'ouest de la France ?
- [ ] L'openfield
- [x] Le bocage
:::
```
