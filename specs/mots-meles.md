# Find The Words — `mots-meles`

H5P.FindTheWords 1.4 · alias : mots-meles, findthewords, find-the-words · syntaxe Markdown simplifiée : oui

## Syntaxe Markdown

Consigne facultative, puis les mots à cacher : une ligne `- mot` chacun (ou `mots: a, b, c`). Lettres uniquement, sans espace.

```markdown
Trouve les noms d'organites.

- noyau
- ribosome
- vacuole
```

## Champs (bloc ```yaml, noms H5P)

`*` = obligatoire ; les autres champs ont une valeur par défaut ou sont facultatifs.

- taskDescription : texte, défaut Trouvez les mots dans la gril… — Task description
- wordList : texte, défaut un,deux,trois — Word list
- behaviour : réglages — Behavioural settings
  fillPool=abcdefghijklmnopqrstuvwxyz, preferOverlap=true, showVocabulary=true, enableShowSolution=true, enableRetry=true

Textes d'interface pré-remplis en français (ne pas fournir sauf besoin) : l10n.
