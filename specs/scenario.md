# Branching Scenario — `scenario`

H5P.BranchingScenario 1.11 · alias : scenario, scenario-a-embranchements, branchingscenario, branching-scenario · syntaxe Markdown simplifiée : oui

## Syntaxe Markdown

Nœuds **nommés** (plus d'indices à gérer). `# Titre` et sous-titre (+ image facultative) pour l'écran d'accueil, puis :
- nœud de contenu `## identifiant` : texte Markdown, **ou** une image/vidéo `![…](…)`, **ou** un bloc `::: type` … `:::` ; ligne `→ identifiant` pour la suite (par défaut : le nœud suivant), `→ fin` ou `→ fin: Titre de fin (score)` pour terminer ;
- nœud question `## identifiant ? Question posée` : choix `- texte → identifiant` (ou `→ fin: …`), retour facultatif en ligne indentée `> …`.

En YAML, `nextContentId` est l'indice du contenu suivant dans `content` (0 = premier, -1 = écran de fin) ; absent, c'est le contenu suivant.

```markdown
# Accident au labo de chimie
Fais les bons choix pour la sécurité de tous.

## situation
Ton voisin renverse un flacon d'acide sur la paillasse.
→ choix

## choix ? Que fais-tu en premier ?
- Je préviens le professeur → bravo
  > Bon réflexe !
- J'essuie avec mon mouchoir → erreur

## bravo
Le professeur sécurise la zone.
→ fin: Bravo ! (10)

## erreur
On ne touche jamais un produit chimique à mains nues.
→ choix
```

## Champs (bloc ```yaml, noms H5P)

`*` = obligatoire ; les autres champs ont une valeur par défaut ou sont facultatifs. Libellés et descriptions : ceux de la bibliothèque (anglais) ; valeurs par défaut : en français.

- branchingScenario : groupe — Branching Scenario Editor
  - title* : texte — Title
  - startScreen : groupe — Start screen
    - startScreenTitle : texte riche (Markdown: a code del em s strong) — Course Title
    - startScreenSubtitle : texte riche (Markdown: a code del em s strong) — Course Details
    - startScreenImage : image (chemin ou URL) — Course image
    - startScreenAltText : texte — Image alternative text
  - endScreens : liste — List of end screens
    chaque élément :
      - endScreenTitle : texte riche (Markdown: a code del em s strong) — Title
      - endScreenSubtitle : texte riche (Markdown: a code del em s strong) — Text
      - endScreenImage : image (chemin ou URL) — Image
      - endScreenScore : nombre, défaut 0 — Score (The score will be sent to any LMS, LRS or any other connected service that receives scores from H5P for users who reach the default end scenario.)
      - contentId : nombre, facultatif — laisser -1 (défaut)
  - content* : liste (min 1) — List of branching scenario content
    chaque élément :
      - type* : sous-contenu, library: question-embranchement | presentation | texte | image | image-interactive | video-interactive | video
      - showContentTitle : booléen — Show content title in view (If selected, the user will see the content title in the top bar above this content.)
      - proceedButtonText : texte, défaut Continuer — Text for the proceed button (max length: 50 characters)
      - forceContentFinished : choix useBehavioural|enabled|disabled, défaut useBehavioural — Override require content finished (Override the individual settings for requiring the content to be finished before activating the "Proceed" button. Will not have any effect if the content doesn't indicate if it was "finished", e.g. images or course pres…)
      - nextContentId : nombre, facultatif — indice du contenu suivant dans `content` (0 = premier), -1 = écran de fin ; défaut : le contenu suivant (-1 pour le dernier)
      - feedback : groupe — Feedback
        - title : texte riche (Markdown: a code del em s strong) — Feedback title
        - subtitle : texte riche (Markdown: a code del em s strong) — Feedback text
        - image : image (chemin ou URL) — Feedback image
        - endScreenScore : nombre — Score for this scenario (The score will be sent to any LMS, LRS or any other connected service that receives scores from H5P for users who reach this scenario)
      - contentBehaviour : choix useBehavioural|enabled|disabled, défaut useBehavioural — Navigate back (This will allow user to go back and see the previous content/question in the scenario.)
  - scoringOptionGroup : réglages — Scoring options
    scoringOption=no-score (static-end-score|dynamic-scor…, includeInteractionsScores=true
  - behaviour : réglages — Behavioural settings
    enableBackwardsNavigation=false, forceContentFinished=false, randomizeBranchingQuestions=false

Textes d'interface pré-remplis en français (ne pas fournir sauf besoin) : l10n.

## Exemple complet (validé : validateur officiel H5P + affichage)

Fichier `tests/examples/scenario.md` (médias dans `tests/media/`).

```markdown
---
type: scenario
title: Accident au labo de chimie – scénario
language: fr
---
# Accident au labo de chimie
Fais les bons choix pour garder tout le monde en sécurité.
![Illustration](../media/paysage.jpg)

## situation
**La situation.** En TP de chimie, ton voisin renverse un flacon d'**acide chlorhydrique dilué**
sur la paillasse. Quelques gouttes tombent sur sa blouse.
→ choix

## choix ? Que fais-tu en premier ?
- Je préviens immédiatement le professeur. → bravo
  > Bon réflexe !
- J'essuie tout de suite avec mon mouchoir. → erreur

## bravo
![Une étoile orange, symbole de réussite](../media/etoile-orange.png)
→ fin: Bravo, le professeur sécurise la zone et fait rincer la blouse. (10)

## erreur
**Mauvaise idée !** On ne touche **jamais** un produit chimique à mains nues.
Il faut d'abord prévenir l'adulte responsable.
→ choix
```

Même activité entièrement en YAML (positions explicites) : `tests/examples/scenario.yaml.md`.
