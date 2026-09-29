# KewAr Code — `qr-code`

H5P.KewArCode 1.7 · alias : qr-code, kewarcode, kew-ar-code · syntaxe Markdown simplifiée : non (bloc ```yaml)

## Champs (bloc ```yaml, noms H5P)

`*` = obligatoire ; les autres champs ont une valeur par défaut ou sont facultatifs.

- introduction : texte riche (Markdown: a code col colgroup del em figcaption figure h1 h2 h3 h4 h5 h6 hr li ol pre s strong sub sup table tbody td tfoot th thead tr u ul) — Introductory text (This text can optionally be presented along with your code.)
- codeType : choix contact|event|email|h5p|location|phone|sms|text|url, défaut url — Type de code (Sélectionnez le type de code que vous souhaitez générer)
- contact : groupe, conditionnel — Contact
  - name* : texte — Name
  - organization : texte — Organization
  - title : texte — Title
  - number : texte — Phone number (Phone number (please use the format +12 345 67890))
  - email : texte — Email address (Email address to write message to)
  - address : groupe — Address
    - extended : texte — Adresse complète (c/o information, etc.)
    - street : texte — Street (Street including number)
    - locality : texte — Locality (City name, etc.)
    - region : texte — Region (Federal state, county, etc.)
    - zip : texte — ZIP code
    - country : texte — Country
  - url : texte — Website (Website to link to (must start with https:// or http://))
  - note : texte — Note
- event : groupe, conditionnel — Événement
  - title* : texte — Titre (Title for the calendar event)
  - allDay : booléen — Événement de toute une journée (Check if event will be valid all day long)
  - dateStart* : texte — Date de début (Start date of the event (please use the format yyyy/mm/dd))
  - timeStart : texte, conditionnel — Heure de début (Heure de début de l'événement (veuillez utiliser le format hh : mm))
  - dateEnd* : texte — Date de fin (Date de fin de l'événement (veuillez utiliser le format aaaa/mm/jj))
  - timeEnd : texte, conditionnel — End time (End time of the event (please use the format hh:mm))
  - timezone : choix -12:00|-11:00|-10:00|-9:30|-9:00|-8:00|-7:00|-6:00|-5:00|-4:00|…, défaut 0:00, conditionnel — Fuseau horaire (Sélectionner le fuseau horaire dans lequel l'événement doit avoir lieu)
  - daylightSavings : booléen, conditionnel — L'heure d'été (Vérifier si l’emplacement où se déroule l'événement utilise l'heure d'été)
  - location : texte — Location (Name the location)
  - description : texte — Description (Add a description for the event)
- email : groupe, conditionnel — Email address (groupe à un champ: écrire directement la valeur)
  - email* : texte — Email address (Email address to write message to)
- h5p : groupe, conditionnel — Contenu H5P (groupe à un champ: écrire directement la valeur)
  - contentTypes* : liste (min 1) — Content types (Select the H5P content type that you want to display. If you select more than one, one will be picked randoml…)
    chaque élément = sous-contenu, library: accordeon | calendrier-avent | agamotto | audio | enregistreur-audio | calcul-mental | trous | graphique | collage | colonne | mots-croises | presentation | cartes | dictee | outil-documentation | glisser-deposer | glisser-mots | redaction | mots-meles | flashcards | devinette | tableau | texte | iframe | image | choix-images | image-interactive | trouver-zone | avant-apres | paires-images | sequence-images | carrousel | livre | video-interactive | lien | marquer-mots | memory | qcm | questionnaire | quiz | choix-unique | trier-paragraphes | resume | frise | vf | video | visite-360 — Contenu H5P (Contenu H5P à afficher)
- location : groupe, conditionnel — Emplacement
  - latitude* : texte — Latitude (Latitude (veuillez utiliser le format 53.864462))
  - longitude* : texte — Longitude (Longitude (please use the format 10.663792))
- phone : groupe, conditionnel — Numéro de téléphone (groupe à un champ: écrire directement la valeur)
  - number* : texte — Numéro de téléphone (Numéro de téléphone à appeler (veuillez utiliser le format +12 345 67890))
- sms : groupe, conditionnel — SMS
  - number* : texte — Numéro de téléphone (Numéro de téléphone à envoyer (veuillez utiliser le format +12 345 67890))
  - message* : texte — Message (Message to send)
- text : groupe, conditionnel — Text (groupe à un champ: écrire directement la valeur)
  - text* : texte multiligne — Text (Text to encode)
- url : groupe, conditionnel — URL (groupe à un champ: écrire directement la valeur)
  - url* : texte — URL (URL vers lequel établir un lien (doit commencer par https:// ou http://))
- behaviour : groupe — Paramètres comportementaux (These options will let you control how the task behaves.)
  - codeColor : couleur #rrggbb, défaut #000000 — Couleur de code
  - backgroundColor : couleur #rrggbb, défaut #ffffff — Background color
  - maxSize : texte — Maximum size (Maximum size for the code given in CSS notation (pixels by default if only a number is given))
  - alignment : choix left|center|right, défaut center — Horizontal alignment (Set horizontal alignment if you set a maximum size)

Textes d'interface pré-remplis en français (ne pas fournir sauf besoin) : l10n, a11y.

## Exemple complet (validé : validateur officiel H5P + affichage)

Fichier `tests/examples/qr-code.md` (médias dans `tests/media/`).

````markdown
---
type: qr-code
title: QR code – ressource sur les fractions
language: fr
---
```yaml
introduction: |
  Scanne ce code avec ta tablette pour ouvrir la **fiche de révision sur les fractions**.
  Tu peux aussi cliquer dessus.
codeType: url
url: https://fr.wikipedia.org/wiki/Fraction_(math%C3%A9matiques)
behaviour:
  codeColor: "#1e3a8a"
  backgroundColor: "#ffffff"
  maxSize: 250px
  alignment: center
```
````
