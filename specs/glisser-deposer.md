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
    - background : image (chemin ou URL) — Image d'arrière-plan (Sélectionnez une image d'arrière-plan pour votre activité (facultatif).)
    - size : groupe — Taille de la zone de l'activité (Spécifiez la largeur et la hauteur (en pixels) de la zone de l'activité.)
      - width* : nombre
      - height* : nombre
  - task : groupe — Éléments de l'activité (Commencez par créer vos zones de dépôt. Ensuite, créez les étiquettes à glisser en cochant la/les zone(s) où …)
    - elements : liste — Eléments
      chaque élément :
        - type* : sous-contenu, library: texte | image (Sélectionnez le type de contenu que vous souhaitez ajouter.)
        - dropZones* : choix  (plusieurs) — Sélectionnez les zones de dépôt
        - backgroundOpacity : nombre, min 0, max 100, défaut 100 — Opacité (Reducing the opacity may result in an insufficient contrast and make the content not accessible.)
        - multiple : booléen, défaut false — Nombre illimité d'instances pour cet élément (Cloner cet élément de sorte qu'il puisse être déposé dans plusieurs zones.)
    - dropZones : liste — Zones de dépôt
      chaque élément :
        - label* : texte riche (Markdown: code del em s strong) — Etiquette (The label is used by assistive technologies.)
        - showLabel : booléen — Afficher l'étiquette
        - correctElements* : choix  (plusieurs) — Sélectionnez les éléments qui devront être correctement placés dans c…
        - backgroundOpacity : nombre, min 0, max 100, défaut 100 — Opacité (Reducing the opacity may result in an insufficient contrast and make the content not accessible.)
        - tipsAndFeedback : groupe — Aides et commentaires
          - tip : texte riche (Markdown: code em strong) — Indice
          - feedbackOnCorrect : texte — Message qui apparaît si l'association des éléments est correcte (Ce message apparaîtra au-dessous de "vérifier" si l'élément est placé correctement.)
          - feedbackOnIncorrect : texte — Message qui apparaît si l'association des éléments est incorrecte (Ce message apparaîtra au-dessous de "vérifier" si l'élément est placé incorrectement.)
        - single : booléen, défaut false — Cette zone de dépôt ne peut contenir qu'un seul élément (Assurez-vous qu'il n'existe qu'une seule bonne réponse pour cette zone)
        - autoAlign : booléen — Activer l'alignement automatique des éléments déplacés (Les éléments déposés dans cette zone seront automatiquement alignés si cette option est cochée.)
- overallFeedback : groupe — Feedback général (groupe à un champ: écrire directement la valeur)
  - overallFeedback : liste (min 1) — Définissez le feedback pour chaque intervalle de scores (Cliquez sur le bouton "Ajouter Intervalle" pour ajouter autant d'intervalles de score que vous le souhaitez. …)
    chaque élément :
      - from : nombre, min 0, max 100, défaut 0 — Intervalle des scores
      - to : nombre, min 0, max 100, défaut 100
      - feedback : texte — Feedback pour un intervalle de scores défini
- behaviour : groupe — Paramètres comportementaux (Ces options vous permettent de contrôler le déroulement de vos activités.)
  - enableRetry : booléen, défaut true — Activer le bouton "Recommencer"
  - singlePoint : booléen, défaut false — Donner un point pour la question dans sa globalité (Désactivez cette option pour donner un point pour chaque étiquette correctement placée.)
  - applyPenalties : booléen, défaut true — Appliquer des pénalités (Appliquez des pénalités pour les éléments déposés dans les mauvaises zones de dépôt. Cela doit être activé lo…)
  - enableScoreExplanation : booléen, défaut true, conditionnel — Activer les explications du score (Montrer l'explication du score aux utilisateurs en vérifiant leurs réponses (si l'option 'Appliquer les pénal…)
  - backgroundOpacity : texte — Opacité des étiquettes (Si vous remplissez ce champ, la valeur d'opacité choisie enlevera la valeur de l'opacité paramétrée avant pou…)
  - dropZoneHighlighting : choix dragging|always|never, défaut dragging — Mise en évidence de la zone de dépôt (Choisissez quand mettre en évidence la zone de dépôt.)
  - autoAlignSpacing : nombre, min 0, défaut 2 — Marge pour l'alignement automatique (en pixels)
  - enableFullScreen : booléen, défaut false — Activer le bouton Plein écran (Cochez cette option pour autoriser le mode Plein écran.)
  - showScorePoints : booléen, défaut true — Montrer les points de votre score (Afficher les points obtenus pour chaque réponse. Indisponible quand l'option 'Donner un point pour la questio…)
  - showTitle : booléen, défaut true — Afficher le titre (Décochez cette option si vous ne voulez pas que ce titre soit affiché. Le titre ne sera affiché que dans les …)
  - dragHandleVisibility : booléen, défaut true — Montrer les Poignées de Déplacement (nouveau look uniquement) (Change l'état de visibilité des poignées permettant de déplacer des éléments sur le canevas)

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
