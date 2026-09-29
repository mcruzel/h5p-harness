# Page — `colonne`

H5P.Column 1.22 · alias : colonne, column · syntaxe Markdown simplifiée : oui

## Syntaxe Markdown

Suite de blocs affichés les uns sous les autres : texte Markdown (devient un bloc texte), ligne `![description](image, vidéo ou audio)`, ou sous-contenu délimité par `::: type` … `:::` et écrit avec la syntaxe de ce type (`::: qcm`, `::: trous`, `::: vf: faux`, `::: mots-croises`…) ; `::: type yaml` pour écrire ses champs en YAML.

```markdown
## La photosynthèse
Les plantes fabriquent leur matière grâce à la lumière.

![Schéma](images/photosynthese.png)

::: qcm
Quel gaz est absorbé ?
- [x] Le dioxyde de carbone
- [ ] Le dioxygène
:::
```

## Champs (bloc ```yaml, noms H5P)

`*` = obligatoire ; les autres champs ont une valeur par défaut ou sont facultatifs.

- content* : liste (min 1) — Liste des contenus empilés
  chaque élément :
    - content* : sous-contenu, library: accordeon | agamotto | audio | enregistreur-audio | trous | graphique | collage | presentation | cartes | outil-documentation | glisser-deposer | glisser-mots | redaction | devinette | tableau | texte | iframe | image | image-interactive | trouver-zone | carrousel | video-interactive | lien | marquer-mots | memory | qcm | questionnaire | quiz | row | choix-unique | resume | frise | vf | video | choix-images — Contenu
    - useSeparator : choix auto|disabled|enabled, défaut auto — Séparer le contenu avec un délimiteur horizontal
