---
title: Meterlex
tagline: Ce que coûtent vraiment vos abonnements d'IA pour coder
description: Meterlex lit les logs de session de Claude Code, Codex, Gemini CLI, Antigravity, Ollama et Copilot CLI, valorise chaque appel au tarif public de l'API et le compare au prix de vos abonnements. Local d'abord, uniquement des compteurs de tokens.
date: 2026-07-30
repo: https://github.com/brbousnguar/meterlex
stack: Python · SQLite · Docker
license: MIT
status: En développement actif, usage personnel
---

Un abonnement IA à prix fixe cache combien vous l'utilisez vraiment. Meterlex lit les logs que vos outils de code écrivent déjà sur le disque, valorise chaque appel de modèle au tarif public de l'API, et met l'abonnement à côté de ce que la même consommation coûterait à l'usage.

## Comment ça marche

Chaque machine fait tourner un petit collecteur : un seul fichier Python, sans dépendance. Il lit les logs de la machine et envoie **uniquement des compteurs de tokens** à un hub. Le hub, c'est deux conteneurs Docker et un fichier SQLite que vous hébergez. Les transcriptions ne quittent jamais la machine qui les a écrites.

Il lit aujourd'hui Claude Code, Codex, Antigravity, Gemini CLI, Ollama (y compris les modèles cloud lancés via Claude Code), Copilot CLI et les agents OpenClaw.

Le coût de chaque appel :

```text
(input × prompt_rate + output × completion_rate
 + cache_read × cache_read_rate + cache_write × cache_write_rate) × fx_rate
```

L'économie, c'est le coût API moins l'abonnement. Positif, l'abonnement est gagnant.

## Le bug qui multipliait tout par 2,5

Claude Code écrit chaque morceau d'une réponse (la réflexion, le texte, chaque appel d'outil) sur sa propre ligne, et chacune de ces lignes porte la consommation de toute la réponse. Si on compte les lignes, on surestime les tokens d'environ **2,5×**.

Meterlex compte chaque réponse une seule fois, par identifiant de message, avec ses chiffres finaux. Gemini CLI a une manie proche : il réécrit un message à chaque mise à jour, donc ces doublons sont retirés aussi.

## Ce qu'on voit

Quatre écrans, sur la semaine, le mois ou l'année, comptés dans votre fuseau horaire :

- **Now** : tokens, prix catalogue contre prix payé, part du cache, tokens par jour.
- **Machines** : un compteur par machine, et les collecteurs devenus muets.
- **Harnesses** et **Models** : par outil et par modèle, classés.

C'est un outil perso : l'API n'a pas d'authentification. Gardez-la en local ou sur un réseau privé.
