Suite de blocs affichés les uns sous les autres :
- texte Markdown (bloc texte : gras, italique, listes, titres `##`, liens) ;
- tableau Markdown (`| a | b |`) → bloc tableau automatiquement ;
- ligne `![description](image, vidéo ou audio)` ;
- sous-contenu délimité par `::: type` … `:::`, écrit avec la syntaxe Markdown de ce type (`::: qcm`, `::: vf: faux`, `::: trous`, `::: glisser-mots`…) ; `::: type yaml` … `:::` pour écrire ses champs en YAML.

Types acceptés dans une colonne (et donc dans un chapitre de livre) : voir `library:` dans les champs ci-dessous (pas de mots croisés ni de mots mêlés).

```markdown
## La photosynthèse
Les plantes fabriquent leur matière grâce à la **lumière**.

![Schéma](images/photosynthese.png)

| Entrées | Sorties |
|---|---|
| CO₂, eau | glucose, O₂ |

::: qcm
Quel gaz est absorbé ?
- [x] Le dioxyde de carbone
- [ ] Le dioxygène
:::
```
