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
