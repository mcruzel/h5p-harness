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

`*` = obligatoire ; les autres champs ont une valeur par défaut ou sont facultatifs.

- media : groupe — Média
  - type : sous-contenu, library: image | video | audio — Type (Média à afficher au-dessus de la question (facultatif).)
  - disableImageZooming : booléen, défaut false, conditionnel — Désactiver le zoom sur image pour l'image de la question
- question* : texte riche (Markdown: code em h2 h3 pre strong sub sup) — Question
- answers* : liste (min 1) — Options disponibles
  chaque élément :
    - text* : texte riche (Markdown: code em strong sub sup) — Réponse
    - correct : booléen — Réponse correcte
    - tipsAndFeedback : groupe — Aide et retour
      - tip : texte riche (Markdown: a code em strong) — Indice (Indication pour l'utilisateur. Ce texte s'affiche avant que l'utilisateur ne valide la/les réponse(s).)
      - chosenFeedback : texte riche (Markdown: a code em strong sub sup) — Commentaire (si cette réponse a été sélectionnée) (Cette indication s'affiche sous la réponse quand l'utilisateur clique sur "Vérifier".)
      - notChosenFeedback : texte riche (Markdown: a code em strong sub sup) — Commentaire (si cette réponse n'a pas été sélectionnée) (Après vérification par l'utilisateur, s'affiche sous la réponse si celle-ci n'a pas été sélectionnée.)
- overallFeedback : groupe — Retour général (groupe à un champ: écrire directement la valeur)
  - overallFeedback : liste (min 1) — Définir un retour personnalisé pour chaque tranche de score (Cliquez sur le bouton "Ajouter Intervalle" pour ajouter autant d'intervalles de score que vous souhaitez. Exe…)
    chaque élément :
      - from : nombre, min 0, max 100, défaut 0 — Fourchette de score
      - to : nombre, min 0, max 100, défaut 100
      - feedback : texte — Retour pour cet intervalle de score
- behaviour : réglages — Paramètres comportementaux (Ces options vous permettent de gérer le comportement de l'activité.)
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
