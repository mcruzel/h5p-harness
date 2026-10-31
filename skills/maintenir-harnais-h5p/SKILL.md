---
name: maintenir-harnais-h5p
description: "Modifie ou met à jour le harnais h5pharness lui-même : tests et ruff, contrôle complet d'un paquet, mise à jour des bibliothèques H5P, régénération des fiches de types, exemples par type, pull request sans fusion. À utiliser quand il faut changer le code ou les bibliothèques du harnais, pas pour produire une activité."
---

# Maintenir le harnais H5P

Le harnais est dans `<HARNAIS>` ; toutes les commandes s'y lancent. Ce skill concerne le code (`h5pharness/`, `tools/`), les bibliothèques
(`vendor/`) et les fiches (`specs/`), pas la production d'une activité (skill `activite-h5p`). Les sources et livrables d'un projet
(`<PROJET>`) ne se modifient pas depuis ici.

## Après toute modification du code

~~~bash
cd <HARNAIS>
.venv/bin/python -m pytest -q          # suite complète
.venv/bin/python -m ruff check .       # lint (ligne de 120 caractères)
.venv/bin/python -m h5pharness build sources/exemples -o /tmp/exemples-h5p --offline -q     # les 63 exemples se construisent
.venv/bin/python tools/qa.py /tmp/exemples-h5p --render        # contrôle complet : validateur officiel + rendu
~~~

Une modification qui change la sortie d'un paquet est vérifiée sur les exemples : la construction est **reproductible à l'octet**
(même source, même paquet) ; une différence inattendue est un défaut.

## Bibliothèques et fiches

- Mettre à jour les bibliothèques : `python tools/vendor_libraries.py` (réseau ; construit ce qui doit l'être avec npm), puis
  `python -m h5pharness specs` (régénère `specs/`) et les contrôles ci-dessus. Les versions retenues sont dans `vendor/libraries.lock.json`.
- Régénérer seulement les fiches : `python -m h5pharness specs`.
- `sources/exemples/` contient **un exemple validé par type** (modèle à copier, affiché dans les fiches, utilisé par les tests) :
  n'y ranger aucune autre activité.
- Dépôt Moodle réel : les tests de `tests/test_moodle.py` ne tournent que si `H5P_MOODLE_TEST_COURSE` nomme un cours **jetable** (et
  `H5P_MOODLE_DIR` le dossier de Moodle). Jamais sur un cours de production.

## Livrer

Travailler sur une branche, pousser la branche, ouvrir une pull request vers `main` ; **ne jamais fusionner** : la fusion revient à
l'utilisateur. Ne pas modifier les workflows GitHub sans demande. Ne jamais versionner de paquet `.h5p` (`dist/` est ignoré : la
construction est reproductible) ni de fichier propre à la machine.
