---
title: ASCII Art Studio
tagline: De l'art ASCII et des animations de terminal, créés dans le navigateur
description: ASCII Art Studio est une app web 100 % locale qui transforme du texte en art ASCII figlet, dessine les emoji en silhouettes ombrées, génère des animations de terminal et convertit des images en ASCII, puis exporte un .txt ou une boucle .sh exécutable. Pas de compte, pas de backend, pas d'upload.
date: 2026-07-29
repo: https://github.com/brbousnguar/ascii-art-studio
stack: TypeScript · Vite · figlet · Docker
status: Fonctionnel, à lancer en local
---

Une petite app web pour créer de l'art ASCII à glisser dans l'écran d'accueil d'un CLI, un README ou un terminal. Tout se fait dans le navigateur : pas de connexion, pas de serveur, rien d'envoyé.

## Trois outils

- **Texte :** votre texte en ASCII figlet, avec plus de 20 polices et cinq mises en page. Un emoji dans la saisie est dessiné en silhouette ombrée à côté du texte.
- **Animation :** huit générateurs en code pur transforment le texte en images successives : `runway`, `decrypt`, `typewriter`, `glitch`, `slide`, `wave`, `matrix` et `fade`. `runway`, c'est le style Copilot CLI : un coureur traverse l'écran et révèle le texte colonne par colonne.
- **Image vers ASCII :** quatre palettes de caractères, avec contraste, luminosité et inversion.

## Direction le terminal

Copiez le résultat, téléchargez toutes les images dans `frames.txt`, ou téléchargez un `play.sh` autonome qui rejoue l'animation en boucle dans n'importe quel terminal.

## Un défaut connu

Le coureur de `runway` est un emoji, et un emoji occupe deux cellules dans un terminal à chasse fixe. Sur sa ligne, tout ce qui est à sa droite se décale donc d'une cellule. Un coureur en caractères ASCII réglerait ça, c'est prévu.

## Le lancer

```bash
docker compose up -d --build
# ouvrir http://localhost:8091
```

Construit en TypeScript pur avec Vite, figlet pour les polices (toutes intégrées au build) et un échantillonnage de luminance sur canvas pour les images et les emoji. Le conteneur est une étape de build Node servie par nginx.
