# Course Presentation — `presentation`

H5P.CoursePresentation 1.27 · alias : presentation, diaporama, coursepresentation, course-presentation · syntaxe Markdown simplifiée : oui

## Syntaxe Markdown

Une diapo par section `# Titre`. Contenu = blocs comme dans une colonne : texte Markdown, une ligne `![description](image ou vidéo)`, interactions `::: type` … `:::` (`::: qcm`, `::: vf: faux`, `::: trous`…). **Mise en page automatique** (diapo 16:9) : titre en haut ; texte à gauche et image à droite s'il y a les deux ; une ou deux interactions sous le texte (côte à côte), au-delà en boutons. Garder ≈ 8 lignes de texte par diapo (avertissement sinon). Positions fines : bloc ```yaml (`presentation.slides[n].elements`, x/y/width/height en % de la diapo).

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

`*` = obligatoire ; les autres champs ont une valeur par défaut ou sont facultatifs.

- presentation : groupe
  - slides : liste
    chaque élément :
      - elements : liste
        chaque élément :
          - action : sous-contenu, library: texte | lien | image | forme | video | audio | trous | choix-unique | qcm | vf | glisser-deposer | resume | glisser-mots | marquer-mots | cartes | texte-continu | zone-texte | tableau | video-interactive | twitter | enregistreur-audio | choix-images
          - solution : texte riche (Markdown: a code del em h2 h3 hr li ol pre s strong ul) — Commentaires
          - alwaysDisplayComments : booléen — Toujours afficher les commentaires
          - backgroundOpacity : nombre, min 0, max 100, défaut 0 — Opacité
          - displayAsButton : booléen, défaut false — Afficher sous forme de bouton
          - buttonLabel : texte — Étiquette de bouton facultative
          - buttonSize : choix small|big, défaut big — La taille de bouton
          - title : texte — Titre
          - goToSlideType : choix specified|next|previous, défaut specified — Aller vers
          - goToSlide : nombre, min 1 — Aller à la diapositive
          - invisible : booléen, défaut false — Invisible
      - keywords : liste
        chaque élément :
          - main : texte
          - subs : liste
            chaque élément = texte
      - slideBackgroundSelector : groupe
        - imageSlideBackground : image (chemin ou URL) — Image
        - fillSlideBackground : couleur #rrggbb — Sélectionnez une couleur
  - keywordListEnabled : booléen, défaut true — Liste des mots-clés
  - keywordListAlwaysShow : booléen, défaut false — Toujours l'afficher
  - keywordListAutoHide : booléen, défaut false — La cacher automatiquement
  - keywordListOpacity : nombre, min 0, max 100, défaut 100 — Opacité
  - globalBackgroundSelector : groupe
    - imageGlobalBackground : image (chemin ou URL) — Image d'arrière-plan
    - fillGlobalBackground : couleur #rrggbb — Sélectionnez une couleur
- override : réglages — Réglages généraux
  activeSurface=false, hideSummarySlide=false, showSolutionButton= (on|off), retryButton= (on|off), summarySlideSolutionButton=true, summarySlideRetryButton=true, enablePrintButton=false

Textes d'interface pré-remplis en français (ne pas fournir sauf besoin) : l10n.

## Exemple complet (validé : validateur officiel H5P + affichage)

Fichier `tests/examples/presentation.md` (médias dans `tests/media/`).

````markdown
---
type: presentation
title: Les formes géométriques – diaporama de révision
language: fr
preset: entrainement
---
```yaml
presentation:
  keywordListEnabled: true
  globalBackgroundSelector:
    fillGlobalBackground: "#f5f7fa"
  slides:
    - keywords:
        - main: Introduction
      slideBackgroundSelector:
        fillSlideBackground: "#ffffff"
      elements:
        - x: 5
          y: 5
          width: 55
          height: 85
          action:
            library: texte
            text: |
              ## Les figures planes

              Une **figure plane** est une forme dessinée sur une surface plate.
              Dans ce diaporama, tu vas revoir :

              - le **cercle** ;
              - le **carré** ;
              - le **triangle**.
        - x: 62
          y: 20
          width: 33
          height: 49
          action:
            library: image
            file: ../media/cercle-bleu.png
            alt: Un cercle bleu
    - keywords:
        - main: Le cercle
      slideBackgroundSelector:
        fillSlideBackground: "#eef6ff"
      elements:
        - x: 3
          y: 4
          width: 62
          height: 92
          action:
            library: qcm
            md: |
              Quelles affirmations sont vraies pour un **cercle** de rayon 3 cm ?
              - [x] Son diamètre mesure 6 cm.
              - [ ] Son diamètre mesure 1,5 cm.
                > Non : le diamètre est le double du rayon.
              - [x] Tous ses points sont à 3 cm du centre.
        - x: 72
          y: 28
          width: 22
          height: 43
          action:
            library: forme
            type: circle
            shape:
              fillColor: "#3b82f6"
              borderColor: "#1e3a8a"
              borderWidth: 2
    - keywords:
        - main: Le triangle
      slideBackgroundSelector:
        fillSlideBackground: "#fff8e6"
      elements:
        - x: 3
          y: 4
          width: 46
          height: 92
          action:
            library: vf
            md: |
              La somme des angles d'un triangle est égale à 180°.
              - [x] Vrai
                > Exact : c'est une propriété de tous les triangles.
              - [ ] Faux
        - x: 51
          y: 4
          width: 46
          height: 92
          action:
            library: trous
            md: |
              Complète.

              Un triangle qui a trois côtés de même longueur est {{équilatéral}}.
          solution: Un triangle **équilatéral** a aussi trois angles de 60°.
```
````
