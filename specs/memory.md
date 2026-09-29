# Memory Game — `memory`

H5P.MemoryGame 1.3 · alias : memory, memorygame, memory-game · syntaxe Markdown simplifiée : oui

## Syntaxe Markdown

Une carte par ligne : `- ![description](image)` (paire identique) ou `- ![a](image1) = ![b](image2)` (paire de deux images différentes). Suffixe optionnel ` :: texte` affiché quand la paire est trouvée.

```markdown
- ![Chat](images/chat.jpg)
- ![Chien](images/chien.jpg) = ![Niche](images/niche.jpg) :: Le chien et sa niche
```

## Champs (bloc ```yaml, noms H5P)

`*` = obligatoire ; les autres champs ont une valeur par défaut ou sont facultatifs.

- cards* : liste (min 2, max 100) — Cartes
  chaque élément :
    - image : image (chemin ou URL) — Image
    - imageAlt* : texte — Texte alternatif pour l'image (Décrivez ce que représente l'image. Le texte est lu par la synthèse vocale.)
    - audio : audio (chemin ou URL) — Audio Track (An optional sound that plays when the card is turned.)
    - match : image (chemin ou URL) — Image correspondante (Une image facultative à comparer au lieu d'utiliser deux cartes avec la même image.)
    - matchAlt : texte — Texte alternatif pour l'image correspondante (Décrivez ce que représente l'image correspondante. Le texte est lu par la synthèse vocale.)
    - matchAudio : audio (chemin ou URL) — Matching Audio Track (An optional sound that plays when the second card is turned.)
    - description : texte — Description (Un texte court optionnel qui apparaîtra une fois que les deux cartes correspondantes auront été trouvées.)
- behaviour : réglages — Paramètres comportementaux (Ces options vous permettent de définir le "comportement" du jeu de mémoire.)
  useGrid=true, numCardsToUse=…, allowRetry=true
- lookNFeel : groupe — Apparence (Définissez l'apparence visuelle des éléments dans le jeu.)
  - themeColor : couleur #rrggbb, défaut #707070 — Couleur du thème (Choisissez une couleur pour créer un thème pour votre jeu de cartes.)
  - cardBack : image (chemin ou URL) — Dos des cartes (Utilisez un dos personnalisé pour vos cartes.)

Textes d'interface pré-remplis en français (ne pas fournir sauf besoin) : l10n.

## Exemple complet (validé : validateur officiel H5P + affichage)

Fichier `tests/examples/memory.md` (médias dans `tests/media/`).

````markdown
---
type: memory
title: Memory des figures géométriques
language: fr
preset: entrainement
license: CC BY-SA 4.0
authors: Équipe de mathématiques
---
Retrouve les paires de figures. Chaque paire trouvée rappelle une propriété de la figure.

- ![Un carré rouge](../media/carre-rouge.png) :: Le carré a quatre côtés de même longueur et quatre angles droits.
- ![Un cercle bleu](../media/cercle-bleu.png) :: Tous les points du cercle sont à la même distance du centre.
- ![Un triangle vert](../media/triangle-vert.png) :: La somme des angles d'un triangle vaut 180°.
- ![Un losange violet](../media/losange-violet.png) = ![Un hexagone gris](../media/hexagone-gris.png) :: Le losange a 4 côtés égaux, l'hexagone régulier en a 6.
- ![Une étoile orange](../media/etoile-orange.png) :: Une étoile à cinq branches possède cinq axes de symétrie.

```yaml
behaviour: {numCardsToUse: 4}
lookNFeel:
  themeColor: "#1e6fb8"
  cardBack: ../media/cercle-bleu.webp
```
````
