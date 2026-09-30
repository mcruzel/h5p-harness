---
name: h5p
description: Crée ou modifie des activités H5P pour Moodle (QCM, vrai/faux, quiz, texte à trous, glisser-déposer, mots croisés, mots mêlés, cartes, flashcards, livre interactif, présentation, vidéo interactive, quiz de personnalité, bingo… 63 types) en écrivant un simple fichier Markdown ; un générateur déterministe produit le paquet .h5p sans consommer de tokens et peut le déposer directement dans un cours d'un Moodle installé sur la même machine (activité H5P ou page). À utiliser dès qu'on demande une activité, une ressource ou un exercice H5P, un paquet .h5p, ou d'en ajouter à un cours Moodle.
---

# Activités H5P pour Moodle

Ne jamais écrire de JSON H5P ni lire `vendor/` : le générateur s'en charge.

1. **Choisir le type** dans le tableau de `specs/README.md` (colonne « type ») et lire sa fiche :
   `python -m h5pharness spec <type>` (syntaxe Markdown simplifiée si elle existe, champs YAML, exemple
   complet validé). Au premier usage seulement, lire le haut de `specs/README.md` (règles communes).
2. **Écrire** `sources/<matière>/<nom-court>.md` : en-tête YAML (`type`, `title`, et au besoin `preset`,
   `license`, `authors`) puis le corps. Médias : chemin dans le dépôt ou URL complète.
   **Vidéo interactive** : des questions ou activités dans la vidéo seulement d'après son **transcrit
   horodaté** (`.vtt`/`.srt`) déclaré par `transcript: fichier.vtt` ; si tu ne l'as pas, demande-le à
   l'agent qui t'a confié la tâche ou à l'utilisateur. Lis-le avec
   `python -m h5pharness transcript fichier.vtt` et place chaque question après le passage qui y répond.
3. **Construire** (et, selon la demande, publier et/ou déposer dans Moodle) :
   - `python -m h5pharness build sources/<matière>/<nom-court>.md --publish` (git add/commit/push) ;
   - dépôt dans un Moodle **installé sur la même machine** : ajouter `--moodle <cours>` (id ou nom abrégé)
     et, au choix, `--as activite` (activité H5P dédiée, notée ; défaut) ou `--as page` (page qui intègre
     le contenu), `--page "<nom de page existante>"` (ajoute le contenu à cette page), `--section <n>`,
     `--hidden`. Relancer la même commande met à jour la même activité (pas de doublon).
4. **Lire la sortie** (quelques lignes) :
   - `OK …` → paquet dans `dist/` ; `PUBLIÉ …` → sources poussées ; `MOODLE … : <url>` → déposé.
   - `ERREUR` → corriger **uniquement** les points cités (`l.12` = ligne du fichier ; `answers[1]` = 2e
     élément, les positions commencent à 0), relancer ; au 2e échec, exposer le problème à l'utilisateur.
   - `piste:` → possibilité offerte (ex. obtenir le transcrit d'une vidéo pour y ajouter des questions) :
     la proposer à l'utilisateur ou à l'agent parent si c'est utile.
   - `ECHEC_PUBLICATION` / `ECHEC_MOODLE` / `ECHEC_ENVIRONNEMENT` → le paquet est bon : ne pas régénérer le
     contenu ; signaler le message (cours introuvable, droits, Moodle absent…).
   - `ECHEC_HARNAIS` → bogue du générateur ; signaler avec le chemin du journal.
   - `avertissement(s)` → le paquet est valide ; corriger si c'est simple (ex. mise en forme retirée).

Vérifier sans écrire de paquet : `python -m h5pharness check <fichier.md>`.
Si `import yaml`/`markdown_it` échoue : `pip install -r requirements.txt`.
