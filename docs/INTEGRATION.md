# Intégrer le harnais H5P dans un nouvel environnement

Ce guide recrée, sur une autre machine ou pour un autre projet, tout ce qu'il faut pour produire des activités H5P pour Moodle avec
le harnais : installation, variables d'environnement, skills des agents. Les quatre skills portables (produire une activité, la
contrôler, la déposer sur Moodle, maintenir le harnais) sont dans `skills/` ; la commande `skills --exporter` les écrit avec les
chemins réels. Le fonctionnement du harnais lui-même (format des sources, types, garanties) est dans le `README.md` et `specs/`.

## 1. Installation

| composant | rôle | obligatoire |
|---|---|---|
| Python 3.10 ou plus | le harnais (`python -m h5pharness`) ; essayé en 3.12 (CI) et 3.14 | oui |
| `pip install -r requirements.txt` (dans un venv conseillé) | PyYAML, markdown-it-py, Pillow ; `requirements-dev.txt` ajoute pytest et ruff | oui |
| git | `--publish` (commit et push des sources), clone de `h5p-php-library` par le contrôle officiel | oui pour `--publish` et `tools/qa.py` |
| accès réseau | téléchargement des médias par URL (une fois, dans `sources/.media/`, puis hors ligne) ; premier usage de `tools/qa.py` | selon les sources |
| PHP CLI avec `zip` et `mbstring` | validateur officiel (`tools/qa.py`) et dépôt direct dans Moodle (`--moodle`) | facultatif (recommandé) |
| node, npm, `unzip` | rendu des paquets dans Chromium et mesure de la hauteur des glisser-déposer (`tools/qa.py --render`) ; `h5p-standalone` et `playwright` sont installés dans `~/.cache/h5p-harness` au premier usage | facultatif |
| Chromium (via playwright, ou `H5P_CHROMIUM`) | idem | facultatif |
| `cairosvg` (pip) | conversion automatique des images SVG (Moodle refuse le SVG dans H5P) | facultatif |
| un Moodle 4.5 ou plus sur la même machine | dépôt direct `--moodle` (API H5P 1.28, `h5plib_v128`) | facultatif |

Les bibliothèques H5P (`vendor/libraries`, 175 bibliothèques, 56 Mo) sont versionnées avec le harnais : un `git clone` suffit, rien
à télécharger pour construire un paquet.

~~~bash
git clone <dépôt du harnais> <HARNAIS> && cd <HARNAIS>
python3 -m venv .venv && .venv/bin/pip install -r requirements.txt -r requirements-dev.txt
.venv/bin/python -m h5pharness types | head                                   # le harnais répond (63 types)
.venv/bin/python -m h5pharness build sources/exemples/qcm.md -o /tmp/essai    # OK /tmp/essai/…/qcm.h5p
.venv/bin/python -m pytest -q && .venv/bin/python -m ruff check .             # tests et lint
~~~

**Rendu : où sont `playwright` et `h5p-standalone`.** `tools/qa.py --render` les installe lui-même au premier usage dans
`$H5P_HARNESS_CACHE/render/node_modules` (`~/.cache/h5p-harness/render` par défaut : `npm i h5p-standalone@3.8.2`, plus `playwright` s'il n'est
pas déjà global) et pose `H5P_RENDER_MODULES` vers ce dossier : rien à faire. Pour lancer `tools/render.mjs` seul avec un dossier d'outils node
existant (le même que celui des autres chaînes), poser `H5P_RENDER_MODULES=<dossier>/node_modules` ; ce dossier contient
`npm install playwright@^1.63 h5p-standalone@^3.8.2` (1.63.0 et 3.8.2 sur l'installation d'origine) et le Chromium de playwright
(`npx playwright install chromium`), ou on pose `H5P_CHROMIUM`. Sur l'installation d'origine, ce dossier s'appelle `h5p-render` : sa
recréation complète (dossier, versions, navigateur, variables qui y pointent, scripts de capture sans équivalent dans ce dépôt ; la mesure de hauteur d'un glisser-déposer a le sien, voir ci-dessous)
est décrite une fois pour les trois chaînes dans le dépôt `course-composer`, `docs/harnais.md`, section « `h5p-render` : le dossier
d'outils node ».

**Mesure de la hauteur des glisser-déposer.** Un glisser-déposer s'allonge après « Vérifier » (retours par zone, tableau de retours, score) :
la mesure de cet allongement est celle qu'un projet exige avant de déposer l'activité (voir § 5). `tools/qa.py <paquet> --render` la fait seul pour
chaque paquet dont la bibliothèque principale est `H5P.DragQuestion` (pas pour un glisser-déposer rangé dans un quiz ou une présentation). Il joue
l'activité dans Chromium à deux largeurs, 400 px (écran étroit) et 760 px (colonne de contenu d'une page de cours) ; `--largeurs 400,760,1000` les
change. À chaque largeur il mesure la hauteur de l'iframe, dépose les étiquettes selon un plan déduit des bonnes réponses du `content.json`,
clique « Vérifier » et mesure de nouveau, dans deux cas : `juste` (chaque étiquette dans sa zone) et `tout faux` (chaque étiquette dans une zone
fausse : le cas où les retours sont les plus longs, donc le pire cas). Sortie, hauteurs en pixels, entre parenthèses l'écart avec la hauteur initiale :

~~~
OK    dist/passeport-ia/3.2-planche-cinq-taches.h5p  « Eléments déplaçables 1 de 5. Lister les candidatures reçues sur un fic »
      hauteur 400 px : avant 381 · juste 1718 (+1337) · tout faux 1775 (+1394)
      hauteur 760 px : avant 653 · juste 1634 (+981) · tout faux 1711 (+1058)
~~~

- **Aucun seuil par défaut** : le harnais mesure, la règle de présentation est celle du projet. `--hauteur-max PX` fait échouer l'activité dont une hauteur
  après « Vérifier » dépasse `PX` (code de sortie 1) ; `--no-mesure` supprime la mesure (le rendu seul est plus rapide : compter une trentaine de secondes par
  glisser-déposer pour deux largeurs et deux plans).
- `--shots <dossier>` ajoute les captures prises après « Vérifier » (`<paquet>-verifie-<largeur>-<plan>.png`) ; `--json` rend le détail dans
  `mesure.runs` (largeur, plan, étiquettes déposées sur attendues, hauteurs de l'iframe et du document avant et après).
- Une mesure qui ne peut pas être menée honnêtement est un échec, pas un chiffre : pas de bouton « Vérifier », étiquette qui ne se laisse pas déposer
  (« 2 étiquette(s) déposée(s) sur 3, mesure incomplète »), erreur du navigateur.
- Même résolution de `playwright` et de `h5p-standalone` que `tools/render.mjs` (`H5P_RENDER_MODULES`, `H5P_CHROMIUM`), aucune dépendance de plus.
  Pour lancer le script seul : `node tools/measure_dnd.mjs <paquet>.h5p '{"widths":[760],"plans":{"juste":[[0,0],[1,1]]}}'` (couples
  `[rang de l'étiquette dans la page, rang de la zone]`, à partir de 0 ; plan et sortie : `tools/dnd_measure.py`).

## 2. Configuration : variables d'environnement

Le harnais n'a **pas de fichier de configuration** : tout réglage propre à la machine passe par l'environnement du processus qui
lance la commande (profil du shell, service, environnement de l'agent, ou préfixe de la commande :
`H5P_MOODLE_DIR=/var/www/html/moodle H5P_MOODLE_RUNAS=www-data .venv/bin/python -m h5pharness build … --moodle <cours>`). Rien n'est à
versionner ; le dépôt ne contient aucun chemin de machine. Dans la colonne « propre à la machine », tout ce qui doit être refait sur
une autre installation.

| variable | lue par | rôle | défaut | propre à la machine |
|---|---|---|---|---|
| `H5P_MOODLE_DIR` | `--moodle` | dossier de Moodle (celui qui contient `config.php`) ; équivalent : `--moodle-dir` | emplacements usuels (`/var/www/moodle`, `/var/www/html/moodle`, `/var/www/html`, `/srv/moodle`, `/opt/moodle`, `/usr/share/moodle`, `~/moodle`) | oui |
| `H5P_MOODLE_RUNAS` | `--moodle` | compte système propriétaire de moodledata (`www-data`…) : le script PHP s'exécute sous ce compte, via `sudo -n -u` (ou `runuser` si root) ; il faut donc un `sudo` sans mot de passe pour la seule commande PHP du harnais | aucun : PHP s'exécute sous le compte courant | oui |
| `H5P_MOODLE_USER` | `--moodle` | compte Moodle au nom duquel le dépôt est fait ; seul l'administrateur peut installer les bibliothèques H5P du paquet | administrateur principal | oui |
| `H5P_MOODLE_PHP` | `--moodle` | binaire PHP utilisé pour le dépôt | `php` | oui si PHP n'est pas dans le `PATH` |
| `H5P_MOODLE_BANQUE` | `--moodle` | `1` : range aussi chaque contenu dans la banque de contenus du cours (comme `--banque`) | non | non (choix du projet) |
| `H5P_MOODLE_OWNER` | `--moodle` | compte enseignant auquel les contenus de banque sont attribués (il peut alors les modifier) ; le fichier reste au nom du compte de dépôt | aucun | oui |
| `H5P_COMMIT_TRAILERS` | `--publish` | lignes ajoutées au message des commits (ex. `Co-Authored-By: …`) | aucune | non |
| `H5P_HARNESS_CACHE` | `tools/qa.py`, `tools/vendor_libraries.py` | dossier de cache : `h5p-php-library`, `h5p-standalone`, `playwright`, sources des bibliothèques | `~/.cache/h5p-harness` | oui |
| `H5P_LIBRARIES` | `tools/qa.py` | dossier des bibliothèques que le validateur officiel utilise | `<HARNAIS>/vendor/libraries` | non |
| `H5P_CHROMIUM` | `tools/qa.py --render` | exécutable Chromium (si celui de playwright ne convient pas) | celui de playwright | oui |
| `H5P_RENDER_MODULES` | `tools/render.mjs` | dossier `node_modules` contenant playwright et h5p-standalone ; **posé par `tools/qa.py`**, à ne régler à la main que pour lancer `render.mjs` seul | `~/.cache/h5p-harness/render/node_modules` | oui |
| `H5P_RENDER_PROBE` | `tools/render.mjs` (via `tools/qa.py --render --json`) | sélecteur CSS : le rendu renvoie les boîtes (position, largeur, hauteur en pixels) des éléments correspondants, dans le champ `render.probe` du JSON ; sert à mesurer la hauteur d'une activité | absent | non |
| `H5P_MOODLE_TEST_COURSE` | `tests/test_moodle.py` | cours **jetable** d'un Moodle de test : active les tests de dépôt réel (avec `H5P_MOODLE_DIR`) | absent : tests ignorés | oui |

Hors de la machine : la variable de dépôt GitHub `H5P_RELEASES=off` désactive le workflow qui attache les paquets à la release de la
branche (`.github/workflows/h5p.yml`) ; `GITHUB_REPOSITORY`, `GITHUB_REF_NAME` et `GITHUB_SHA` ne servent qu'à ce workflow.

**Réglages par source** (pas par machine) : le bloc `moodle:` de l'en-tête d'une source (`course`, `section`, `as`, `page`, `hidden`,
`banque`) donne la destination par défaut ; les options de la ligne de commande la complètent ou la remplacent.

## 3. Les skills nécessaires

| skill | rôle | où le trouver |
|---|---|---|
| `activite-h5p` | **produire une activité** : choisir le type, écrire la source Markdown (médias, transcrit d'une vidéo interactive), `check`, `build`, lire la sortie (codes 0 à 3) ; sources du harnais ou du projet (copie de travail) | `skills/activite-h5p/SKILL.md` (version d'origine, pour Claude Code : `.claude/skills/h5p/SKILL.md`) |
| `controler-activite-h5p` | **contrôler un paquet** avant dépôt : validateur officiel `h5p-php-library` (droits gestionnaire et enseignant, filtre d'affichage), rendu Chromium, captures à regarder | `skills/controler-activite-h5p/SKILL.md` |
| `depot-moodle-h5p` | **déposer sur Moodle** un paquet contrôlé (activité, page, banque de contenus ; création ou mise à jour sans doublon), après accord explicite | `skills/depot-moodle-h5p/SKILL.md` |
| `maintenir-harnais-h5p` | **modifier le harnais** : tests, ruff, contrôle complet des 63 exemples, mise à jour des bibliothèques, fiches, pull request sans fusion | `skills/maintenir-harnais-h5p/SKILL.md` |

Les fichiers de `skills/` écrivent leurs chemins avec `<HARNAIS>` (dossier du harnais) et `<PROJET>` (dossier du projet : sources,
spécification de ses exercices) et ne citent aucune machine. Pour les recréer d'un coup dans un nouvel environnement :

~~~bash
cd <HARNAIS>
.venv/bin/python -m h5pharness skills --exporter <dossier de skills de l'agent> --projet <PROJET>
~~~

La commande écrit `<dossier>/<skill>/SKILL.md` avec les chemins réels de cette installation (sans `--exporter`, elle liste les skills).
Dossier de skills selon l'agent : Claude Code `<projet>/.claude/skills/` (ou `~/.claude/skills/`) ; OpenClaw le dossier de skills de
l'agent ou de son espace de travail (ou un dossier déclaré dans sa configuration de chargement des skills) ; tout autre agent :
l'endroit où il lit ses skills (`name` et `description` du frontmatter suffisent). Un agent qui ne lit pas les skills peut recevoir le
contenu du fichier comme consigne. Le skill d'origine `.claude/skills/h5p/SKILL.md` (écrit pour travailler dans le dépôt du harnais)
reste en place ; `activite-h5p` en est la version portable, qui couvre aussi les sources d'un autre dépôt.

**Une seule version de chaque skill visible par un agent.** Les skills de `skills/` sont des versions *portables* : elles servent à recréer
les skills dans un environnement qui n'en a pas. Si l'environnement possède déjà une version adaptée du même skill, ne pas installer la
version portable (l'agent verrait deux skills du même nom) : la version adaptée fait foi. Cas de l'installation d'origine (OpenClaw) :
l'agent ne charge que le dossier `skills/course-composer` du dépôt `second-brain` (déclaré dans `skills.load.extraDirs` de `openclaw.json`),
où les versions locales adaptées font foi ; les quatre skills de `skills/` ne servent là qu'à recréer les skills ailleurs. Le skill d'origine
`.claude/skills/h5p/SKILL.md` et `activite-h5p` portent le même rôle : n'en exposer qu'un à un même agent.

Garde-fous communs à tous les skills (à reprendre dans les consignes de l'agent, `AGENTS.md` du dépôt) : jamais de dépôt Moodle sans
accord explicite de l'utilisateur ; jamais de `--publish` pour des sources qui vivent dans un autre dépôt ; jamais de fusion de pull
request par l'agent ; aucune image générée sans accord ; pas de questions inventées dans une vidéo interactive sans transcrit ; jamais
d'écriture de JSON H5P à la main.

## 4. Vérifier l'installation

1. `python -m h5pharness types` : 63 types ; `python -m h5pharness spec qcm` : une fiche.
2. `python -m h5pharness build sources/exemples -o /tmp/essai --offline -q` : les 63 paquets se construisent (`OK`).
3. `python tools/qa.py /tmp/essai/qcm.h5p --render` : `OK` (PHP, node et Chromium fonctionnent ; réseau au premier usage). Même commande sur
   `/tmp/essai/glisser-deposer.h5p` : `OK` suivi de deux lignes `hauteur 400 px : …` et `hauteur 760 px : …` (mesure après « Vérifier »).
4. `python -m pytest -q` et `python -m ruff check .`. Les tests de dépôt réel sont ignorés sans `H5P_MOODLE_TEST_COURSE`.
5. Dépôt (si Moodle est sur la machine, avec `H5P_MOODLE_DIR` et `H5P_MOODLE_RUNAS` posés) : `build sources/exemples/vf.md --moodle <cours d'essai> --hidden` rend
   `MOODLE activité H5P créée : <url>` ; relancer rend `mise à jour` (pas de doublon).
6. `python -m h5pharness skills --exporter /tmp/skills --projet <PROJET>` : quatre `SKILL.md` sans `<HARNAIS>` ni `<PROJET>`.

## 5. Ce qui reste propre à chaque projet

- **Où vivent les sources.** Dans le dépôt du harnais (`sources/<matière>/`, `--publish` possible), ou dans le dépôt du projet : le
  harnais n'accepte que des médias situés dans son propre dépôt, on construit donc depuis une **copie de travail**
  (`rsync -a --delete <PROJET>/h5p/ <HARNAIS>/sources/<cours>/`, jamais commitée dans le harnais ; pour que git l'ignore sans modifier
  `.gitignore` : ajouter `sources/<cours>/` à `.git/info/exclude`). L'identifiant d'une activité Moodle dérive du chemin de la source
  sous le harnais : garder le même chemin pour mettre à jour la même activité, ne jamais le renommer après dépôt.
- **Les règles de conduite d'un projet** : types admis ou exclus, registre des énoncés et des retours, mesures de présentation
  (seuil de hauteur d'un glisser-déposer après « Vérifier » : le harnais la mesure, `--hauteur-max` l'applique), numérotation, qui valide, qui dépose, quelle forme (activité dédiée plutôt que page),
  usage de la banque de contenus, cours d'essai. Elles se déclarent dans la spécification du projet et dans les consignes de ses agents,
  pas dans le harnais.
- **Le Moodle cible** : sa version (4.5 ou plus), son dossier, le compte de dépôt, les droits des enseignants (`moodle/h5p:updatelibraries`
  pour installer des bibliothèques ; sinon le site doit déjà posséder les mêmes versions).
