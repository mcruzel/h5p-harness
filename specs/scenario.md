# Branching Scenario — `scenario`

H5P.BranchingScenario 1.11 · alias : scenario, scenario-a-embranchements, branchingscenario, branching-scenario · syntaxe Markdown simplifiée : oui

## Syntaxe Markdown

Nœuds **nommés** (plus d'indices à gérer). `# Titre` et sous-titre (+ image facultative) pour l'écran d'accueil, puis :
- nœud de contenu `## identifiant` : texte Markdown, **ou** une image/vidéo `![…](…)`, **ou** un bloc `::: type` … `:::` ; ligne `→ identifiant` pour la suite (par défaut : le nœud suivant), `→ fin` ou `→ fin: Titre de fin (score)` pour terminer ;
- nœud question `## identifiant ? Question posée` : choix `- texte → identifiant` (ou `→ fin: …`), retour facultatif en ligne indentée `> …`.

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

`*` = obligatoire ; les autres champs ont une valeur par défaut ou sont facultatifs.

- branchingScenario : groupe — Éditeur de scénario
  - title* : texte — Titre
  - startScreen : groupe — Écran de départ
    - startScreenTitle : texte riche (Markdown: a code del em s strong) — Titre de l’écran d'accueil
    - startScreenSubtitle : texte riche (Markdown: a code del em s strong) — Sous-titre de l’écran d'accueil
    - startScreenImage : image (chemin ou URL) — Image de l’écran d'accueil
    - startScreenAltText : texte — Texte alternatif pour l'image
  - endScreens : liste — Liste des écrans de fin
    chaque élément :
      - endScreenTitle : texte riche (Markdown: a code del em s strong) — Titre
      - endScreenSubtitle : texte riche (Markdown: a code del em s strong) — Texte
      - endScreenImage : image (chemin ou URL) — Image
      - endScreenScore : nombre, défaut 0 — Score (Le score sera envoyé à tout LMS, LRS ou tout autre service qui reçoit des résultats depuis H5P pour des utili…)
  - content* : liste (min 1) — Liste de contenus de scénario de branchement
    chaque élément :
      - type* : sous-contenu, library: question-embranchement | presentation | texte | image | image-interactive | video-interactive | video
      - showContentTitle : booléen — Voir le titre du contenu dans la vue (Si sélectionné, l'utilisateur verra le titre du contenu dans la barre supérieure en haut de ce contenu)
      - proceedButtonText : texte, défaut Continuer — Text for the proceed button (max length: 50 characters)
      - forceContentFinished : choix useBehavioural|enabled|disabled, défaut useBehavioural — Identifiant de contenu suivant (les écrans de fin sont définis par de… (Contourner les options personnelles exigeant la complétion du contenu avant d’activer le bouton « Continuer »…)
      - feedback : groupe — Feedback
        - title : texte riche (Markdown: a code del em s strong) — Feedback title
        - subtitle : texte riche (Markdown: a code del em s strong) — Feedback text
        - image : image (chemin ou URL) — Feedback image
        - endScreenScore : nombre — Score for this scenario (The score will be sent to any LMS, LRS or any other connected service that receives scores from H5P for users…)
      - contentBehaviour : choix useBehavioural|enabled|disabled, défaut useBehavioural — Navigate back (This will allow the user to go back and see the previous content/question in the scenario.)
  - scoringOptionGroup : réglages — Options de notation
    scoringOption=no-score (static-end-score|dynamic-scor…, includeInteractionsScores=true
  - behaviour : réglages — Options comportementales
    enableBackwardsNavigation=false, forceContentFinished=false, randomizeBranchingQuestions=false

Textes d'interface pré-remplis en français (ne pas fournir sauf besoin) : l10n.

## Exemple complet (validé : validateur officiel H5P + affichage)

Fichier `tests/examples/scenario.md` (médias dans `tests/media/`).

````markdown
---
type: scenario
title: Accident au labo de chimie – scénario
language: fr
---
```yaml
branchingScenario:
  title: Accident au labo de chimie
  startScreen:
    startScreenTitle: Accident au labo de chimie
    startScreenSubtitle: Fais les bons choix pour garder tout le monde en sécurité.
    startScreenImage: ../media/paysage.jpg
    startScreenAltText: Illustration
  endScreens:
    - endScreenTitle: Fin du scénario
      endScreenSubtitle: Retiens les **règles de sécurité** au laboratoire.
      endScreenScore: 0
      contentId: -1
  content:
    # 1 (id 0)
    - type:
        library: texte
        text: |
          ## La situation
          En TP de chimie, ton voisin renverse un flacon d'**acide chlorhydrique dilué**
          sur la paillasse. Quelques gouttes tombent sur sa blouse.
      nextContentId: 1
    # 2 (id 1)
    - type:
        library: question-embranchement
        branchingQuestion:
          question: Que fais-tu **en premier** ?
          alternatives:
            - text: Je préviens immédiatement le professeur.
              nextContentId: 2
              feedback:
                title: Bon réflexe !
            - text: J'essuie tout de suite avec mon mouchoir.
              nextContentId: 3
    # 3 (id 2)
    - type:
        library: image
        file: ../media/etoile-orange.png
        alt: Une étoile orange, symbole de réussite
      nextContentId: -1
      feedback:
        title: Bravo
        subtitle: Le professeur sécurise la zone et fait rincer la blouse à l'eau.
    # 4 (id 3)
    - type:
        library: texte
        text: |
          ## Mauvaise idée !
          On ne touche **jamais** un produit chimique à mains nues.
          Il faut d'abord prévenir l'adulte responsable.
      nextContentId: 1
```
````
