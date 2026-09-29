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
