# KewAr Code — `qr-code`

H5P.KewArCode 1.7 · alias : qr-code, kewarcode, kew-ar-code · syntaxe Markdown simplifiée : non (bloc ```yaml)

## Champs (bloc ```yaml, noms H5P)

`*` = obligatoire ; les autres champs ont une valeur par défaut ou sont facultatifs. Libellés et descriptions : ceux de la bibliothèque (anglais) ; valeurs par défaut : en français.

- introduction : texte riche (Markdown: a code col colgroup del em figcaption figure h1 h2 h3 h4 h5 h6 hr li ol pre s strong sub sup table tbody td tfoot th thead tr u ul) — Introductory text (This text can optionally be presented along with your code.)
- codeType : choix contact|event|email|h5p|location|phone|sms|text|url, défaut url — Code type (Select what kind of code you want to generate)
- contact : groupe, si codeType = contact — Contact
  - name* : texte — Name
  - organization : texte — Organization
  - title : texte — Title
  - number : texte — Phone number (Phone number (please use the format +12 345 67890))
  - email : texte — Email address (Email address to write message to)
  - address : groupe — Address
    - extended : texte — Extended address (c/o information, etc.)
    - street : texte — Street (Street including number)
    - locality : texte — Locality (City name, etc.)
    - region : texte — Region (Federal state, county, etc.)
    - zip : texte — ZIP code
    - country : texte — Country
  - url : texte — Website (Website to link to (must start with https:// or http://))
  - note : texte — Note
- event : groupe, si codeType = event — Event
  - title* : texte — Title (Title for the calendar event)
  - allDay : booléen — All day event (Check if event will be valid all day long)
  - dateStart* : texte — Start date (Start date of the event (please use the format yyyy/mm/dd))
  - timeStart : texte, si allDay = False — Start time (Start time of the event (please use the format hh:mm))
  - dateEnd* : texte — End date (End date of the event (please use the format yyyy/mm/dd))
  - timeEnd : texte, si allDay = False — End time (End time of the event (please use the format hh:mm))
  - timezone : choix -12:00|-11:00|-10:00|-9:30|-9:00|-8:00|-7:00|-6:00|-5:00|-4:00|…, défaut 0:00, si allDay = False — Timezone (Select the time zone the event is supposed to take place in)
  - daylightSavings : booléen, si allDay = False — Daylight savings (Check if location that the event is taking place in uses daylight savings time)
  - location : texte — Location (Name the location)
  - description : texte — Description (Add a description for the event)
- email : groupe, si codeType = email — Email address (groupe à un champ: écrire directement la valeur)
  - email* : texte — Email address (Email address to write message to)
- h5p : groupe, si codeType = h5p — H5P content (groupe à un champ: écrire directement la valeur)
  - contentTypes* : liste (min 1) — Content types (Select the H5P content type that you want to display. If you select more than one, one will be picked randomly when scanning the code.)
    chaque élément = sous-contenu, library: accordeon | calendrier-avent | agamotto | audio | enregistreur-audio | calcul-mental | trous | graphique | collage | colonne | mots-croises | presentation | cartes | dictee | outil-documentation | glisser-deposer | glisser-mots | redaction | mots-meles | flashcards | devinette | tableau | texte | iframe | image | choix-images | image-interactive | trouver-zone | avant-apres | paires-images | sequence-images | carrousel | livre | video-interactive | lien | marquer-mots | memory | qcm | questionnaire | quiz | choix-unique | trier-paragraphes | resume | frise | vf | video | visite-360 — H5P content (H5P content to display)
- location : groupe, si codeType = location — Location
  - latitude* : texte — Latitude (Latitude (please use the format 53.864462))
  - longitude* : texte — Longitude (Longitude (please use the format 10.663792))
- phone : groupe, si codeType = phone — Phone number (groupe à un champ: écrire directement la valeur)
  - number* : texte — Phone number (Phone number to call (please use the format +12 345 67890))
- sms : groupe, si codeType = sms — SMS
  - number* : texte — Phone number (Phone number to send to (please use the format +12 345 67890))
  - message* : texte — Message (Message to send)
- text : groupe, si codeType = text — Text (groupe à un champ: écrire directement la valeur)
  - text* : texte multiligne — Text (Text to encode)
- url : groupe, si codeType = url — URL (groupe à un champ: écrire directement la valeur)
  - url* : texte — URL (URL to link to (must start with https:// or http://))
- behaviour : groupe — Behavioural settings (These options will let you control how the task behaves.)
  - codeColor : couleur #rrggbb, défaut #000000 — Code color
  - backgroundColor : couleur #rrggbb, défaut #ffffff — Background color
  - maxSize : texte — Maximum size (Maximum size for the code given in CSS notation (pixels by default if only a number is given))
  - alignment : choix left|center|right, défaut center — Horizontal alignment (Set horizontal alignment if you set a maximum size)

Textes d'interface pré-remplis en français (ne pas fournir sauf besoin) : l10n, a11y.

## Exemple complet (validé : validateur officiel H5P + affichage)

Fichier `sources/exemples/qr-code.md` (médias dans `sources/exemples/media/`).

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
