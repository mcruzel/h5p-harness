# Twitter User Feed — `twitter`

H5P.TwitterUserFeed 1.0 · alias : twitter, twitteruserfeed, twitter-user-feed · syntaxe Markdown simplifiée : non (bloc ```yaml)

## Champs (bloc ```yaml, noms H5P)

`*` = obligatoire ; les autres champs ont une valeur par défaut ou sont facultatifs.

- userName* : texte — Nom d'utilisateur sur Twitter (Nom qui est affiché lors de vos tweets)
- showReplies : booléen — Montrer les réponses
- numTweets : nombre, min 1, max 20, défaut 5 — Nombre de tweets

## Exemple complet (validé : validateur officiel H5P + affichage)

Fichier `tests/examples/twitter.md` (médias dans `tests/media/`).

````markdown
---
type: twitter
title: Fil d'actualité – la NASA en français
language: fr
---
```yaml
userName: NASA_fr
showReplies: false
numTweets: 5
```
````
