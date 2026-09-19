---
title: gemmaquiz
tagline: Transformer n'importe quel sujet en quiz avec un modèle Gemma local
description: gemmaquiz transforme un sujet approximatif en quiz à choix multiples : un modèle Gemma local via Ollama nettoie le sujet, lit le vrai article Wikipédia et écrit les questions. Pas de LLM cloud, pas de clé d'API.
date: 2026-08-12
repo: https://github.com/brbousnguar/gemmaquiz
stack: JavaScript · Express · Ollama · Gemma
license: MIT
status: Fonctionnel, à lancer en local
video: /assets/video/gemmaquiz-demo-fr.mp4
video_square: /assets/video/gemmaquiz-demo-fr-square.mp4
poster: /assets/img/demo/gemmaquiz-fr.jpg
video_caption: Vraie session sur mon Mac mini avec un modèle Gemma local. Voix off : ma propre voix, clonée par IA. Les attentes sont accélérées, et c'est indiqué.
video_duration: 21.5
---

Tapez un sujet, même mal orthographié, et obtenez un quiz dessus. Le modèle tourne sur votre machine via Ollama ; la seule chose qui sort, c'est une recherche Wikipédia.

```text
sujet ──▶ gemma corrige ──▶ vous validez ──▶ extrait wikipédia ──▶ gemma écrit le quiz ──▶ vous jouez
```

## Comment ça marche

1. Un modèle Gemma local transforme votre saisie approximative en sujet Wikipédia propre (`revoltion french` → `French Revolution`), et vous validez.
2. Il lit le vrai article Wikipédia de ce sujet.
3. Il écrit un quiz à choix multiples à partir de l'article : 3, 5, 10, 15 ou 20 questions.
4. Vous jouez, avec un retour immédiat et une courte explication par question.

Ancrer les questions dans l'article, c'est tout l'intérêt : le modèle écrit à partir d'un vrai texte, pas de sa mémoire.

## Deux réglages à connaître

- **Modèle par défaut `gemma4:e2b`.** Mesuré sur un GPU Intel Arc, il tourne à environ 28–32 tokens/s contre environ 16 pour `gemma4:latest` : à peu près 2× plus rapide, et largement suffisant pour des quiz. `OLLAMA_MODEL=gemma4:latest` pour la qualité maximale.
- **La réflexion est désactivée.** Gemma est un modèle qui « réfléchit », mais pour du JSON structuré comme la correction de sujet et la génération de quiz, ce raisonnement ajoute de la latence sans meilleur résultat. `OLLAMA_THINK=1` le réactive.

## Le lancer

```bash
ollama pull gemma4:e2b
git clone https://github.com/brbousnguar/gemmaquiz.git
cd gemmaquiz && npm install && npm start
```

Ouvrez `http://localhost:3000`. Il écoute sur toutes les interfaces, donc les autres appareils du réseau peuvent jouer aussi. Seule dépendance à l'exécution : Express, et le frontend est en JS pur, sans build.
