---
name: depot-moodle-h5p
description: "Dépose une activité H5P construite par le harnais h5pharness dans un cours d'un Moodle installé sur la même machine (activité H5P, page ou banque de contenus ; création ou mise à jour sans doublon), après accord explicite de l'utilisateur. À utiliser pour publier une activité H5P contrôlée dans un cours Moodle."
---

# Déposer une activité H5P sur Moodle

Prérequis : le paquet est construit (`OK`, skill `activite-h5p`) et contrôlé (skill `controler-activite-h5p`). Les commandes se lancent depuis
`<HARNAIS>`. Le projet est dans `<PROJET>`. Ce skill ne s'applique qu'à un Moodle **4.5 ou plus récent installé sur la même machine** :
le harnais exécute un script PHP dans Moodle (`h5pharness/moodle_deploy.php`), qui passe par l'API de Moodle (droits, journal,
cache de cours), comme si un enseignant avait téléversé le paquet.

## Configuration (une fois, dans l'environnement de l'agent ; aucun fichier versionné)

| variable | rôle |
|---|---|
| `H5P_MOODLE_DIR` | dossier de Moodle (celui qui contient `config.php`) ; sinon les emplacements usuels sont cherchés ; équivalent : `--moodle-dir` |
| `H5P_MOODLE_RUNAS` | compte système propriétaire de moodledata (`www-data`…) : le script PHP s'exécute sous ce compte (`sudo -n`, ou `runuser` en root) |
| `H5P_MOODLE_USER` | compte Moodle du dépôt ; défaut : l'administrateur principal, seul capable d'installer les bibliothèques H5P du paquet |
| `H5P_MOODLE_PHP` | binaire PHP (défaut `php`) |
| `H5P_MOODLE_BANQUE` | `1` : range aussi chaque contenu dans la banque de contenus du cours (comme `--banque`) |
| `H5P_MOODLE_OWNER` | compte enseignant auquel les contenus de banque sont attribués (pour qu'il puisse les modifier) |

Si le compte système demande `sudo`, l'autoriser sans mot de passe pour la commande PHP du harnais seulement. Pour vérifier la
configuration, déposer (avec l'accord de l'utilisateur) un exemple masqué dans un cours d'essai :
`python -m h5pharness build sources/exemples/vf.md --moodle <cours d'essai> --hidden`.

## Procédure

1. **Accord** : demander à l'utilisateur l'accord explicite pour déposer, avec le cours (id ou nom abrégé), la section, la forme
   (activité, page, banque) et la visibilité. Sans accord, ne rien déposer. Un accord pour produire ou contrôler le paquet n'est
   pas un accord pour déposer.
2. **Premier dépôt** : activité dédiée (suivi des tentatives, note au carnet) et **masquée** ; l'utilisateur la rend visible lui-même :
   `.venv/bin/python -m h5pharness build sources/<cours>/<fichier>.md --moodle <cours> --section <n> --hidden`.
3. **Formes** : `--as activite` (défaut) ; `--as page` (nouvelle page qui intègre le contenu) ; `--page "<nom ou id>"` (ajoute le contenu à une
   page **existante**) ; `--as banque` (banque de contenus seule) ; `--banque` (range aussi le contenu dans la banque du cours et y lie
   l'activité, pour le réutiliser ailleurs). `--page` et `--as page` écrivent dans une page sans sauvegarde ni comparaison avec la
   version en ligne : ne les employer qu'avec l'accord explicite de l'utilisateur pour cette page. Ne pas ajouter `--banque` de sa
   propre initiative : la ligne `piste:` de la sortie le rappelle, la proposer.
4. **Mise à jour** : relancer la même commande, **depuis le même chemin de source**, met à jour la même activité (identifiant
   stable dérivé du chemin de la source), sans doublon. Avant, demander à l'utilisateur si l'activité en ligne a été retouchée dans
   Moodle ; si oui, attendre son arbitrage : le harnais écraserait ses modifications. Ne jamais renommer ni déplacer une source déjà déposée.
5. **Résultat** : la ligne `MOODLE activité H5P créée|mise à jour : <url>` donne l'adresse (et l'identifiant de l'activité) ; la
   consigner dans le suivi du projet. Vérifier ensuite l'affichage avec un compte élève ou l'aperçu : les bibliothèques H5P sont
   installées par Moodle au premier affichage.
6. **Erreurs** : `ECHEC_MOODLE` (cours introuvable, droits, Moodle absent, PHP) : le paquet est bon, ne pas régénérer le contenu ; lire
   le message, corriger la configuration ou signaler. `ECHEC_ENVIRONNEMENT` : idem. `ECHEC_HARNAIS` : bogue, signaler le journal.

## Règles

- Jamais de dépôt sans accord explicite ; jamais de suppression d'activité ; ne pas modifier à la main les réglages d'une activité déposée.
- Un enseignant (`H5P_MOODLE_USER` non administrateur) ne peut installer des bibliothèques que s'il a le droit `moodle/h5p:updatelibraries`
  ; sinon le site doit déjà posséder les mêmes versions. Les paquets complets (défaut) conviennent aux deux cas.
- Cours d'essai recommandé pour un premier test : un cours masqué ; supprimer l'essai relève de l'utilisateur.
- La spécification du projet dit qui valide, qui dépose et quelle forme employer ; le harnais ne le décide pas.
