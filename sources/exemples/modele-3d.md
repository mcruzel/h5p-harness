---
type: modele-3d
title: Le cristal de sel (halite)
language: fr
preset: decouverte
license: CC BY-SA 4.0
authors: Équipe de physique-chimie
---
```yaml
model:
  file: media/modele-3d-cristal.glb
  alt: Modèle 3D d'un cristal de sel gemme de forme cubique
annotations:
  annotations:
    # « surface » (champ caché, non documenté dans la fiche) : sans lui l'annotation n'est pas affichée.
    # Format model-viewer : n° de nœud, n° de primitive, 3 indices de sommets, 3 coordonnées barycentriques.
    - text: Face carrée du cristal
      surface: "0 0 16 17 18 0.4 0.3 0.3"
    - text: Arête entre deux faces
      surface: "0 0 8 9 10 0.1 0.45 0.45"
visuals:
  backgroundColor: "#f4f1e8"
```
