Tri / association avec **mise en page automatique** : consigne facultative (affichée en haut), puis une section `## Zone` par zone de dépôt, suivie des éléments à y déposer (`- texte` ou `- ![description](image)`). Les éléments sont disposés en haut, les zones en colonnes dessous. Avec une image de fond (ligne `![…](image)` avant la première zone), donner la position de chaque zone en % : `## Noyau @ 45,30`. Réglage fin : bloc ```yaml (`question.task.elements` / `dropZones`, x/y en %, largeur/hauteur en em).

```markdown
Range chaque animal dans sa classe.

## Mammifères
- chat
- dauphin

## Oiseaux
- aigle
- ![Manchot](images/manchot.png)
```
