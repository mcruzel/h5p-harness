---
type: scenario
title: Accident au labo de chimie – scénario
language: fr
---
```yaml
branchingScenario:
  title: Accident au labo de chimie
  startScreen:
    startScreenTitle: Accident au labo de chimie
    startScreenSubtitle: Fais les bons choix pour garder tout le monde en sécurité.
    startScreenImage: /sources/exemples/media/paysage.jpg
    startScreenAltText: Illustration
  endScreens:
    - endScreenTitle: Fin du scénario
      endScreenSubtitle: Retiens les **règles de sécurité** au laboratoire.
      endScreenScore: 0
      contentId: -1
  content:
    # 1 (id 0)
    - type:
        library: texte
        text: |
          ## La situation
          En TP de chimie, ton voisin renverse un flacon d'**acide chlorhydrique dilué**
          sur la paillasse. Quelques gouttes tombent sur sa blouse.
      nextContentId: 1
    # 2 (id 1)
    - type:
        library: question-embranchement
        branchingQuestion:
          question: Que fais-tu **en premier** ?
          alternatives:
            - text: Je préviens immédiatement le professeur.
              nextContentId: 2
              feedback:
                title: Bon réflexe !
            - text: J'essuie tout de suite avec mon mouchoir.
              nextContentId: 3
    # 3 (id 2)
    - type:
        library: image
        file: /sources/exemples/media/etoile-orange.png
        alt: Une étoile orange, symbole de réussite
      nextContentId: -1
      feedback:
        title: Bravo
        subtitle: Le professeur sécurise la zone et fait rincer la blouse à l'eau.
    # 4 (id 3)
    - type:
        library: texte
        text: |
          ## Mauvaise idée !
          On ne touche **jamais** un produit chimique à mains nues.
          Il faut d'abord prévenir l'adulte responsable.
      nextContentId: 1
```
