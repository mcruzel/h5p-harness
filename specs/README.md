# Écrire une activité H5P (format source)

Une activité = un fichier `.md` dans `sources/` : un **en-tête YAML** puis un **corps**.

```markdown
---
type: qcm                 # obligatoire : alias du type (colonne « type » ci-dessous)
title: Titre du paquet    # obligatoire
language: fr              # facultatif (fr par défaut)
preset: entrainement      # facultatif : entrainement | evaluation | decouverte
license: CC BY-SA 4.0     # facultatif : CC BY, CC BY-SA, CC BY-NC-SA, CC0, PD, C, U…
authors: Nom Prénom       # facultatif
---
Corps : syntaxe Markdown simplifiée du type (si elle existe) et/ou un bloc ```yaml de champs.
```

## Deux façons d'écrire le corps (combinables)

1. **Markdown simplifié** — disponible pour les types marqués « Markdown » dans le tableau ; la
   syntaxe est décrite en tête de chaque fiche.
2. **Bloc ```yaml** — possible pour **tous** les types : les clés sont les noms de champs H5P de la
   fiche du type. Un bloc yaml s'ajoute au Markdown simplifié et le complète ou le remplace champ
   par champ (ex. `behaviour: {randomAnswers: false}`).

Règles communes aux champs :

- **texte riche** : écrire du Markdown (gras, italique, listes, titres `##`, liens, tableaux,
  `H<sub>2</sub>O`) ; seules les balises indiquées dans la fiche sont conservées.
- **média** (image, audio, vidéo, fichier) : chemin relatif au `.md` ou à la racine du dépôt, ou
  URL complète (téléchargée une fois dans `sources/.media/`) ; forme longue
  `{src: …, license: CC BY-SA 4.0, author: …, title: …, source: …}`. Vidéo : lien YouTube/Vimeo
  accepté tel quel. SVG et WebP sont convertis (Moodle les refuse).
- **sous-contenu** : `library: <type>` plus ses champs au même niveau
  (ex. `{library: qcm, question: …, answers: […]}`), ou `md: |` + syntaxe Markdown du type.
- **groupe à un champ** : écrire directement la valeur (règle H5P).
- Les textes d'interface (boutons, messages, accessibilité) et les réglages ont des valeurs par
  défaut en français : ne les écrire que pour les modifier.

## Construire

```bash
python -m h5pharness build sources/mon-activite.md            # -> dist/mon-activite.h5p
python -m h5pharness build sources/mon-activite.md --publish  # + git add/commit/push
python -m h5pharness spec qcm                                 # fiche d'un type
```

Sortie : `OK <paquet>` (code 0) ; `ERREUR` + au plus 8 lignes `- emplacement: problème` (code 1 :
corriger seulement ces points) ; code 2 = problème d'environnement (git, réseau) : ne pas
régénérer le contenu, signaler. Les emplacements comptent à partir de 1 (`answers[2]` = 2e réponse).

## Types disponibles

Cible : Moodle 4.5 ou plus récent (API H5P 1.28).

<!-- index -->
| type | nom | bibliothèque | syntaxe |
|---|---|---|---|
| `chasse-ar` | AR Scavenger (beta) | H5P.ARScavenger 1.6 | yaml |
| `accordeon` | Accordion | H5P.Accordion 1.0 | Markdown |
| `trous-avances` | Advanced Fill in the Blanks | H5P.AdvancedBlanks 1.4 | yaml |
| `calendrier-avent` | Advent Calendar (beta) | H5P.AdventCalendar 0.4 | yaml |
| `agamotto` | Agamotto | H5P.Agamotto 1.7 | yaml |
| `calcul-mental` | Arithmetic Quiz | H5P.ArithmeticQuiz 1.1 | yaml |
| `audio` | Audio | H5P.Audio 1.5 | Markdown |
| `enregistreur-audio` | Audio Recorder | H5P.AudioRecorder 1.0 | yaml |
| `trous` | Fill in the Blanks | H5P.Blanks 1.14 | Markdown |
| `scenario` | Branching Scenario | H5P.BranchingScenario 1.11 | yaml |
| `graphique` | Chart | H5P.Chart 1.2 | yaml |
| `explorateur-choix` | ChoiceExplorer | H5P.ChoiceExplorer 1.0 | yaml |
| `collage` | Collage | H5P.Collage 0.3 | yaml |
| `colonne` | Page | H5P.Column 1.22 | Markdown |
| `cadenas` | Combination Lock | H5P.CombinationLock 1.0 | yaml |
| `cornell` | Cornell Notes | H5P.Cornell 0.5 | yaml |
| `presentation` | Course Presentation | H5P.CoursePresentation 1.27 | Markdown |
| `mots-croises` | Crossword | H5P.Crossword 0.7 | Markdown |
| `cartes` | Dialog Cards | H5P.Dialogcards 1.9 | Markdown |
| `dictee` | Dictation | H5P.Dictation 1.4 | yaml |
| `outil-documentation` | Documentation Tool | H5P.DocumentationTool 1.8 | yaml |
| `glisser-deposer` | Drag and Drop | H5P.DragQuestion 1.15 | yaml |
| `glisser-mots` | Drag the Words | H5P.DragText 1.10 | Markdown |
| `redaction` | Essay | H5P.Essay 1.6 | Markdown |
| `mots-meles` | Find The Words | H5P.FindTheWords 1.4 | Markdown |
| `flashcards` | Flashcards | H5P.Flashcards 1.7 | Markdown |
| `carte-jeu` | Game Map | H5P.GameMap 1.9 | yaml |
| `devinette` | Guess the Answer | H5P.GuessTheAnswer 1.5 | yaml |
| `iframe` | Iframe Embedder | H5P.IFrameEmbed 1.0 | yaml |
| `trouver-zone` | Find the Hotspot | H5P.ImageHotspotQuestion 1.8 | yaml |
| `image-interactive` | Image Hotspots | H5P.ImageHotspots 1.11 | yaml |
| `avant-apres` | Image Juxtaposition | H5P.ImageJuxtaposition 1.6 | yaml |
| `trouver-zones` | Find Multiple Hotspots | H5P.ImageMultipleHotspotQuestion 1.0 | yaml |
| `paires-images` | Image Pair | H5P.ImagePair 1.4 | yaml |
| `sequence-images` | Image Sequencing | H5P.ImageSequencing 1.1 | yaml |
| `carrousel` | Image Slider | H5P.ImageSlider 1.1 | Markdown |
| `mur-infos` | Information Wall | H5P.InfoWall 0.6 | yaml |
| `livre` | Interactive Book | H5P.InteractiveBook 1.15 | Markdown |
| `video-interactive` | Interactive Video | H5P.InteractiveVideo 1.28 | Markdown |
| `qr-code` | KewAr Code | H5P.KewArCode 1.7 | yaml |
| `marquer-lettres` | Mark the Letters | H5P.MarkTheLetters 1.1 | yaml |
| `marquer-mots` | Mark the Words | H5P.MarkTheWords 1.11 | Markdown |
| `memory` | Memory Game | H5P.MemoryGame 1.3 | Markdown |
| `qcm` | Multiple Choice | H5P.MultiChoice 1.16 | Markdown |
| `choix-images` | Multimedia Choice | H5P.MultiMediaChoice 0.3 | yaml |
| `quiz` | Question Set | H5P.QuestionSet 1.21 | Markdown |
| `questionnaire` | Questionnaire | H5P.Questionnaire 1.3 | yaml |
| `choix-unique` | Single Choice Set | H5P.SingleChoiceSet 1.11 | Markdown |
| `trier-paragraphes` | Sort the Paragraphs | H5P.SortParagraphs 0.12 | Markdown |
| `dire-mots` | Speak the Words | H5P.SpeakTheWords 1.5 | yaml |
| `dire-mots-serie` | Speak the Words Set | H5P.SpeakTheWordsSet 1.3 | yaml |
| `bande-structure` | Structure Strip | H5P.StructureStrip 1.1 | yaml |
| `resume` | Summary | H5P.Summary 1.10 | Markdown |
| `onglets` | Tabs | H5P.Tabs 1.3 | yaml |
| `modele-3d` | 3D Model | H5P.ThreeDModel 1.0 | yaml |
| `visite-360` | Virtual Tour (360) | H5P.ThreeImage 0.5 | yaml |
| `frise` | Timeline | H5P.Timeline 1.1 | yaml |
| `transcription` | Transcript | H5P.Transcript 1.3 | yaml |
| `vf` | True/False Question | H5P.TrueFalse 1.8 | Markdown |
| `twitter` | Twitter User Feed | H5P.TwitterUserFeed 1.0 | yaml |
| `rayons-x` | X-Ray | H5P.XRay 0.1 | yaml |
