# Page — `colonne`

H5P.Column 1.22 · alias : colonne, column · syntaxe Markdown simplifiée : oui

## Syntaxe Markdown

Suite de blocs affichés les uns sous les autres :
- texte Markdown (bloc texte : gras, italique, listes, titres `##`, liens) ;
- tableau Markdown (`| a | b |`) → bloc tableau automatiquement ;
- ligne `![description](image, vidéo ou audio)` ;
- sous-contenu délimité par `::: type` … `:::`, écrit avec la syntaxe Markdown de ce type (`::: qcm`, `::: vf: faux`, `::: trous`, `::: glisser-mots`…) ; `::: type yaml` … `:::` pour écrire ses champs en YAML.

Types acceptés dans une colonne (et donc dans un chapitre de livre) : voir `library:` dans les champs ci-dessous (pas de mots croisés ni de mots mêlés).

```markdown
## La photosynthèse
Les plantes fabriquent leur matière grâce à la **lumière**.

![Schéma](images/photosynthese.png)

| Entrées | Sorties |
|---|---|
| CO₂, eau | glucose, O₂ |

::: qcm
Quel gaz est absorbé ?
- [x] Le dioxyde de carbone
- [ ] Le dioxygène
:::
```

## Champs (bloc ```yaml, noms H5P)

`*` = obligatoire ; les autres champs ont une valeur par défaut ou sont facultatifs.

- content* : liste (min 1) — Liste des contenus empilés
  chaque élément :
    - content* : sous-contenu, library: accordeon | agamotto | audio | enregistreur-audio | trous | graphique | collage | presentation | cartes | outil-documentation | glisser-deposer | glisser-mots | redaction | devinette | tableau | texte | iframe | image | image-interactive | trouver-zone | carrousel | video-interactive | lien | marquer-mots | memory | qcm | questionnaire | quiz | row | choix-unique | resume | frise | vf | video | choix-images — Contenu
    - useSeparator : choix auto|disabled|enabled, défaut auto — Séparer le contenu avec un délimiteur horizontal

## Exemple complet (validé : validateur officiel H5P + affichage)

Fichier `tests/examples/colonne.md` (médias dans `tests/media/`).

```markdown
---
type: colonne
title: Page – Le son
language: fr
license: CC BY-SA 4.0
---
## Qu'est-ce qu'un son ?
Un son est produit par un objet qui **vibre**. La vibration se propage de proche en proche dans un milieu matériel (air, eau, solide) jusqu'à notre oreille.

Écoute ce signal sonore :

![Bip sonore de 440 Hz](../media/bip.wav)

::: vf: faux
Le son peut se propager dans le vide.
:::

::: trous
Complète avec les bonnes valeurs.

Dans l'air, le son se propage à environ {{340}} m/s. L'oreille humaine perçoit les sons de 20 Hz à {{20000|20 000}} Hz.
:::

::: qcm
Dans quel milieu le son se propage-t-il le **plus vite** ?
- [ ] L'air
- [ ] L'eau
- [x] L'acier
  > Oui : plus le milieu est rigide, plus le son va vite.
:::

::: devinette yaml
taskDescription: "Devinette : je **vibre** quand tu parles ou quand tu chantes, et je suis cachée dans ta gorge. Qui suis-je ?"
solutionLabel: Voir la réponse
solutionText: Les cordes vocales.
:::
```
