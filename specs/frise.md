# Timeline — `frise`

H5P.Timeline 1.1 · alias : frise, timeline · syntaxe Markdown simplifiée : oui

## Syntaxe Markdown

`# Titre` de la frise, introduction facultative, puis un événement par section `## date : titre` (dates `1789`, `1789-07-14`, `14/07/1789`, `-500` ; période `## 1939 → 1945 : titre`) suivie d'un texte facultatif. Remarque : ce type charge jQuery et des polices depuis les serveurs de Google à l'affichage (réseau de l'établissement).

```markdown
# La Révolution française
Quelques dates clés.

## 1789-07-14 : Prise de la Bastille
Symbole de la fin de l'Ancien Régime.

## 1792 → 1804 : Première République
```

## Champs (bloc ```yaml, noms H5P)

`*` = obligatoire ; les autres champs ont une valeur par défaut ou sont facultatifs.

- timeline : groupe — Chronologie
  - headline* : texte — Titre
  - text : texte riche (Markdown: a code del em hr li ol s strong ul) — Corps du texte
  - defaultZoomLevel : texte, défaut 0 — Niveau de zoom par défaut
  - backgroundImage : image (chemin ou URL) — Image d'arrière-plan'
  - height : nombre, défaut 600 — Hauteur
  - asset : groupe — Média
    - media : texte — Adresse URL du média
    - credit : texte — Crédits
    - caption : texte — Légende
  - date* : liste (min 1) — Dates
    chaque élément :
      - startDate* : texte — Date de début
      - endDate : texte — Date de fin
      - headline* : texte — Titre
      - text : texte riche (Markdown: a code del em h2 h3 hr li ol pre s strong ul) — Texte
      - tag : texte — Etiquettes
      - asset : groupe — Média
        - media : texte — Adresse URL du média
        - thumbnail : image (chemin ou URL) — Image miniature
        - credit : texte — Crédits
        - caption : texte — Légende
  - era : liste (min 0) — Périodes
    chaque élément :
      - startDate* : texte — Date de début
      - endDate : texte — Date de fin
      - headline* : texte — Titre
      - text : texte riche (Markdown: a code del em hr li ol s strong ul) — Contenu
      - tag : texte — Etiquette
  - language : choix af|ar|hy|eu|bg|ca|zh-cn|hr|cz|da|…, défaut en — Langue
