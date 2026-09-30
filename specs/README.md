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
  `H<sub>2</sub>O`) ; seules les balises indiquées dans la fiche sont conservées (sinon : retrait
  avec avertissement, H<sub>2</sub>O → H₂O, tableau → erreur hors conteneur).
- **texte simple** (champ « texte » de la fiche) : pas de Markdown, le texte est affiché tel quel.
- **YAML** : mettre entre guillemets tout texte contenant « : » suivi d'un espace (fréquent en
  français : `question: "Vrai ou faux : …"`), et, dans la notation `{…}` / `[…]`, tout texte
  contenant une virgule ; pour un texte sur plusieurs lignes, `champ: |` puis les lignes indentées.
  Seuls `12`, `-3`, `1.5` sont lus comme des nombres et `true`/`false` comme des booléens : `0472`,
  `1:20`, `yes`, `no` restent du texte tel qu'écrit. Durées : secondes ou `m:ss` (`1:30` = 90 s).
- **retours à la ligne** : un simple retour à la ligne dans un paragraphe est conservé (`<br>`) ;
  une ligne vide sépare les paragraphes.
- **média** (image, audio, vidéo, fichier) : chemin relatif au `.md` ou à la racine du dépôt, ou
  URL complète (téléchargée une fois dans `sources/.media/`) ; un chemin commençant par `/` part de
  la racine du dépôt ; forme longue `{src: …, license: CC BY-SA 4.0, author: …, title: …, source: …}`.
  Vidéo : lien YouTube/Vimeo accepté tel quel. WebP, BMP, TIFF sont convertis en PNG/JPG (Moodle
  les refuse) ; SVG seulement si le paquet Python `cairosvg` est installé, sinon fournir un PNG.
- **sous-contenu** : `library: <type>` plus ses champs au même niveau
  (ex. `{library: qcm, question: …, answers: […]}`), ou `library: <type>` + `md: |` + syntaxe
  Markdown du type ;
  `metadata: {title: …}` fixe son titre (sommaire d'un livre, bilan d'un quiz), sinon il est déduit
  du premier texte. Si le champ H5P s'appelle lui-même `library` (questionnaire), cela donne
  `library: {library: choix-simple, …}`.
- **groupe à un champ** : écrire directement la valeur (règle H5P).
- Les textes d'interface (boutons, messages, accessibilité) et les réglages ont des valeurs par
  défaut en français : ne les écrire que pour les modifier.

## Construire

```bash
python -m h5pharness build sources/mon-activite.md            # -> dist/mon-activite.h5p
python -m h5pharness build sources/mon-activite.md --publish  # + git add/commit/push
python -m h5pharness build sources/mon-activite.md --moodle 12 --as page   # + dépôt dans un Moodle local
python -m h5pharness spec qcm                                 # fiche d'un type
python -m h5pharness transcript video.vtt                     # transcrit d'une vidéo, en lignes m:ss
```

Dépôt Moodle : `--as activite` (activité H5P, défaut) ou `--as page` ; `--page "<nom>"` ajoute à une page
existante ; `--section <n>`, `--hidden`. Relancer met à jour la même activité. Sortie `MOODLE … : <url>`,
ou `ECHEC_MOODLE …` (code 2 : le paquet est bon, ne pas le régénérer).

Sortie : `OK <paquet>` (code 0), éventuellement suivi de lignes `piste:` (possibilités à proposer) ; `ERREUR` + au plus 8 lignes `- emplacement: problème` (code 1 :
corriger seulement ces points) ; code 2 = problème d'environnement (git, réseau) : ne pas
régénérer le contenu, signaler. Les emplacements comptent à partir de 0 (`answers[1]` = 2e réponse),
comme les références entre éléments (`correctElements`, `neighbors`, `nextContentId`).

## Types disponibles

Cible : Moodle 4.5 ou plus récent (API H5P 1.28). Colonne « exemple validé » : l'exemple complet du
type est dans `sources/exemples/<type>.md` (médias dans `sources/exemples/media/`).

<!-- index -->
| type | nom | bibliothèque | syntaxe | exemple validé |
|---|---|---|---|---|
| `chasse-ar` | AR Scavenger (beta) | H5P.ARScavenger 1.6 | yaml | ✓ |
| `accordeon` | Accordion | H5P.Accordion 1.0 | Markdown | ✓ |
| `trous-avances` | Advanced Fill in the Blanks | H5P.AdvancedBlanks 1.4 | Markdown | ✓ |
| `calendrier-avent` | Advent Calendar (beta) | H5P.AdventCalendar 0.4 | yaml | ✓ |
| `agamotto` | Agamotto | H5P.Agamotto 1.7 | Markdown | ✓ |
| `calcul-mental` | Arithmetic Quiz | H5P.ArithmeticQuiz 1.1 | yaml | ✓ |
| `audio` | Audio | H5P.Audio 1.5 | Markdown | ✓ |
| `enregistreur-audio` | Audio Recorder | H5P.AudioRecorder 1.0 | yaml | ✓ |
| `bingo` | Bingo | H5P.Bingo 0.3 | Markdown | ✓ |
| `trous` | Fill in the Blanks | H5P.Blanks 1.14 | Markdown | ✓ |
| `scenario` | Branching Scenario | H5P.BranchingScenario 1.11 | Markdown | ✓ |
| `graphique` | Chart | H5P.Chart 1.2 | Markdown | ✓ |
| `explorateur-choix` | ChoiceExplorer | H5P.ChoiceExplorer 1.0 | yaml | ✓ |
| `collage` | Collage | H5P.Collage 0.3 | yaml | ✓ |
| `colonne` | Page | H5P.Column 1.22 | Markdown | ✓ |
| `cadenas` | Combination Lock | H5P.CombinationLock 1.0 | yaml | ✓ |
| `cornell` | Cornell Notes | H5P.Cornell 0.5 | yaml | ✓ |
| `presentation` | Course Presentation | H5P.CoursePresentation 1.27 | Markdown | ✓ |
| `mots-croises` | Crossword | H5P.Crossword 0.7 | Markdown | ✓ |
| `cartes` | Dialog Cards | H5P.Dialogcards 1.9 | Markdown | ✓ |
| `dictee` | Dictation | H5P.Dictation 1.4 | Markdown | ✓ |
| `outil-documentation` | Documentation Tool | H5P.DocumentationTool 1.8 | yaml | ✓ |
| `glisser-deposer` | Drag and Drop | H5P.DragQuestion 1.15 | Markdown | ✓ |
| `glisser-mots` | Drag the Words | H5P.DragText 1.10 | Markdown | ✓ |
| `redaction` | Essay | H5P.Essay 1.6 | Markdown | ✓ |
| `mots-meles` | Find The Words | H5P.FindTheWords 1.4 | Markdown | ✓ |
| `flashcards` | Flashcards | H5P.Flashcards 1.7 | Markdown | ✓ |
| `carte-jeu` | Game Map | H5P.GameMap 1.9 | yaml | ✓ |
| `devinette` | Guess the Answer | H5P.GuessTheAnswer 1.5 | Markdown | ✓ |
| `iframe` | Iframe Embedder | H5P.IFrameEmbed 1.0 | yaml | ✓ |
| `trouver-zone` | Find the Hotspot | H5P.ImageHotspotQuestion 1.8 | yaml | ✓ |
| `image-interactive` | Image Hotspots | H5P.ImageHotspots 1.11 | Markdown | ✓ |
| `avant-apres` | Image Juxtaposition | H5P.ImageJuxtaposition 1.6 | Markdown | ✓ |
| `trouver-zones` | Find Multiple Hotspots | H5P.ImageMultipleHotspotQuestion 1.0 | yaml | ✓ |
| `paires-images` | Image Pair | H5P.ImagePair 1.4 | Markdown | ✓ |
| `sequence-images` | Image Sequencing | H5P.ImageSequencing 1.1 | Markdown | ✓ |
| `carrousel` | Image Slider | H5P.ImageSlider 1.1 | Markdown | ✓ |
| `mur-infos` | Information Wall | H5P.InfoWall 0.6 | yaml | ✓ |
| `livre` | Interactive Book | H5P.InteractiveBook 1.15 | Markdown | ✓ |
| `video-interactive` | Interactive Video | H5P.InteractiveVideo 1.28 | Markdown | ✓ |
| `qr-code` | KewAr Code | H5P.KewArCode 1.7 | yaml | ✓ |
| `marquer-lettres` | Mark the Letters | H5P.MarkTheLetters 1.1 | yaml | ✓ |
| `marquer-mots` | Mark the Words | H5P.MarkTheWords 1.11 | Markdown | ✓ |
| `memory` | Memory Game | H5P.MemoryGame 1.3 | Markdown | ✓ |
| `qcm` | Multiple Choice | H5P.MultiChoice 1.16 | Markdown | ✓ |
| `choix-images` | Multimedia Choice | H5P.MultiMediaChoice 0.3 | Markdown | ✓ |
| `quiz-personnalite` | Personality Quiz | H5P.PersonalityQuiz 1.0 | Markdown | ✓ |
| `quiz` | Question Set | H5P.QuestionSet 1.21 | Markdown | ✓ |
| `questionnaire` | Questionnaire | H5P.Questionnaire 1.3 | yaml | ✓ |
| `choix-unique` | Single Choice Set | H5P.SingleChoiceSet 1.11 | Markdown | ✓ |
| `trier-paragraphes` | Sort the Paragraphs | H5P.SortParagraphs 0.12 | Markdown | ✓ |
| `dire-mots` | Speak the Words | H5P.SpeakTheWords 1.5 | yaml | ✓ |
| `dire-mots-serie` | Speak the Words Set | H5P.SpeakTheWordsSet 1.3 | yaml | ✓ |
| `bande-structure` | Structure Strip | H5P.StructureStrip 1.1 | yaml | ✓ |
| `resume` | Summary | H5P.Summary 1.10 | Markdown | ✓ |
| `onglets` | Tabs | H5P.Tabs 1.3 | Markdown | ✓ |
| `modele-3d` | 3D Model | H5P.ThreeDModel 1.0 | yaml | ✓ |
| `visite-360` | Virtual Tour (360) | H5P.ThreeImage 0.5 | yaml | ✓ |
| `frise` | Timeline | H5P.Timeline 1.1 | Markdown | ✓ |
| `transcription` | Transcript | H5P.Transcript 1.3 | yaml | ✓ |
| `vf` | True/False Question | H5P.TrueFalse 1.8 | Markdown | ✓ |
| `twitter` | Twitter User Feed ⚠ obsolète | H5P.TwitterUserFeed 1.0 | yaml | ✓ |
| `rayons-x` | X-Ray | H5P.XRay 0.1 | yaml | ✓ |
