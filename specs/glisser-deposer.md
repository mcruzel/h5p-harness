# Drag and Drop — `glisser-deposer`

H5P.DragQuestion 1.15 · alias : glisser-deposer, dragquestion, drag-question · syntaxe Markdown simplifiée : oui

## Syntaxe Markdown

Tri / association avec **mise en page automatique** : consigne facultative (affichée en haut), puis une section `## Zone` par zone de dépôt, suivie des éléments à y déposer (`- texte` ou `- ![description](image)`). Les éléments sont disposés en haut, les zones en colonnes dessous. Avec une image de fond (ligne `![…](image)` avant la première zone), donner la position de chaque zone en % : `## Noyau @ 45,30`. Réglage fin : bloc ```yaml (`question.task.elements` / `dropZones` : x/y en %, width/height en em ; `dropZones` d'un élément et `correctElements` d'une zone = indices à partir de 0 ; sans aucune position et sans image de fond : même mise en page automatique).

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

`*` = obligatoire ; les autres champs ont une valeur par défaut ou sont facultatifs. Libellés et descriptions : ceux de la bibliothèque (anglais) ; valeurs par défaut : en français.

- question : groupe
  - settings : groupe — Settings
    - background : image (chemin ou URL) — Background image (Optional. Select an image to use as background for your drag and drop task.)
    - size : groupe — Task size (Specify how large (in px) the play area should be.)
      - width* : nombre
      - height* : nombre
  - task : groupe — Task (Start by placing your drop zones. Next, place your droppable elements and check off the appropriate drop zones. Last, edit your drop zone again and check off the correct answers.)
    - elements : liste — Elements
      chaque élément :
        - type* : sous-contenu, library: texte | image (Choose the type of content you would like to add.)
        - x, y, height, width : nombre, facultatif — x, y en % de la zone de jeu ; width, height en em (1 em = 16 px) ; sans positions nulle part : mise en page automatique (sans image de fond)
        - dropZones* : choix  (plusieurs) — Select drop zones — **indices des zones, à partir de 0**
        - backgroundOpacity : nombre, min 0, max 100, défaut 100 — Background Opacity (Reducing the opacity may result in an insufficient contrast and make the content not accessible.)
        - multiple : booléen, défaut false — Infinite number of element instances (Clones this element so that it can be dragged to multiple drop zones.)
    - dropZones : liste — Drop Zones — **indices des zones, à partir de 0**
      chaque élément :
        - label* : texte riche (Markdown: code del em s strong) — Label (The label is used by assistive technologies.)
        - showLabel : booléen — Show label
        - x, y, height, width : nombre, facultatif — x, y en % de la zone de jeu ; width, height en em (1 em = 16 px) ; sans positions nulle part : mise en page automatique (sans image de fond)
        - correctElements* : choix  (plusieurs) — Select correct elements — **indices des éléments, à partir de 0 (dans l'ordre de `elements`)**
        - backgroundOpacity : nombre, min 0, max 100, défaut 100 — Background Opacity (Reducing the opacity may result in an insufficient contrast and make the content not accessible.)
        - tipsAndFeedback : groupe — Tips and feedback
          - tip : texte riche (Markdown: code em strong) — Tip text
          - feedbackOnCorrect : texte — Message displayed on correct match (Message will appear below the task on "check" if correct droppable is matched.)
          - feedbackOnIncorrect : texte — Message displayed on incorrect match (Message will appear below the task on "check" if the match is incorrect.)
        - single : booléen, défaut false — This drop zone can only contain one element (Make sure there is only one correct answer for this dropzone)
        - autoAlign : booléen — Enable Auto-Align (Will auto-align all draggables dropped in this zone.)
- overallFeedback : groupe — Overall Feedback (groupe à un champ: écrire directement la valeur)
  - overallFeedback : liste (min 1) — Define custom feedback for any score range (Click the "Add range" button to add as many ranges as you need. Example: 0-20% Bad score, 21-91% Average Score, 91-100% Great Score!)
    chaque élément :
      - from : nombre, min 0, max 100, défaut 0 — Score Range
      - to : nombre, min 0, max 100, défaut 100
      - feedback : texte — Feedback for defined score range
- behaviour : groupe — Behavioural settings (These options will let you control how the task behaves.)
  - enableRetry : booléen, défaut true — Enable "Retry"
  - singlePoint : booléen, défaut false — Give one point for the whole task (Disable to give one point for each draggable that is placed correctly.)
  - applyPenalties : booléen, défaut true — Apply penalties (Apply penalties for elements dropped in the wrong drop zones. This must be enabled when the same element(s) are able to be dropped into multiple drop zones, or if there is only one drop-zone. If this is not enabled, lea…)
  - enableScoreExplanation : booléen, défaut true, si singlePoint = False — Enable score explanation (Display a score explanation to user when checking their answers (if the 'Apply penalties' option has been selected).)
  - backgroundOpacity : texte — Background opacity for draggables (If this field is set, it will override opacity set on all draggable elements. This should be a number between 0 and 100, where 0 means full transparency and 100 means no transparency)
  - dropZoneHighlighting : choix dragging|always|never, défaut dragging — Drop Zone Highlighting (Choose when to highlight drop zones.)
  - autoAlignSpacing : nombre, min 0, défaut 2 — Spacing for Auto-Align (in px)
  - enableFullScreen : booléen, défaut false — Enable FullScreen (Check this option to enable the full screen button.)
  - showScorePoints : booléen, défaut true — Show score points (Show points earned for each answer. Not available when the 'Give one point for the whole task' option is enabled.)
  - showTitle : booléen, défaut true — Show Title (Uncheck this option if you do not want this title to be displayed. The title will only be displayed in summaries, statistics etc.)
  - dragHandleVisibility : booléen, défaut true — Show drag handles (new look and feel only) (Toggles the visibility of drag handles used to move elements on the canvas.)

Textes d'interface pré-remplis en français (ne pas fournir sauf besoin) : scoreShow, submit, tryAgain, scoreExplanation, localize, grabbablePrefix, grabbableSuffix, dropzonePrefix, noDropzone, tipLabel, tipAvailable, correctAnswer, wrongAnswer, feedbackHeader, scoreBarLabel, scoreExplanationButtonLabel, a11yCheck, a11yRetry.

## Exemple complet (validé : validateur officiel H5P + affichage)

Fichier `sources/exemples/glisser-deposer.md` (médias dans `sources/exemples/media/`).

```markdown
---
type: glisser-deposer
title: Polygone ou pas ? Classe les figures
language: fr
preset: entrainement
---
Classe chaque figure : un polygone n'a que des côtés **droits**.

## Polygones
- ![Un carré rouge](media/carre-rouge.png)
- ![Un triangle vert](media/triangle-vert.png)
- un losange

## Non polygones
- ![Un disque bleu](media/cercle-bleu.png)
- un ovale
```

Même activité entièrement en YAML (positions explicites) : `tests/fixtures/glisser-deposer.yaml.md`.
