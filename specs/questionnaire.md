# Questionnaire — `questionnaire`

H5P.Questionnaire 1.3 · alias : questionnaire · syntaxe Markdown simplifiée : non (bloc ```yaml)

## Champs (bloc ```yaml, noms H5P)

`*` = obligatoire ; les autres champs ont une valeur par défaut ou sont facultatifs.

- questionnaireElements* : liste (min 1) — Eléments du questionnaire
  chaque élément :
    - library* : sous-contenu, library: question-ouverte | choix-simple — Bibliothèque
    - requiredField : booléen, défaut false — Champ requis
- successScreenOptions : groupe — Ecran en cas de réussite
  - enableSuccessScreen : booléen, défaut true — Activer l'écran
  - successScreenImage : groupe — Ajouter une image à l'écran (groupe à un champ: écrire directement la valeur)
    - successScreenImage : sous-contenu, library: image — Rempacez l'icône de la réussite avec une image
  - successMessage : texte, défaut Vous avez terminé le question… — Texte affiché à l'envoi des réponses

Textes d'interface pré-remplis en français (ne pas fournir sauf besoin) : uiElements.
