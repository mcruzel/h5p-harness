# Branching Scenario — `scenario`

H5P.BranchingScenario 1.11 · alias : scenario, scenario-a-embranchements, branchingscenario, branching-scenario · syntaxe Markdown simplifiée : non (bloc ```yaml)

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
      - endScreenScore : nombre, défaut 0 — Score
  - content* : liste (min 1) — Liste de contenus de scénario de branchement
    chaque élément :
      - type* : sous-contenu, library: question-embranchement | presentation | texte | image | image-interactive | video-interactive | video
      - showContentTitle : booléen — Voir le titre du contenu dans la vue
      - proceedButtonText : texte, défaut Proceed — Text for the proceed button (max length: 50 characters)
      - forceContentFinished : choix useBehavioural|enabled|disabled, défaut useBehavioural — Identifiant de contenu suivant (les écrans de fin sont définis par de…
      - feedback : groupe — Feedback
        - title : texte riche (Markdown: a code del em s strong) — Feedback title
        - subtitle : texte riche (Markdown: a code del em s strong) — Feedback text
        - image : image (chemin ou URL) — Feedback image
        - endScreenScore : nombre — Score for this scenario
      - contentBehaviour : choix useBehavioural|enabled|disabled, défaut useBehavioural — Navigate back
  - scoringOptionGroup : réglages — Options de notation
    scoringOption=no-score (static-end-score|dynamic-scor…, includeInteractionsScores=true
  - behaviour : réglages — Options comportementales
    enableBackwardsNavigation=false, forceContentFinished=false, randomizeBranchingQuestions=false

Textes d'interface pré-remplis en français (ne pas fournir sauf besoin) : l10n.
