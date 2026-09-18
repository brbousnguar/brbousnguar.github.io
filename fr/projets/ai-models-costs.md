---
title: AI Models Costs
tagline: Les prix des API d'IA côte à côte, sans backend
description: Un tableau de bord React statique qui compare les prix publics des API d'IA chez les fournisseurs américains, chinois, européens et spécialisés, pour le texte, le raisonnement, l'image, l'audio, la vidéo, les embeddings et plus, normalisés en USD par million de tokens quand c'est possible.
date: 2026-06-15
repo: https://github.com/brbousnguar/ai-models-costs
live: https://heybrahim.com/ai-models-costs/
stack: TypeScript · React · Vite
status: En ligne, prix rafraîchis par script
---

Comparer les prix des API d'IA, c'est ouvrir une douzaine de pages tarifaires qui n'utilisent jamais les mêmes unités. Ce tableau les réunit : fournisseurs américains, chinois et européens, plus des spécialistes comme Z.AI et Moonshot/Kimi.

Il couvre le texte, le raisonnement, le multimodal, l'image, l'audio, la vidéo, la traduction en direct, les documents, les embeddings, le rerank et l'outillage.

## Sélectionné, pas scrapé

Les pages de prix sont toutes différentes, et prétendre qu'on peut toutes les scraper proprement serait mentir. Les lignes sont donc sélectionnées depuis les sources officielles, et un script fait la partie honnête :

```bash
npm run refresh-prices
```

Il vérifie les pages tarifaires officielles de chaque fournisseur, date chaque ligne avec `lastChecked`, et marque un fournisseur `source-unavailable` si aucune de ses pages n'a répondu. La ligne reste, signalée, au lieu de vieillir en silence.

Les pages des fournisseurs vivent dans un seul registre JSON, que le tableau affiche aussi dans une vue Sources.

## Les unités

Les prix au token sont ramenés en USD par million de tokens quand le fournisseur publie cette unité. Le reste garde son unité d'origine : par image, minute, heure, caractère, page, requête ou seconde générée.

## Pas de backend

Le build est entièrement statique : pas de base de données, pas d'appel d'API à l'exécution. Il se déploie sur GitHub Pages via Actions, et vous pouvez [l'utiliser en ligne](https://heybrahim.com/ai-models-costs/).
