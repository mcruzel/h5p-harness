# KewAr Code — `qr-code`

H5P.KewArCode 1.7 · alias : qr-code, kewarcode, kew-ar-code · syntaxe Markdown simplifiée : non (bloc ```yaml)

## Champs (bloc ```yaml, noms H5P)

`*` = obligatoire ; les autres champs ont une valeur par défaut ou sont facultatifs.

- introduction : texte riche (Markdown: a code col colgroup del em figcaption figure h1 h2 h3 h4 h5 h6 hr li ol pre s strong sub sup table tbody td tfoot th thead tr u ul) — Introductory text
- codeType : choix contact|event|email|h5p|location|phone|sms|text|url, défaut url — Type de code
- contact : groupe, conditionnel — Contact
  - name* : texte — Name
  - organization : texte — Organization
  - title : texte — Title
  - number : texte — Phone number
  - email : texte — Email address
  - address : groupe — Address
    - extended : texte — Adresse complète
    - street : texte — Street
    - locality : texte — Locality
    - region : texte — Region
    - zip : texte — ZIP code
    - country : texte — Country
  - url : texte — Website
  - note : texte — Note
- event : groupe, conditionnel — Événement
  - title* : texte — Titre
  - allDay : booléen — Événement de toute une journée
  - dateStart* : texte — Date de début
  - timeStart : texte, conditionnel — Heure de début
  - dateEnd* : texte — Date de fin
  - timeEnd : texte, conditionnel — End time
  - timezone : choix -12:00|-11:00|-10:00|-9:30|-9:00|-8:00|-7:00|-6:00|-5:00|-4:00|…, défaut 0:00, conditionnel — Fuseau horaire
  - daylightSavings : booléen, conditionnel — L'heure d'été
  - location : texte — Location
  - description : texte — Description
- email : groupe, conditionnel — Email address (groupe à un champ: écrire directement la valeur)
  - email* : texte — Email address
- h5p : groupe, conditionnel — Contenu H5P (groupe à un champ: écrire directement la valeur)
  - contentTypes* : liste (min 1) — Content types
    chaque élément = sous-contenu, library: accordeon | calendrier-avent | agamotto | audio | enregistreur-audio | calcul-mental | trous | graphique | collage | colonne | mots-croises | presentation | cartes | dictee | outil-documentation | glisser-deposer | glisser-mots | redaction | mots-meles | flashcards | devinette | tableau | texte | iframe | image | choix-images | image-interactive | trouver-zone | avant-apres | paires-images | sequence-images | carrousel | livre | video-interactive | lien | marquer-mots | memory | qcm | questionnaire | quiz | choix-unique | trier-paragraphes | resume | frise | vf | video | visite-360 — Contenu H5P
- location : groupe, conditionnel — Emplacement
  - latitude* : texte — Latitude
  - longitude* : texte — Longitude
- phone : groupe, conditionnel — Numéro de téléphone (groupe à un champ: écrire directement la valeur)
  - number* : texte — Numéro de téléphone
- sms : groupe, conditionnel — SMS
  - number* : texte — Numéro de téléphone
  - message* : texte — Message
- text : groupe, conditionnel — Text (groupe à un champ: écrire directement la valeur)
  - text* : texte multiligne — Text
- url : groupe, conditionnel — URL (groupe à un champ: écrire directement la valeur)
  - url* : texte — URL
- behaviour : groupe — Paramètres comportementaux
  - codeColor : couleur #rrggbb, défaut #000000 — Couleur de code
  - backgroundColor : couleur #rrggbb, défaut #ffffff — Background color
  - maxSize : texte — Maximum size
  - alignment : choix left|center|right, défaut center — Horizontal alignment

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
