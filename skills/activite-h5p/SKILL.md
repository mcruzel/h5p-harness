---
name: activite-h5p
description: "Produit une activité H5P pour Moodle (QCM, vrai/faux, quiz, trous, glisser-déposer, présentation, vidéo interactive… 63 types) en écrivant un fichier Markdown, avec le harnais h5pharness : paquet .h5p déterministe, sans écrire de JSON ni consommer de tokens pour la partie invariante. À utiliser pour toute demande d'activité, d'exercice ou de paquet H5P."
---

# Produire une activité H5P

Le harnais est dans `<HARNAIS>` (les commandes se lancent depuis ce dossier : `cd <HARNAIS> && .venv/bin/python -m h5pharness …`,
ou `python -m h5pharness …` si les dépendances sont installées pour le Python courant). Le projet (sources, spécification
de ses exercices) est dans `<PROJET>`. Installation et configuration d'un nouvel environnement : `<HARNAIS>/docs/INTEGRATION.md`.

Tu écris une source Markdown courte, le harnais fait le reste : bibliothèques H5P, traductions françaises, paramètres, validation.
**Ne jamais écrire de JSON H5P à la main, ne jamais lire `vendor/`.**

## Où vivent les sources

- **Sources du harnais** : `<HARNAIS>/sources/<matière>/<nom-court>.md` ; `build … --publish` les pousse (git add, commit, push) sur
  le dépôt du harnais, et seulement si l'utilisateur le demande.
- **Sources d'un projet** (dans `<PROJET>`, par exemple `<PROJET>/h5p/<leçon>-exercice-<n>.md`) : la source du projet fait foi, mais le
  harnais n'accepte que des médias situés dans son propre dépôt. On construit donc à partir d'une **copie de travail** :
  `rsync -a --delete <PROJET>/h5p/ <HARNAIS>/sources/<cours>/` (un sous-dossier propre au projet, jamais `exemples/`), puis
  `build sources/<cours>/<fichier>.md`. Jamais `--publish` (il pousserait la copie sur le dépôt du harnais), jamais de commit
  dans le harnais. Garder le même chemin `sources/<cours>/<fichier>.md` d'une fois sur l'autre : l'identifiant de l'activité Moodle
  en dérive (voir le skill `depot-moodle-h5p`).

## Procédure

1. **Choisir le type** à partir de la capacité à travailler, pas du catalogue : `python -m h5pharness types` (63 types) ;
   fiche d'un type : `python -m h5pharness spec <type>` (syntaxe Markdown simplifiée si elle existe, champs YAML, valeurs par défaut
   en français, points d'attention, **exemple complet validé**, aussi dans `<HARNAIS>/sources/exemples/<type>.md`). Au premier
   usage, lire le haut de `<HARNAIS>/specs/README.md` (règles communes). Les règles du projet (types admis ou exclus, registre des
   énoncés et des retours, qui choisit le type) se lisent dans la spécification du projet, pas ici.
2. **Écrire** `<source>.md` : en-tête YAML (`type`, `title`, au besoin `preset`, `license`, `authors`, `moodle:`) puis le corps. Une note
   d'auteur s'écrit en commentaires YAML (`# …`) dans l'en-tête, jamais en commentaire HTML dans le corps (il serait lu comme une question).
3. **Médias** : `![description](chemin)` ou `image: {src: …}` ; chemin relatif au `.md` ou à la racine du harnais, ou URL complète
   (téléchargée une fois dans `<HARNAIS>/sources/.media/` ; l'environnement doit pouvoir joindre l'hôte). Écrire l'alternative
   textuelle d'après ce que l'image montre ; licence et auteur pour une image tierce. Jamais d'image générée sans l'accord de
   l'utilisateur. Vidéo : lien YouTube/Vimeo ou fichier MP4/WebM.
4. **Vidéo interactive** : des questions ou activités dans la vidéo seulement d'après son **transcrit horodaté** (`.vtt` ou `.srt`),
   déclaré par `transcript: fichier.vtt`. Sans transcrit, ne pas inventer de questions : le demander à l'utilisateur. Le lire avec
   `python -m h5pharness transcript fichier.vtt` et placer chaque interaction après le passage qui y répond.
5. **Vérifier sans écrire de paquet** : `python -m h5pharness check <source>.md`.
6. **Construire** : `python -m h5pharness build <source>.md` (paquet dans `<HARNAIS>/dist/…`, reproductible à l'octet près). Un
   dossier est accepté : `build sources/<cours>` construit tout.
7. **Lire la sortie** (quelques lignes) :
   - `OK …` (code 0) : paquet construit ; `avertissement(s)` : paquet valide, corriger si c'est simple.
   - `ERREUR <fichier>: n problème(s)` (code 1) : corriger **uniquement** les points cités (`l.12` = ligne du fichier ; `answers[1]` =
     deuxième élément, les positions commencent à 0), relancer ; au deuxième échec, exposer le problème à l'utilisateur.
   - `piste:` : possibilité offerte (transcrit d'une vidéo, banque de contenus…) à proposer à l'utilisateur si c'est utile.
   - `ECHEC_PUBLICATION`, `ECHEC_MOODLE`, `ECHEC_ENVIRONNEMENT` (code 2) : le paquet est bon, ne pas régénérer le contenu ; signaler le message.
   - `ECHEC_HARNAIS` (code 3) : bogue du générateur ; signaler avec le chemin du journal (`dist/.harness-error.log`).
8. **Contrôler** avant tout dépôt : skill `controler-activite-h5p`. **Déposer** sur Moodle : skill `depot-moodle-h5p`.

## Règles

- Un type en version bêta (`0.x` dans `types`) ou signalé obsolète ou fragile (`twitter` obsolète ; `frise` charge des ressources chez
  l'élève ; `chasse-ar` demande des marqueurs à imprimer) se signale à l'utilisateur avant usage.
- Construire n'est pas déposer : un accord pour produire le paquet n'est pas un accord pour le déposer sur Moodle.
- Ne rien écrire dans `<HARNAIS>/sources/exemples/` : un exemple validé par type, rien d'autre.
- Si `import yaml` ou `import markdown_it` échoue : `pip install -r requirements.txt` dans `<HARNAIS>`.
