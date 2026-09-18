---
title: MacBook MCP Server
tagline: Demandez à Claude comment va votre Mac
description: Un petit serveur MCP en Python qui expose le CPU, la mémoire, le disque, la batterie, le réseau, le GPU et les processus les plus gourmands d'un MacBook, en stdio ou en HTTP streamable pour un accès distant via Tailscale.
date: 2026-03-26
repo: https://github.com/brbousnguar/macbook-mcp-server
stack: Python · MCP SDK
license: Apache-2.0
status: Fonctionnel, usage personnel
---

Un petit serveur MCP qui permet à Claude de regarder l'état d'un Mac : CPU, mémoire, disque, batterie, réseau, GPU, et les processus qui consomment le plus de CPU ou de RAM. Demandez « pourquoi le ventilateur tourne à fond ? » et il peut vraiment aller voir.

## Ce qu'il expose

Des outils :

- `get_system_overview`
- `get_disk_usage`
- `get_battery`
- `get_network`
- `get_gpu`
- `get_top_resource_processes`

Et une ressource, `status://system/overview`, pour les clients qui lisent des ressources plutôt que d'appeler des outils.

## En local ou à distance

Sur la même machine, en `stdio`, ajouté à Claude Desktop : c'est le chemin simple.

Pour surveiller un Mac depuis ailleurs, il parle aussi HTTP streamable :

```bash
PYTHONPATH=src MCP_TRANSPORT=streamable-http MCP_HOST=127.0.0.1 MCP_PORT=8765 python3 -m macbook_status_mcp.server
```

Ne l'exposez pas sur internet. La spec MCP elle-même met en garde contre le DNS rebinding pour les serveurs HTTP distants. Gardez-le privé sur Tailscale, lié à l'IP Tailscale, avec le jeton optionnel (`MCP_SHARED_TOKEN`). Un modèle `launchd` le relance après un redémarrage.

## Pourquoi du Python simple

La surveillance d'une machine, c'est un problème de code, pas de workflow : d'où le SDK MCP Python natif. Des alertes via n8n pourront venir par-dessus plus tard.
