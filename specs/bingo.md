# Bingo — `bingo`

H5P.Bingo 0.3 · alias : bingo · syntaxe Markdown simplifiée : oui

## Syntaxe Markdown

Consigne facultative, puis un mot ou une expression par puce (`- …`) : chaque élève reçoit une grille tirée au hasard. Sans puces : bingo de nombres. Taille de la grille (3 à 7, défaut 5) : `size:` dans un bloc ```yaml ; prévoir au moins taille² mots, davantage pour des grilles variées.

```markdown
Coche chaque mot entendu dans le bulletin météo.

- nuage
- averse
- soleil
```

## Champs (bloc ```yaml, noms H5P)

`*` = obligatoire ; les autres champs ont une valeur par défaut ou sont facultatifs. Libellés et descriptions : ceux de la bibliothèque (anglais) ; valeurs par défaut : en français.

- media : groupe — Media
  - type : sous-contenu, library: image | video | audio — Type (Optional media to display above the question.)
  - disableImageZooming : booléen, défaut false, si type = H5P.Image — Disable image zooming
- taskDescription : texte riche (Markdown: a em h2 h3 hr li ol strong u ul) — Task description (Optionally give a description here.)
- mode : choix numbers|words, défaut words — Mode (Choose the mode for playing. Numbers will be filled in automatically, words need to be given.)
- words : groupe, si mode = words — Words or phrases (groupe à un champ: écrire directement la valeur)
  - wordsContent : texte multiligne — Words or phrases (Use one line for each word and phrase.)
- size : nombre, min 3, max 7, défaut 5 — Board size
- visuals : groupe — Visuals (You can customize the visual appearance here.)
  - buttonImage : image (chemin ou URL) — Image (Joker image for the buttons.)
  - backgroundColor : couleur #rrggbb — Background Color (Background color for the board.)
- sound : groupe — Audio (You can customize audio here.)
  - soundSelected : audio (chemin ou URL) — Selected/unselected a field (Sound to play when a field is selected or unselected.)
  - soundCompleted : audio (chemin ou URL) — Completed row or column (Sound to play when the user has selected a complete row or column.)
- behaviour : réglages — Behavioural settings (These options will let you control how the task behaves.)
  enableRetry=true, shuffleOnRetry=true, joker=false, heightLimitMode=none (none|auto|custom), heightLimit=…

Textes d'interface pré-remplis en français (ne pas fournir sauf besoin) : tryAgain, a11yTryAgain, a11yMute, a11yUnmute.

## Exemple complet (validé : validateur officiel H5P + affichage)

Fichier `sources/exemples/bingo.md` (médias dans `sources/exemples/media/`).

```markdown
---
type: bingo
title: Bingo des mots de la météo
language: fr
---
Écoute la présentatrice météo et coche chaque mot que tu entends. Une ligne complète : BINGO !

- nuage
- averse
- soleil
- brouillard
- orage
- éclaircie
- vent
- neige
- grêle
- température
- degré
- anticyclone
- dépression
- rafale
- humidité
- arc-en-ciel
- tempête
- verglas
- canicule
- gelée
- bruine
- baromètre
- prévision
- front froid
- ciel dégagé
- pluie verglaçante
- vague de chaleur
- bulletin
```
