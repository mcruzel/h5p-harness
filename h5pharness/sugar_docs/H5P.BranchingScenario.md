Nœuds **nommés** (plus d'indices à gérer). `# Titre` et sous-titre (+ image facultative) pour l'écran d'accueil, puis :
- nœud de contenu `## identifiant` : texte Markdown, **ou** une image/vidéo `![…](…)`, **ou** un bloc `::: type` … `:::` ; ligne `→ identifiant` pour la suite (par défaut : le nœud suivant), `→ fin` ou `→ fin: Titre de fin (score)` pour terminer ;
- nœud question `## identifiant ? Question posée` : choix `- texte → identifiant` (ou `→ fin: …`), retour facultatif en ligne indentée `> …`.

```markdown
# Accident au labo de chimie
Fais les bons choix pour la sécurité de tous.

## situation
Ton voisin renverse un flacon d'acide sur la paillasse.
→ choix

## choix ? Que fais-tu en premier ?
- Je préviens le professeur → bravo
  > Bon réflexe !
- J'essuie avec mon mouchoir → erreur

## bravo
Le professeur sécurise la zone.
→ fin: Bravo ! (10)

## erreur
On ne touche jamais un produit chimique à mains nues.
→ choix
```
