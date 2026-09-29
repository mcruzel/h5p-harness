Une ligne `![titre](vidéo)` (fichier MP4/WebM, URL, ou lien YouTube/Vimeo), une courte description facultative, puis une section par moment de la vidéo : `## <temps> <type>` avec le temps en `m:ss` (ou secondes). Types : questions (`qcm`, `vf: faux`, `trous`, `glisser-mots`, `marquer-mots`, `choix-unique`, `resume`…) affichées en carte et mettant la vidéo en pause ; `texte` (bouton d'information, sans pause) ; `signet: Titre` (chapitre) ; `fin: Titre` (écran de fin). Positions et durées fines : bloc ```yaml (`interactiveVideo.assets.interactions[n]`).

```markdown
![La photosynthèse](videos/photosynthese.mp4)
Regarde la vidéo et réponds aux questions.

## 0:00 signet: Introduction

## 0:45 texte
Observe la couleur des feuilles.

## 1:30 qcm
Quel gaz est rejeté ?
- [x] Le dioxygène
- [ ] Le dioxyde de carbone
```
