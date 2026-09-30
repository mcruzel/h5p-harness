# Course Presentation — `presentation`

H5P.CoursePresentation 1.27 · alias : presentation, diaporama, coursepresentation, course-presentation · syntaxe Markdown simplifiée : oui

## Syntaxe Markdown

Une diapo par section `# Titre`. Contenu = blocs comme dans une colonne : texte Markdown, une ligne `![description](image ou vidéo)`, interactions `::: type` … `:::` (`::: qcm`, `::: vf: faux`, `::: trous`…). **Mise en page automatique** (diapo 16:9) : titre en haut ; texte à gauche et image à droite s'il y a les deux ; une ou deux interactions sous le texte (côte à côte), au-delà en boutons. Garder ≈ 8 lignes de texte par diapo (avertissement sinon). En bloc ```yaml (`presentation.slides[n].elements`) : x/y/width/height en % de la diapo, facultatifs — une diapo sans aucune position reçoit la même mise en page automatique.

```markdown
# La photosynthèse
Les plantes fabriquent leur matière à partir de lumière, d'eau et de CO<sub>2</sub>.
- lieu : les **chloroplastes**
- produits : glucose et dioxygène

![Feuille au soleil](images/feuille.jpg)

# Vérifie
::: qcm
Quel gaz est rejeté ?
- [x] Le dioxygène
- [ ] Le dioxyde de carbone
:::
```

## Champs (bloc ```yaml, noms H5P)

`*` = obligatoire ; les autres champs ont une valeur par défaut ou sont facultatifs. Libellés et descriptions : ceux de la bibliothèque (anglais) ; valeurs par défaut : en français.

- presentation : groupe
  - slides : liste
    chaque élément :
      - elements : liste
        chaque élément :
          - x, y, width, height : nombre, facultatif — position et taille en % de la diapo 16:9 ; aucun élément positionné sur une diapo = mise en page automatique (texte à gauche, image à droite, interactions dessous ou en boutons)
          - action : sous-contenu, library: texte | lien | image | forme | video | audio | trous | choix-unique | qcm | vf | glisser-deposer | resume | glisser-mots | marquer-mots | cartes | texte-continu | zone-texte | tableau | video-interactive | twitter | enregistreur-audio | choix-images
          - solution : texte riche (Markdown: a code del em h2 h3 hr li ol pre s strong ul) — Comments (The comments are shown when the user displays the suggested answers for all slides.)
          - alwaysDisplayComments : booléen — Always display comments
          - backgroundOpacity : nombre, min 0, max 100, défaut 0 — Background Opacity
          - displayAsButton : booléen, défaut false — Display as button
          - buttonLabel : texte — Optional button label
          - buttonSize : choix small|big, défaut big — Button size
          - title : texte — Title
          - goToSlideType : choix specified|next|previous, défaut specified — Go to
          - goToSlide : nombre, min 1 — Specific slide number (Only applicable when 'Specific slide number' is selected)
          - invisible : booléen, défaut false — Invisible (Default cursor, no title and no tab index. Warning: Users with disabilities or keyboard only users will have trouble using this element.)
      - keywords : liste
        chaque élément :
          - main : texte
          - subs : liste
            chaque élément = texte
      - slideBackgroundSelector : groupe
        - imageSlideBackground : image (chemin ou URL) — Image (Image background should have a 2:1 width to height ratio to avoid stretching. High resolution images will display better on larger screens.)
        - fillSlideBackground : couleur #rrggbb — Pick a color
  - keywordListEnabled : booléen, défaut true — Keyword list
  - keywordListAlwaysShow : booléen, défaut false — Always show
  - keywordListAutoHide : booléen, défaut false — Auto hide
  - keywordListOpacity : nombre, min 0, max 100, défaut 100 — Opacity
  - globalBackgroundSelector : groupe
    - imageGlobalBackground : image (chemin ou URL) — Image (Image background should have a 2:1 width to height ratio to avoid stretching. High resolution images will display better on larger screens.)
    - fillGlobalBackground : couleur #rrggbb — Pick a color
- override : réglages — Behaviour settings. (These options will let you override behaviour settings.)
  activeSurface=false, hideSummarySlide=false, showSolutionButton= (on|off), retryButton= (on|off), summarySlideSolutionButton=true, summarySlideRetryButton=true, enablePrintButton=false

Textes d'interface pré-remplis en français (ne pas fournir sauf besoin) : l10n.

## Exemple complet (validé : validateur officiel H5P + affichage)

Fichier `sources/exemples/presentation.md` (médias dans `sources/exemples/media/`).

```markdown
---
type: presentation
title: Les formes géométriques – diaporama de révision
language: fr
preset: entrainement
---
# Les figures planes
Une **figure plane** est une forme dessinée sur une surface plate. Dans ce diaporama, tu vas revoir :

- le **cercle** ;
- le **triangle**.

![Un cercle bleu](media/cercle-bleu.png)

# Le cercle
::: qcm
Quelles affirmations sont vraies pour un **cercle** de rayon 3 cm ?
- [x] Son diamètre mesure 6 cm.
- [ ] Son diamètre mesure 1,5 cm.
  > Non : le diamètre est le double du rayon.
- [x] Tous ses points sont à 3 cm du centre.
:::

# Le triangle
::: vf
La somme des angles d'un triangle est égale à 180°.
- [x] Vrai
  > Exact : c'est une propriété de tous les triangles.
- [ ] Faux
:::

::: trous
Complète.

Un triangle qui a trois côtés de même longueur est {{équilatéral}}.
:::
```

Même activité entièrement en YAML (positions explicites) : `tests/fixtures/presentation.yaml.md`.
