Tri / association avec **mise en page automatique** : consigne facultative (affichée en haut), puis une section `## Zone` par zone de dépôt, suivie des éléments à y déposer (`- texte` ou `- ![description](image)`). Les éléments sont disposés en haut, les zones en colonnes dessous. Avec une image de fond (ligne `![…](image)` avant la première zone), donner la position de chaque zone en % : `## Noyau @ 45,30`. Réglage fin : bloc ```yaml (`question.task.elements` / `dropZones` : x/y en %, width/height en em ; `dropZones` d'un élément et `correctElements` d'une zone = indices à partir de 0 ; sans aucune position et sans image de fond : même mise en page automatique).

```markdown
Range chaque animal dans sa classe.

## Mammifères
- chat
- dauphin

## Oiseaux
- aigle
- ![Manchot](images/manchot.png)
```
