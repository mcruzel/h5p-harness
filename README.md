# h5p-harness

Générateur **déterministe** de paquets H5P pour **Moodle** : un agent IA (ou un humain) écrit un
fichier Markdown court ; un script Python produit le paquet `.h5p` complet (bibliothèques,
traductions françaises, paramètres), le vérifie, le publie via git et, si Moodle est installé sur la
même machine, le dépose directement dans un cours (activité H5P ou page). La partie invariante d'un
paquet ne passe jamais par l'IA : elle ne coûte aucun token et ne peut pas « halluciner ».

```
sources/svt/cellule.md ──► python -m h5pharness build … [--publish] [--moodle <cours>]
   (seule partie variable)        │  lecture Markdown/YAML
                                  │  valeurs par défaut + traductions fr
                                  │  validation stricte, médias (chemins/URL) intégrés
                                  ▼
                          dist/svt/cellule.h5p ──► --moodle : activité H5P ou page dans le cours
                                               ──► --publish : git push des sources (release GitHub)
```

## Utilisation

```bash
pip install -r requirements.txt                          # une fois (automatique sur Claude Code web)
python -m h5pharness types                               # les 63 types disponibles
python -m h5pharness spec qcm                            # fiche d'un type
python -m h5pharness build sources/svt/cellule.md        # -> dist/svt/cellule.h5p
python -m h5pharness build sources/svt/cellule.md --publish   # + git add/commit/push des sources
python -m h5pharness build sources/svt/cellule.md --moodle svt5e --section 2   # + dépôt dans Moodle
python -m h5pharness transcript video.vtt                # transcrit compact (vidéo interactive)
```

Exemple de source (`type: quiz`) :

```markdown
---
type: quiz
title: La cellule – quiz de révision
preset: entrainement
---
## qcm
Quel organite est le siège de la **photosynthèse** ?
- [x] Le chloroplaste
- [ ] La mitochondrie
  > Non : la mitochondrie assure la respiration cellulaire.

## vf: faux
La mitochondrie contient de la chlorophylle.

## trous
La photosynthèse produit du {{dioxygène|oxygène}} et du {{glucose::un sucre}}.
```

## Exemples : un par type

[`sources/exemples/`](sources/exemples/) contient **un exemple validé pour chacun des 63 types**, nommé
d'après le type (`qcm.md`, `glisser-deposer.md`, `video-interactive.md`, `quiz-personnalite.md`…),
avec ses médias dans `sources/exemples/media/`. Ce sont à la fois des modèles à copier, les exemples
affichés dans les fiches `specs/`, et les données des tests. La liste des types figure dans
[`specs/README.md`](specs/README.md).

```bash
python -m h5pharness build sources/exemples                  # les 63 paquets -> dist/exemples/
python -m h5pharness build sources/exemples --moodle essais --section 1   # tout essayer dans un cours de test
```

Les paquets correspondants sont aussi téléchargeables dans la release GitHub de la branche (voir
« Où sont les paquets ? »).

## Format des sources

Le format est décrit dans [`specs/README.md`](specs/README.md) ; chaque type a sa fiche dans
`specs/` (générée depuis les schémas officiels : champs, valeurs par défaut en français, points
d'attention et un **exemple complet validé** pour chacun des 63 types). Deux écritures, combinables :
une **syntaxe Markdown simplifiée** (38 types, dont présentation, vidéo interactive, glisser-déposer
et scénario, avec mise en page automatique) et un **bloc YAML** qui donne accès à tous les champs de
**tous** les types (63 types de contenu + sous-contenus). En YAML aussi, le harnais complète ce que
l'éditeur H5P aurait calculé : positions absentes (diapos, glisser-déposer, vidéo, carte de jeu),
enchaînements d'un scénario, identifiants et chemins d'une carte, motifs des marqueurs de réalité
augmentée.

### Contrat de sortie (pensé pour les agents)

| code | sortie | conduite à tenir |
|---|---|---|
| 0 | `OK dist/…h5p (1,4 Mo, 200 ms)` (+ `PUBLIÉ commit …`, `MOODLE activité H5P créée : <url>`) | terminé ; une ligne `piste:` signale une possibilité à proposer (ex. transcrit d'une vidéo) |
| 1 | `ERREUR fichier: n problème(s)` + au plus 8 lignes `- emplacement: problème` | corriger ces points seulement (positions comptées à partir de 0) |
| 2 | `ECHEC_PUBLICATION …` / `ECHEC_MOODLE …` / `ECHEC_ENVIRONNEMENT …` | le paquet est bon : ne pas régénérer le contenu, signaler |
| 3 | `ECHEC_HARNAIS … (détails: dist/.harness-error.log)` | bogue du harnais |

Le skill [`.claude/skills/h5p/SKILL.md`](.claude/skills/h5p/SKILL.md) donne cette procédure aux
agents ; il ne charge qu'une description courte tant qu'il ne sert pas.

## Dépôt direct dans Moodle (même machine)

Moodle n'offre pas de service web pour créer des activités : quand il est installé sur la machine de
l'agent (serveur OpenClaw, par exemple), `--moodle` exécute un petit script PHP **dans** Moodle
(`h5pharness/moodle_deploy.php`), qui passe par l'API de Moodle (droits, journal, cache de cours) :

| option | effet |
|---|---|
| `--moodle <cours>` | id ou nom abrégé du cours (ou `moodle: {course: …}` dans l'en-tête) |
| `--as activite` (défaut) | **activité H5P** dédiée (suivi des tentatives, note dans le carnet) |
| `--as page` | nouvelle **page** qui intègre le contenu (filtre « Afficher H5P ») |
| `--page "<nom>"` ou `--page <id>` | ajoute le contenu à une **page existante** (sans toucher au reste) |
| `--section <n>` · `--hidden` | section du cours (créée si besoin) · caché aux étudiants |
| `--banque` | range aussi le contenu dans la **banque de contenus** du cours et y **lie** l'activité ou la page (un seul exemplaire : une mise à jour se répercute partout) |
| `--as banque` | banque de contenus seule, sans activité (l'enseignant l'insère où il veut) |

Relancer la même commande **met à jour** l'activité ou la page (identifiant stable dérivé du chemin de
la source), sans doublon. Configuration par variables d'environnement : `H5P_MOODLE_DIR` (dossier
contenant `config.php`, sinon recherche dans les emplacements usuels), `H5P_MOODLE_RUNAS` (compte
système propriétaire de moodledata, ex. `www-data`, via `sudo -n`/`runuser`), `H5P_MOODLE_USER` (compte
Moodle utilisé ; défaut : l'administrateur principal, seul capable d'installer les bibliothèques H5P
contenues dans le paquet), `H5P_MOODLE_PHP`, `H5P_MOODLE_BANQUE=1` (banque de contenus par défaut), `H5P_MOODLE_OWNER` (voir
ci-dessous). Vérifié de bout en bout sur Moodle 5.0 + PostgreSQL : les exemples
des 63 types et les 5 variantes YAML (68 activités) déposés en 32 s, puis ouverts sans erreur par un
compte élève (bibliothèques installées par Moodle au premier affichage) ; page existante complétée,
mise à jour sans doublon, dépôt au nom d'un enseignant et sous `www-data`, banque de contenus (contenu
lié, mis à jour, visible dans la banque du cours).

**Banque de contenus : facultative.** Comme lorsqu'un enseignant téléverse un `.h5p` dans une activité,
le contenu est par défaut rangé dans l'activité elle-même : il fonctionne et reste modifiable par les
enseignants (bouton « Modifier le contenu H5P » de l'activité) sans passer par la banque, qui sert
surtout à **réutiliser** un contenu (autres activités, pages, bouton H5P de l'éditeur de texte). Avec
`--banque`, l'activité ou la page pointe vers le contenu de la banque, comme le fait Moodle quand on le
choisit avec « Lier au fichier ». Dans la banque, un enseignant ne peut modifier que ses propres
contenus (les autres le sont par les gestionnaires et créateurs de cours) : `H5P_MOODLE_OWNER=<identifiant>`
attribue les contenus de banque à cet enseignant, le fichier restant au nom du compte de dépôt (ce qui
permet à Moodle d'installer les bibliothèques). Sans `--banque`, la sortie le rappelle par une ligne
`piste:`.

## Moodle

- **Version** : Moodle **4.5 ou plus récent** (les bibliothèques embarquées exigent l'API H5P 1.28,
  livrée avec `h5plib_v128`). Pour Moodle 4.4 ou 4.1, il faudrait embarquer des versions plus
  anciennes des bibliothèques.
- **Droits** : par défaut seul le rôle *gestionnaire* peut installer des bibliothèques
  (`moodle/h5p:updatelibraries`). Un paquet déposé par un *enseignant* fonctionne si le site possède
  déjà les mêmes versions (tâche planifiée « Télécharger les types de contenu H5P » active, ou un
  paquet complet déposé une fois par un gestionnaire). Les paquets produits contiennent toujours
  les bibliothèques : ils conviennent aux deux cas. `--content-only` produit un paquet de quelques Ko
  sans bibliothèques.
- **Import** : activité « Contenu interactif H5P » ou banque de contenus, fichier `.h5p`. La release
  propose aussi une variante `.contenu-seul.h5p` (sans bibliothèques, quelques Ko) pour les sites
  qui ont déjà les bonnes versions et une limite de dépôt faible.
- **Réseau des élèves** : la frise (`frise`) charge jQuery et des polices depuis les serveurs de
  Google à l'affichage (comportement de la bibliothèque officielle TimelineJS).
- **Vidéo interactive** : questions et activités seulement d'après le transcrit horodaté de la vidéo
  (`transcript: fichier.vtt` ou `.srt`) ; le harnais vérifie leur placement, les signale si elles
  semblent sans rapport avec le passage, et ajoute le transcrit en sous-titres. Sans transcrit, il
  construit la vidéo seule et indique en « piste » comment l'obtenir.
- **Réalité augmentée** (`chasse-ar`) : les marqueurs à imprimer se téléchargent dans l'éditeur H5P
  de Moodle (en modifiant l'activité) ; `twitter` est obsolète (X a fermé l'intégration).

## Où sont les paquets ? (poids de l'historique git)

Les `.h5p` ne sont **pas** versionnés : un paquet complet pèse 1 à 5 Mo, git compresse mal les zip,
et chaque régénération alourdirait définitivement l'historique. Comme la construction est
**reproductible** (même source ⇒ même paquet à l'octet près), seules les sources sont versionnées :
`--publish` pousse le `.md` et ses médias ; un workflow GitHub volontairement minimal
(`.github/workflows/h5p.yml` : déclenché seulement par un changement dans `sources/`, sans tests,
désactivable avec la variable de dépôt `H5P_RELEASES=off`) reconstruit les paquets et les attache à
la release **`h5p-<branche>`** (onglet *Releases*), dont un paquet par type grâce à
`sources/exemples/`. Seuls les paquets modifiés sont renvoyés (empreinte SHA-256 comparée à celle de la
release), ce qui garde chaque passage court. Le paquet est aussi disponible immédiatement en local dans
`dist/`.

## Médias

`![description](images/schema.png)` ou `image: {src: https://…, license: CC BY-SA 4.0, author: …}` :
chemin relatif au `.md` ou à la racine du dépôt, ou URL complète. Les URL sont téléchargées une fois
dans `sources/.media/` (+ `lock.json`) et versionnées avec la source : la CI reconstruit hors ligne.
Les images sont converties (WebP, BMP, TIFF → PNG/JPG, refusés par Moodle ; SVG si `cairosvg` est
installé) et redimensionnées (1920 px).
Vidéos : lien YouTube/Vimeo conservé tel quel, ou fichier MP4/WebM.
**L'environnement de l'agent doit pouvoir joindre l'hôte des URL** (politique réseau).

## Garanties et contrôles

1. validation stricte pendant la construction : types, champs obligatoires, bornes, balises HTML
   autorisées champ par champ (H5P les supprimerait en silence), syntaxes des trous, règles propres
   aux types (au moins une bonne réponse, mots croisés constructibles, indices de zones…) ;
2. contrôle structurel du paquet (liste blanche de fichiers, dépendances) ;
3. `python tools/qa.py dist/` : **validateur officiel `h5p-php-library`** (le code qu'embarque
   Moodle), en droits gestionnaire et enseignant, et vérification que le filtre d'affichage ne
   modifie rien ; avec `--render`, chaque paquet est aussi joué dans Chromium (h5p-standalone) et
   toute erreur JavaScript est signalée. Ces contrôles tournent en local ; sur GitHub, seulement à la
   demande (workflow manuel « Tests du harnais »), pour ne pas consommer de minutes d'Actions.

## Maintenance

| tâche | commande |
|---|---|
| mettre à jour les bibliothèques H5P | `python tools/vendor_libraries.py` puis `python -m h5pharness specs` |
| régénérer les fiches | `python -m h5pharness specs` |
| tests | `python -m pytest` · `python -m ruff check .` |
| contrôle complet | `python tools/qa.py dist/ --render` |
| ajouter des lignes aux commits de `--publish` | variable `H5P_COMMIT_TRAILERS` (ex. `Co-Authored-By: …`) |

Les bibliothèques (`vendor/libraries`, 175 bibliothèques pour 63 types, 55 Mo) viennent des dépôts
GitHub listés par le registre officiel `h5p-cli` (`vendor/registry.json`, corrections dans
`vendor/registry-extra.json`), compilées si nécessaire. Pour chaque dépôt, la branche `release` (ce
que publie le Hub H5P, donc ce qu'installe Moodle) est préférée à la branche de développement quand
elle est tenue à jour ; `vendor/libraries.lock.json` enregistre dépôt, branche et commit de chacune.
Le Hub H5P (`api.h5p.org`) serait la source canonique mais il était inaccessible depuis
l'environnement de développement.

## Arborescence

```
h5pharness/       moteur (engine, markdown, markers, media, package, sugar/, specs, cli)
h5pharness/l10n/  traductions françaises manquantes dans les bibliothèques officielles
specs/            fiches par type (générées)
sources/          activités (Markdown) + sources/.media/ (médias téléchargés)
sources/exemples/ un exemple validé par type (63) + media/ (leurs médias)
tests/            tests ; tests/fixtures/ : cinq exemples réécrits entièrement en YAML
tools/            vendoring, validateur officiel, rendu headless, publication des releases
vendor/           bibliothèques H5P et verrou des versions
```
