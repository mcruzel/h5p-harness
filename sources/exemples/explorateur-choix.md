---
type: explorateur-choix
title: Composer un repas équilibré
language: fr
---
```yaml
media:
  type: {library: image, file: media/paysage.jpg, alt: Illustration}
taskDescription: |
  Compose ton **déjeuner** en choisissant le nombre de portions de chaque aliment.
  Objectif : un apport d'énergie, de protéines et de fibres **dans les intervalles conseillés**.
decisions:
  - {label: Pâtes (portion de 100 g), id: pates, unit: portion(s), min: 0, max: 4}
  - {label: Poulet (portion de 100 g), id: poulet, unit: portion(s), min: 0, max: 3}
  - {label: Haricots verts (portion de 100 g), id: legumes, unit: portion(s), min: 0, max: 4}
  - {label: Fromage (portion de 30 g), id: fromage, unit: portion(s), min: 0, max: 3}
targets:
  - {label: Énergie, id: energie, unit: kcal, min: 600, max: 850}
  - {label: Protéines, id: proteines, unit: g, min: 20, max: 55}
  - {label: Fibres, id: fibres, unit: g, min: 8, max: 15}
# chaque portion d'aliment ajoute « weight » unités à chaque objectif
weights:
  - decisionId: pates
    targets:
      - {targetId: energie, weight: 150}
      - {targetId: proteines, weight: 5}
      - {targetId: fibres, weight: 2}
  - decisionId: poulet
    targets:
      - {targetId: energie, weight: 165}
      - {targetId: proteines, weight: 31}
      - {targetId: fibres, weight: 0}
  - decisionId: legumes
    targets:
      - {targetId: energie, weight: 30}
      - {targetId: proteines, weight: 2}
      - {targetId: fibres, weight: 3}
  - decisionId: fromage
    targets:
      - {targetId: energie, weight: 120}
      - {targetId: proteines, weight: 7}
      - {targetId: fibres, weight: 0}
behaviour:
  maxTotalDecisions: 8
  givesLiveFeedback: true
```
