# Image — `image`

H5P.Image 1.1 · alias : image · syntaxe Markdown simplifiée : oui

## Syntaxe Markdown

Une seule ligne `![description](image ou URL "titre au survol")`. Description vide = image décorative.

## Champs (bloc ```yaml, noms H5P)

`*` = obligatoire ; les autres champs ont une valeur par défaut ou sont facultatifs.

- file : image (chemin ou URL) — Image
- decorative : booléen, défaut false — Cette image ne sert que de décoration (Activez cette option si l'image est purement décorative et n'ajoute aucune information au contenu de la page.…)
- alt : texte, conditionnel — Texte alternatif (Obligatoire. Ce texte sera affiché si l'image n'apparaît pas dans le navigateur.)
- title : texte — Texte de survol (Optionnel. Ce texte est affiché quand la souris survole une image.)

Textes d'interface pré-remplis en français (ne pas fournir sauf besoin) : contentName, expandImage, minimizeImage.
