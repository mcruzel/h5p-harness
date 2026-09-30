# Twitter User Feed — `twitter`

H5P.TwitterUserFeed 1.0 · alias : twitter, twitteruserfeed, twitter-user-feed · syntaxe Markdown simplifiée : non (bloc ```yaml)

> **Attention — type obsolète : X (Twitter) a fermé l'intégration des fils, le contenu n'affichera qu'un message d'obsolescence (en anglais).** À ne pas utiliser pour une nouvelle activité.

## Champs (bloc ```yaml, noms H5P)

`*` = obligatoire ; les autres champs ont une valeur par défaut ou sont facultatifs. Libellés et descriptions : ceux de la bibliothèque (anglais) ; valeurs par défaut : en français.

- userName* : texte — Username on Twitter (The username we'll be fetching tweets from)
- showReplies : booléen — Show replies
- numTweets : nombre, min 1, max 20, défaut 5 — Number of tweets

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
