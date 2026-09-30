**Interactions seulement d'après le transcrit.** Questions et activités ne sont ajoutées que si la source déclare le transcrit horodaté de la vidéo (`.vtt` ou `.srt`) : `transcript: fichier.vtt` dans l'en-tête (ou une ligne `transcrit: fichier.vtt` sous la vidéo). Sans lui, le harnais refuse les interactions et, pour une vidéo seule, indique en « piste » comment l'obtenir : le demander à l'agent qui a confié la tâche ou à l'utilisateur (sous-titres de la plateforme vidéo, export d'un outil de transcription). `python -m h5pharness transcript fichier.vtt` l'affiche en lignes horodatées `m:ss texte` : placer chaque question après le passage qui y répond. Le harnais vérifie que chaque interaction tombe dans la durée du transcrit, signale une question sans mot commun avec ce qui vient d'être dit, et ajoute le transcrit comme sous-titres de la vidéo.

Une ligne `![titre](vidéo)` (fichier MP4/WebM, URL, ou lien YouTube/Vimeo), une courte description facultative, puis une section par moment de la vidéo : `## <temps> <type>` avec le temps en `m:ss` (ou secondes). Types : questions (`qcm`, `vf: faux`, `trous`, `glisser-mots`, `marquer-mots`, `choix-unique`, `resume`…) affichées en carte et mettant la vidéo en pause ; `texte` (bouton d'information, sans pause) ; `signet: Titre` (chapitre) ; `fin: Titre` (écran de fin). Une interaction reste affichée 10 s, ou jusqu'à l'apparition de la suivante. Positions et durées fines : bloc ```yaml (`interactiveVideo.assets.interactions[n]` : temps en secondes ou `m:ss`, x/y en % de la vidéo, width/height en em, facultatifs). Un bloc ```yaml peut aussi compléter le raccourci (ex. `summary`).

```markdown
![La photosynthèse](videos/photosynthese.mp4)
transcrit: videos/photosynthese.vtt
Regarde la vidéo et réponds aux questions.

## 0:00 signet: Introduction

## 0:45 texte
Observe la couleur des feuilles.

## 1:30 qcm
Quel gaz est rejeté ?
- [x] Le dioxygène
- [ ] Le dioxyde de carbone
```
