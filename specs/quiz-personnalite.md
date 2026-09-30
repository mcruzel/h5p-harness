# Personality Quiz — `quiz-personnalite`

H5P.PersonalityQuiz 1.0 · alias : quiz-personnalite, test-personnalite, personalityquiz, personality-quiz · syntaxe Markdown simplifiée : oui

## Syntaxe Markdown

`# Titre` (+ image facultative), puis des sections `## Profil : Nom` (description sur les lignes suivantes, image facultative) et des sections `## Question` suivies de réponses `- texte → Profil` (plusieurs profils séparés par des virgules). Au moins 2 profils ; le résultat est le profil le plus choisi.

```markdown
# Quel scientifique es-tu ?

## Profil : Explorateur
Tu aimes le terrain et les expéditions.

## Profil : Théoricien
Tu aimes les idées et les modèles.

## Un samedi libre, tu préfères…
- une randonnée → Explorateur
- une énigme de logique → Théoricien
```

## Champs (bloc ```yaml, noms H5P)

`*` = obligatoire ; les autres champs ont une valeur par défaut ou sont facultatifs. Libellés et descriptions : ceux de la bibliothèque (anglais) ; valeurs par défaut : en français.

- titleScreen : groupe — Title Screen
  - title : groupe — Title
    - text* : texte — Title
    - display : booléen, défaut true — Display Title (Wether or not to show the title as a headline at the start of the personality quiz.)
  - image : groupe — Optional: Image
    - file : image (chemin ou URL) — File
    - alt : texte — Alt text (Alternative text if the browser is unable to load the image.)
  - skip : booléen, défaut false — Skip (Select if you want the quiz to start on the first question instead of the title screen.)
- resultScreen : réglages — Result screen
  animation=none (none|fade-in|wheel), displayTitle=true, displayDescription=true, imagePosition=background (background|inline)
- personalities* : liste (min 2, max 10) — Personality
  chaque élément :
    - name* : texte — Personality name (The personality name will be used to associate answers with their respective personalities.)
    - description* : texte multiligne — Description
    - image : groupe — Optional: Image
      - file : image (chemin ou URL) — Image (An image to display on the result screen.)
      - alt : texte — Alt text (Alternative text if the browser is unable to load the image.)
- questions : liste — Questions
  chaque élément :
    - text* : texte — Question
    - image : groupe — Optional: Image (Image displayed at the top of the screen above or below the question text.)
      - file : image (chemin ou URL) — File
      - alt : texte — Alt text (Alternative text if the browser is unable to load the image.)
    - answers* : liste (min 2, max 6) — Answers
      chaque élément :
        - text* : texte — text
        - personality* : texte — Personalities (A comma separated list of personality names associated with this answer.)
        - image : groupe — Optional: Image (Images associated with answers will not show up unless all answers associated with a question has an image attached.)
          - file : image (chemin ou URL) — File
          - alt : texte — Alt text (Alternative text if the browser is unable to load the image.)
- startText : texte, défaut Commencer — Start (Text displayed on the start quiz button on the title card.)
- progressText : texte, défaut Question @question sur @total — Progress text (Progress text, variables available: @question and @total. Example: '@question of @total')
- retakeText : texte, défaut Recommencer le quiz — Retake (Retake text)
- animation : booléen, défaut true — Animation (Uncheck to turn off all animation)
- buttonColor : couleur #rrggbb, défaut 4D5DAA — Button Accent (Change the color of the button borders and the animation color fill)
- progressbarColor : couleur #rrggbb, défaut 38B755 — Progressbar Color (Determines the color of the progress bar)

## Exemple complet (validé : validateur officiel H5P + affichage)

Fichier `sources/exemples/quiz-personnalite.md` (médias dans `sources/exemples/media/`).

```markdown
---
type: quiz-personnalite
title: Quel scientifique es-tu ?
language: fr
---
# Quel scientifique es-tu ?
![Paysage à explorer](media/paysage.jpg)

## Profil : Explorateur
Tu aimes le terrain, les expéditions et les découvertes au grand air : la géologie ou l'écologie t'attendent.
![Un triangle vert](media/triangle-vert.png)

## Profil : Expérimentateur
Tu veux comprendre en manipulant : le laboratoire de chimie ou de physique est fait pour toi.

## Profil : Théoricien
Tu aimes les idées, les calculs et les modèles : les mathématiques et la physique théorique te plairont.

## Un samedi libre, tu préfères…
- une randonnée pour observer les oiseaux → Explorateur
- construire une fusée à eau → Expérimentateur
- résoudre une énigme de logique → Théoricien

## Dans un musée, tu files vers…
- la salle des fossiles → Explorateur
- les manipulations interactives → Expérimentateur
- la salle des grandes équations → Théoricien
- la boutique de minéraux → Explorateur, Expérimentateur
```
