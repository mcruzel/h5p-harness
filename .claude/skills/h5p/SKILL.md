---
name: h5p
description: Crée ou modifie des activités H5P pour Moodle (QCM, vrai/faux, quiz, texte à trous, glisser-déposer, mots croisés, mots mêlés, cartes, flashcards, livre interactif, présentation, vidéo interactive… 60 types) en écrivant un simple fichier Markdown ; un générateur déterministe produit le paquet .h5p sans consommer de tokens. À utiliser dès qu'on demande une activité, une ressource ou un exercice H5P, ou un paquet .h5p.
---

# Activités H5P pour Moodle

Ne jamais écrire de JSON H5P ni lire `vendor/` : le générateur s'en charge.

1. **Choisir le type** dans le tableau de `specs/README.md` (colonne « type ») et lire sa fiche :
   `python -m h5pharness spec <type>` (syntaxe Markdown simplifiée si elle existe, sinon champs YAML).
   Au premier usage seulement, lire le haut de `specs/README.md` (règles communes).
2. **Écrire** `sources/<matière>/<nom-court>.md` : en-tête YAML (`type`, `title`, et au besoin `preset`,
   `license`, `authors`) puis le corps. Médias : chemin dans le dépôt ou URL complète.
3. **Construire et publier** : `python -m h5pharness build sources/<matière>/<nom-court>.md --publish`
4. **Lire la sortie** (quelques lignes) :
   - `OK …` puis `PUBLIÉ …` → terminé : la CI attache le paquet à la release GitHub `h5p-<branche>` ;
     le fichier local est dans `dist/`.
   - `ERREUR` → corriger **uniquement** les points cités (`l.12` = ligne du fichier ; `answers[2]` = 2e
     élément), relancer ; au 2e échec, exposer le problème à l'utilisateur.
   - `ECHEC_PUBLICATION` / `ECHEC_ENVIRONNEMENT` → ne pas régénérer le contenu ; signaler.
   - `ECHEC_HARNAIS` → bogue du générateur ; signaler avec le chemin du journal.
   - `avertissement(s)` → le paquet est valide ; corriger si c'est simple (ex. mise en forme retirée).

Vérifier sans écrire de paquet : `python -m h5pharness check <fichier.md>`.
Si `import yaml`/`markdown_it` échoue : `pip install -r requirements.txt`.
