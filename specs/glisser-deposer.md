# Drag and Drop — `glisser-deposer`

H5P.DragQuestion 1.15 · alias : glisser-deposer, dragquestion, drag-question · syntaxe Markdown simplifiée : oui

## Syntaxe Markdown

Tri / association avec **mise en page automatique** : consigne facultative (affichée en haut), puis une section `## Zone` par zone de dépôt, suivie des éléments à y déposer (`- texte` ou `- ![description](image)`). Les éléments sont disposés en haut, les zones en colonnes dessous. Avec une image de fond (ligne `![…](image)` avant la première zone), donner la position de chaque zone en % : `## Noyau @ 45,30`. Réglage fin : bloc ```yaml (`question.task.elements` / `dropZones`, x/y en %, largeur/hauteur en em).

```markdown
Range chaque animal dans sa classe.

## Mammifères
- chat
- dauphin

## Oiseaux
- aigle
- ![Manchot](images/manchot.png)
```

## Champs (bloc ```yaml, noms H5P)

`*` = obligatoire ; les autres champs ont une valeur par défaut ou sont facultatifs.

- question : groupe
  - settings : groupe — Réglages
    - background : image (chemin ou URL) — Image d'arrière-plan
    - size : groupe — Taille de la zone de l'activité
      - width* : nombre
      - height* : nombre
  - task : groupe — Éléments de l'activité
    - elements : liste — Eléments
      chaque élément :
        - type* : sous-contenu, library: texte | image
        - dropZones* : choix  (plusieurs) — Sélectionnez les zones de dépôt
        - backgroundOpacity : nombre, min 0, max 100, défaut 100 — Opacité
        - multiple : booléen, défaut false — Nombre illimité d'instances pour cet élément
    - dropZones : liste — Zones de dépôt
      chaque élément :
        - label* : texte riche (Markdown: code del em s strong) — Etiquette
        - showLabel : booléen — Afficher l'étiquette
        - correctElements* : choix  (plusieurs) — Sélectionnez les éléments qui devront être correctement placés dans c…
        - backgroundOpacity : nombre, min 0, max 100, défaut 100 — Opacité
        - tipsAndFeedback : groupe — Aides et commentaires
          - tip : texte riche (Markdown: code em strong) — Indice
          - feedbackOnCorrect : texte — Message qui apparaît si l'association des éléments est correcte
          - feedbackOnIncorrect : texte — Message qui apparaît si l'association des éléments est incorrecte
        - single : booléen, défaut false — Cette zone de dépôt ne peut contenir qu'un seul élément
        - autoAlign : booléen — Activer l'alignement automatique des éléments déplacés
- overallFeedback : groupe — Feedback général (groupe à un champ: écrire directement la valeur)
  - overallFeedback : liste (min 1) — Définissez le feedback pour chaque intervalle de scores
    chaque élément :
      - from : nombre, min 0, max 100, défaut 0 — Intervalle des scores
      - to : nombre, min 0, max 100, défaut 100
      - feedback : texte — Feedback pour un intervalle de scores défini
- behaviour : groupe — Paramètres comportementaux
  - enableRetry : booléen, défaut true — Activer le bouton "Recommencer"
  - singlePoint : booléen, défaut false — Donner un point pour la question dans sa globalité
  - applyPenalties : booléen, défaut true — Appliquer des pénalités
  - enableScoreExplanation : booléen, défaut true, conditionnel — Activer les explications du score
  - backgroundOpacity : texte — Opacité des étiquettes
  - dropZoneHighlighting : choix dragging|always|never, défaut dragging — Mise en évidence de la zone de dépôt
  - autoAlignSpacing : nombre, min 0, défaut 2 — Marge pour l'alignement automatique (en pixels)
  - enableFullScreen : booléen, défaut false — Activer le bouton Plein écran
  - showScorePoints : booléen, défaut true — Montrer les points de votre score
  - showTitle : booléen, défaut true — Afficher le titre
  - dragHandleVisibility : booléen, défaut true — Montrer les Poignées de Déplacement (nouveau look uniquement)

Textes d'interface pré-remplis en français (ne pas fournir sauf besoin) : scoreShow, submit, tryAgain, scoreExplanation, localize, grabbablePrefix, grabbableSuffix, dropzonePrefix, noDropzone, tipLabel, tipAvailable, correctAnswer, wrongAnswer, feedbackHeader, scoreBarLabel, scoreExplanationButtonLabel, a11yCheck, a11yRetry.

## Exemple complet (validé : validateur officiel H5P + affichage)

Fichier `tests/examples/glisser-deposer.md` (médias dans `tests/media/`).

````markdown
---
type: glisser-deposer
title: Polygone ou pas ? Classe les figures
language: fr
preset: entrainement
---
```yaml
# x, y en % de la zone ; width, height en em (1 em = 16 px pour une zone de 620 × 310)
question:
  settings:
    background: ../media/paysage.jpg
    size: {width: 620, height: 310}
  task:
    elements:
      - type: {library: image, file: ../media/carre-rouge.png, alt: Un carré rouge}
        dropZones: [0]
        x: 2
        y: 6
        width: 5
        height: 3.75
      - type: {library: image, file: ../media/triangle-vert.png, alt: Un triangle vert}
        dropZones: [0]
        x: 19
        y: 6
        width: 5
        height: 3.75
      - type: {library: image, file: ../media/cercle-bleu.png, alt: Un disque bleu}
        dropZones: [1]
        x: 2
        y: 36
        width: 5
        height: 3.75
      - type: {library: texte, text: un losange}
        dropZones: [0]
        x: 19
        y: 40
        width: 5.5
        height: 2
      - type: {library: texte, text: un ovale}
        dropZones: [1]
        x: 2
        y: 70
        width: 5.5
        height: 2
    dropZones:
      - label: Polygones
        showLabel: true
        correctElements: [0, 1, 3]
        autoAlign: true
        x: 40
        y: 12
        width: 11
        height: 16
        tipsAndFeedback:
          tip: Un polygone n'a que des côtés **droits**.
      - label: Non polygones
        showLabel: true
        correctElements: [2, 4]
        autoAlign: true
        x: 70
        y: 12
        width: 11
        height: 16
        tipsAndFeedback:
          feedbackOnIncorrect: Une figure avec un bord courbe n'est pas un polygone.
```
````
