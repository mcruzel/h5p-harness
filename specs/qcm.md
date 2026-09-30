# Multiple Choice — `qcm`

H5P.MultiChoice 1.16 · alias : qcm, choix-multiple, multichoice, multi-choice · syntaxe Markdown simplifiée : oui

## Syntaxe Markdown

Énoncé en Markdown, puis une ligne par réponse : `- [x]` bonne réponse, `- [ ]` distracteur (plusieurs `[x]` = cases à cocher). Sous une réponse, lignes indentées : `> retour si cochée`, `< retour si non cochée`, `? indice`. Une ligne `![description](image, vidéo YouTube ou audio)` avant les réponses ajoute un média.

```markdown
Quel organite est le siège de la **photosynthèse** ?
![Cellule végétale](images/cellule.png)
- [x] Le chloroplaste
- [ ] La mitochondrie
  > Non : elle assure la respiration cellulaire.
- [ ] Le noyau
  ? Pense à la couleur des feuilles.
```

## Champs (bloc ```yaml, noms H5P)

`*` = obligatoire ; les autres champs ont une valeur par défaut ou sont facultatifs. Libellés et descriptions : ceux de la bibliothèque (anglais) ; valeurs par défaut : en français.

- media : groupe — Media
  - type : sous-contenu, library: image | video | audio — Type (Optional media to display above the question.)
  - disableImageZooming : booléen, défaut false, si type = H5P.Image — Disable image zooming
- question* : texte riche (Markdown: code em h2 h3 pre strong sub sup) — Question
- answers* : liste (min 1) — Available options
  chaque élément :
    - text* : texte riche (Markdown: code em strong sub sup) — Text
    - correct : booléen — Correct
    - tipsAndFeedback : groupe — Tips and feedback
      - tip : texte riche (Markdown: a code em strong) — Tip text (Hint for the user. This will appear before user checks his answer/answers.)
      - chosenFeedback : texte riche (Markdown: a code em strong sub sup) — Message displayed if answer is selected (Message will appear below the answer on "check" if this answer is selected.)
      - notChosenFeedback : texte riche (Markdown: a code em strong sub sup) — Message displayed if answer is not selected (Message will appear below the answer on "check" if this answer is not selected.)
- overallFeedback : groupe — Overall Feedback (groupe à un champ: écrire directement la valeur)
  - overallFeedback : liste (min 1) — Define custom feedback for any score range (Click the "Add range" button to add as many ranges as you need. Example: 0-20% Bad score, 21-91% Average Score, 91-100% Great Score!)
    chaque élément :
      - from : nombre, min 0, max 100, défaut 0 — Score Range
      - to : nombre, min 0, max 100, défaut 100
      - feedback : texte — Feedback for defined score range
- behaviour : réglages — Behavioural settings (These options will let you control how the task behaves.)
  enableRetry=true, enableSolutionsButton=true, type=auto (auto|multi|single), singlePoint=false, randomAnswers=true, showSolutionsRequiresInput=true, confirmCheckDialog=false, confirmRetryDialog=false, autoCheck=false, passPercentage=100, showScorePoints=true

Textes d'interface pré-remplis en français (ne pas fournir sauf besoin) : UI, confirmCheck, confirmRetry.

## Exemple complet (validé : validateur officiel H5P + affichage)

Fichier `tests/examples/qcm.md` (médias dans `tests/media/`).

````markdown
---
type: qcm
title: Les volcans – QCM
language: fr
license: CC BY-SA 4.0
authors: Équipe SVT
---
Parmi ces affirmations sur les **volcans effusifs**, lesquelles sont exactes ?
![Schéma d'un volcan (illustration)](../media/triangle-vert.png)
- [x] Leur lave est **fluide** et pauvre en gaz.
  > Oui : c'est ce qui permet les longues coulées.
- [x] Ils forment souvent des coulées de lave.
- [ ] Ils produisent surtout des nuées ardentes.
  > Non : les nuées ardentes caractérisent les volcans *explosifs*.
  ? Pense au volcan de la Montagne Pelée (1902).
- [ ] Leur lave est très visqueuse.
  < Bien vu de ne pas l'avoir cochée : une lave visqueuse donne un volcanisme explosif.

```yaml
overallFeedback:
  - {from: 0, to: 49, feedback: "Relis le cours sur les deux types d'éruptions."}
  - {from: 50, to: 99, feedback: "Presque ! Vérifie les caractéristiques de la lave."}
  - {from: 100, to: 100, feedback: "Parfait !"}
behaviour:
  randomAnswers: true
```
````
