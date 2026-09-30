# Consignes pour les agents

- **Produire une activité H5P** : suivre `.claude/skills/h5p/SKILL.md` (écrire `sources/…/*.md`,
  lancer `python -m h5pharness build <fichier> --publish`, lire la sortie courte). Ne jamais écrire
  de JSON H5P à la main ni lire `vendor/`.
- **Exemples** : `sources/exemples/<type>.md` = un exemple validé par type (modèle à copier, affiché
  dans les fiches `specs/`, construit par les tests) ; ne pas y ranger d'autres activités.
- **Modifier le harnais** (`h5pharness/`) : lancer `python -m pytest` et `python -m ruff check .` ;
  contrôle complet d'un paquet : `python tools/qa.py dist/ --render` (validateur PHP officiel + rendu).
- **Mettre à jour les bibliothèques H5P** : `python tools/vendor_libraries.py` puis
  `python -m h5pharness specs`.
