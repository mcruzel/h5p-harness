# h5p-harness

Générateur **déterministe** de paquets H5P pour **Moodle** : un agent IA (ou un humain) écrit un
fichier Markdown court ; un script Python produit le paquet `.h5p` complet (bibliothèques,
traductions françaises, paramètres), le vérifie, puis le publie via git. La partie invariante
d'un paquet ne passe jamais par l'IA : elle ne coûte aucun token et ne peut pas « halluciner ».

```
sources/svt/cellule.md ──► python -m h5pharness build … --publish ──► git push (sources)
   (seule partie variable)        │  lecture Markdown/YAML                 │
                                  │  valeurs par défaut + traductions fr   ▼
                                  │  validation stricte               CI GitHub : reconstruction,
                                  │  médias (chemins/URL) intégrés     validateur H5P officiel,
                                  ▼                                    release « h5p-<branche> »
                          dist/svt/cellule.h5p  ──────────────────────► import dans Moodle
```

## Utilisation

```bash
pip install -r requirements.txt                          # une fois (automatique sur Claude Code web)
python -m h5pharness types                               # les 60 types disponibles
python -m h5pharness spec qcm                            # fiche d'un type
python -m h5pharness build sources/svt/cellule.md        # -> dist/svt/cellule.h5p
python -m h5pharness build sources/svt/cellule.md --publish   # + git add/commit/push des sources
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

Le format est décrit dans [`specs/README.md`](specs/README.md) ; chaque type a sa fiche dans
`specs/` (générée depuis les schémas officiels, libellés en français). Deux écritures, combinables :
une **syntaxe Markdown simplifiée** pour les types courants, et un **bloc YAML** qui donne accès à
tous les champs de **tous** les types.

### Contrat de sortie (pensé pour les agents)

| code | sortie | conduite à tenir |
|---|---|---|
| 0 | `OK dist/…h5p (1,4 Mo, 200 ms)` (+ `PUBLIÉ commit … poussé sur …`) | terminé |
| 1 | `ERREUR fichier: n problème(s)` + au plus 8 lignes `- emplacement: problème` | corriger ces points seulement |
| 2 | `ECHEC_PUBLICATION …` / `ECHEC_ENVIRONNEMENT …` | ne pas régénérer le contenu, signaler |
| 3 | `ECHEC_HARNAIS … (détails: dist/.harness-error.log)` | bogue du harnais |

Le skill [`.claude/skills/h5p/SKILL.md`](.claude/skills/h5p/SKILL.md) donne cette procédure aux
agents ; il ne charge qu'une description courte tant qu'il ne sert pas.

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
- **Import** : activité « Contenu interactif H5P » ou banque de contenus, fichier `.h5p`.

## Où sont les paquets ? (poids de l'historique git)

Les `.h5p` ne sont **pas** versionnés : un paquet complet pèse 1 à 5 Mo, git compresse mal les zip,
et chaque régénération alourdirait définitivement l'historique. Comme la construction est
**reproductible** (même source ⇒ même paquet à l'octet près), seules les sources sont versionnées :
`--publish` pousse le `.md` et ses médias, puis la CI (`.github/workflows/h5p.yml`) reconstruit,
valide avec le cœur PHP officiel d'H5P et attache les paquets à la release GitHub
**`h5p-<branche>`** (onglet *Releases* du dépôt ; aussi en artefact de workflow 30 jours). Le paquet
est aussi disponible immédiatement en local dans `dist/`.

## Médias

`![description](images/schema.png)` ou `image: {src: https://…, license: CC BY-SA 4.0, author: …}` :
chemin relatif au `.md` ou à la racine du dépôt, ou URL complète. Les URL sont téléchargées une fois
dans `sources/.media/` (+ `lock.json`) et versionnées avec la source : la CI reconstruit hors ligne.
Les images sont converties (SVG, WebP → PNG/JPG, refusés par Moodle) et redimensionnées (1920 px).
Vidéos : lien YouTube/Vimeo conservé tel quel, ou fichier MP4/WebM.
**L'environnement de l'agent doit pouvoir joindre l'hôte des URL** (politique réseau).

## Garanties et contrôles

1. validation stricte pendant la construction : types, champs obligatoires, bornes, balises HTML
   autorisées champ par champ (H5P les supprimerait en silence), syntaxes des trous, règles propres
   aux types (au moins une bonne réponse, mots croisés constructibles, indices de zones…) ;
2. contrôle structurel du paquet (liste blanche de fichiers, dépendances) ;
3. en CI : **validateur officiel `h5p-php-library`** (le code qu'embarque Moodle), en droits
   gestionnaire et enseignant, et vérification que le filtre d'affichage ne modifie rien ;
4. en local : `python tools/qa.py dist/ --render` joue aussi chaque paquet dans Chromium
   (h5p-standalone) et signale toute erreur JavaScript.

## Maintenance

| tâche | commande |
|---|---|
| mettre à jour les bibliothèques H5P | `python tools/vendor_libraries.py` puis `python -m h5pharness specs` |
| régénérer les fiches | `python -m h5pharness specs` |
| tests | `python -m pytest` · `python -m ruff check .` |
| contrôle complet | `python tools/qa.py dist/ --render` |

Les bibliothèques (`vendor/libraries`, 171 bibliothèques pour 60 types, 54 Mo) viennent des dépôts
GitHub listés par le registre officiel `h5p-cli` (`vendor/registry.json`, corrections dans
`vendor/registry-extra.json`), compilées si nécessaire. Le Hub H5P (`api.h5p.org`) serait la source
canonique mais il était inaccessible depuis l'environnement de développement.

## Arborescence

```
h5pharness/       moteur (engine, markdown, markers, media, package, sugar/, specs, cli)
h5pharness/l10n/  traductions françaises manquantes dans les bibliothèques officielles
specs/            fiches par type (générées)
sources/          activités (Markdown) + sources/.media/ (médias téléchargés)
tests/            tests + exemples de chaque type (tests/examples/) + médias de test
tools/            vendoring, validateur officiel, rendu headless, publication des releases
vendor/           bibliothèques H5P et verrou des versions
```
