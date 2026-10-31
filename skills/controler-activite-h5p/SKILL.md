---
name: controler-activite-h5p
description: "Contrôle un paquet H5P construit avant tout dépôt : validateur officiel h5p-php-library (droits gestionnaire et enseignant, filtre d'affichage) et rendu dans Chromium avec captures, via tools/qa.py du harnais h5pharness. À utiliser sur chaque paquet avant de le déposer sur Moodle ou de le livrer."
---

# Contrôler une activité H5P construite

Prérequis : le paquet est construit (`OK` du skill `activite-h5p`) dans `<HARNAIS>/dist/`. Les commandes se lancent depuis `<HARNAIS>`.
Le projet est dans `<PROJET>`. Ce skill ne modifie ni la source, ni le paquet, ni Moodle : il constate.

## Commandes

~~~bash
cd <HARNAIS>
.venv/bin/python tools/qa.py dist/<cours>/                       # validateur officiel, droits gestionnaire et enseignant
.venv/bin/python tools/qa.py dist/<cours>/x.h5p --render --shots /tmp/captures   # + rendu Chromium et captures PNG
~~~

- Sans `--render` : le **validateur officiel** `h5p-php-library` (le code qu'embarque Moodle), en droits gestionnaire puis enseignant, et
  la vérification que le filtre d'affichage de Moodle ne modifie rien dans le contenu.
- Avec `--render` : chaque paquet est aussi joué dans Chromium (h5p-standalone) ; toute erreur JavaScript, fichier manquant ou
  affichage vide est signalé. `--shots <dossier>` écrit une capture PNG par paquet.
- Autres options : `--no-php` (sans PHP), `--json`, `-j <n>` (parallélisme). Mesure : avec `--render --json`, la variable
  `H5P_RENDER_PROBE='<sélecteur CSS>'` ajoute au résultat (`render.probe`) la position et la taille en pixels des éléments
  correspondants de l'activité jouée.
- Prérequis : `php` avec les extensions `zip` et `mbstring`, `git`, `unzip`, et pour `--render` `node` et `npm` ; au premier usage, le
  contrôle récupère `h5p-php-library`, `h5p-standalone` et `playwright` dans le cache `~/.cache/h5p-harness` (réseau nécessaire une
  fois ; dossier modifiable par `H5P_HARNESS_CACHE`). Chromium introuvable : `H5P_CHROMIUM=/chemin/chromium`.

## Procédure

1. Lancer `tools/qa.py dist/<cours>/ --render --shots <dossier temporaire>` sur les paquets à déposer.
2. Lire le résultat : une ligne `OK` par paquet conforme, `ÉCHEC <paquet>` suivi des problèmes (`admin:`, `teacher:`, `filtre H5P:`,
   `rendu:`) sinon, puis `n/n paquet(s) conformes`. Code de sortie 0 = tout est conforme, 1 = au moins un échec, 2 = PHP absent.
3. **Regarder** chaque capture : l'activité s'affiche, le texte est lisible, rien ne déborde. Les règles de présentation du projet
   (par exemple la hauteur de l'activité après « Vérifier », dans le cas juste et dans le pire cas) se mesurent sur le rendu : elles
   sont dans la spécification du projet, pas dans le harnais.
4. Un `ÉCHEC` de contenu se corrige dans la source (skill `activite-h5p`), puis on reconstruit et on recontrôle. Un échec de
   l'environnement (PHP, réseau, Chromium) ne se contourne pas en réécrivant le contenu : le signaler.

## Livrable accepté

`OK` à la construction et au validateur officiel, rendu sans erreur, aucun avertissement laissé sans explication. Transmettre à
l'utilisateur la liste des paquets contrôlés et les captures regardées ; ne rien déposer sans son accord (skill `depot-moodle-h5p`).
