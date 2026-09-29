# Question Set — `quiz`

H5P.QuestionSet 1.21 · alias : quiz, questionset, question-set · syntaxe Markdown simplifiée : oui

## Syntaxe Markdown

Introduction facultative (page d'accueil ; une première ligne `# Titre` devient son titre), puis une section `## <type>` par question, écrite avec la syntaxe de ce type : `qcm`, `vf` (ou `vf: faux`), `trous`, `glisser-mots`, `marquer-mots`, `redaction`, `choix-unique`. Pour les autres types (glisser-déposer…), écrire tout le quiz en bloc ```yaml.

```markdown
Révise les organites.

## qcm
Siège de la photosynthèse ?
- [x] Chloroplaste
- [ ] Noyau

## vf: faux
La mitochondrie contient de la chlorophylle.

## trous
L'ADN se trouve dans le {{noyau}}.
```

## Champs (bloc ```yaml, noms H5P)

`*` = obligatoire ; les autres champs ont une valeur par défaut ou sont facultatifs.

- introPage : groupe — Introduction du Quiz
  - showIntroPage : booléen — Afficher l'introduction
  - title : texte riche (Markdown: code em strong sub sup) — Titre
  - introduction : texte riche (Markdown: code em strong sub sup) — Texte d'introduction
  - startButtonText : texte, défaut Commencer — Texte du bouton de démarrage
  - backgroundImage : image (chemin ou URL) — Image d'arrière-plan
  - backgroundImageAltText : texte — Alternative text
- progressType : choix textual|dots, défaut dots — Indicateur de progression
- passPercentage : nombre, min 0, max 100, défaut 50 — Pourcentage de réussite
- questions* : liste (min 1) — Questions
  chaque élément = sous-contenu, library: qcm | glisser-deposer | trous | marquer-mots | glisser-mots | vf | redaction | choix-images — Type de question
- disableBackwardsNavigation : booléen, défaut false — Désactiver la possibilité de naviguer en arrière
- randomQuestions : booléen, défaut false — Afficher les questions dans un ordre aléatoire
- poolSize : nombre, min 1 — Nombre de questions à afficher :
- endGame : groupe — Quiz terminé
  - showResultPage : booléen, défaut true — Afficher les résultats
  - showSolutionButton : booléen, défaut true — Afficher le bouton "Solution".
  - showRetryButton : booléen, défaut true — Afficher le bouton "Recommencer".
  - noResultMessage : texte, défaut Terminé — Message si pas de résultats
  - message : texte riche (Markdown: code em strong), défaut Results — Results heading
  - amountCorrect : texte, défaut @finals of @totals correct — Amount correct heading
  - scoreBarLabel : texte, défaut Vous avez obtenu @finals sur … — Score announcer
  - scoreHeader : texte, défaut Score — Score heading
  - overallFeedback : groupe — Feedback général (groupe à un champ: écrire directement la valeur)
    - overallFeedback : liste (min 1) — Définir un retour personnalisé pour chaque tranche de score
      chaque élément :
        - from : nombre, min 0, max 100, défaut 0 — Tranche de score
        - to : nombre, min 0, max 100, défaut 100
        - feedback : texte — Retour pour cette tranche de score
  - solutionButtonText : texte, défaut Voir la solution — Texte du bouton "Solution"
  - retryButtonText : texte, défaut Recommencer — Texte du bouton "Recommencer"
  - finishButtonText : texte, défaut Terminer — Texte pour le bouton "Terminer"
  - submitButtonText : texte, défaut Soumettre — Submit button text
  - showAnimations : booléen — Afficher une vidéo avant l'affichage des résultats du quiz
  - skippable : booléen — Activer le bouton "Passer la vidéo"
  - skipButtonText : texte, défaut Passer la vidéo — Texte du bouton "Passer la vidéo"
  - successVideo : vidéo (URL YouTube/Vimeo, chemin ou URL) — Vidéo en cas de succès
  - failVideo : vidéo (URL YouTube/Vimeo, chemin ou URL) — Vidéo en cas d'échec
- override : groupe — Behavioural settings
  - checkButton : booléen, défaut true — Montrer les boutons "Vérifier"
  - showSolutionButton : choix on|off, conditionnel — Cacher le bouton "Voir la correction"
  - retryButton : choix on|off, conditionnel — Cacher le bouton "Recommencer"
  - backgroundImage : image (chemin ou URL) — Image d'arrière-plan

Textes d'interface pré-remplis en français (ne pas fournir sauf besoin) : texts.
