---
title: mulewatch
tagline: Serveur MCP en lecture seule pour les logs MuleSoft Anypoint
description: mulewatch est un serveur MCP open source, en lecture seule, qui permet à Claude, Cursor ou tout client MCP de lire les logs MuleSoft Anypoint en direct et archivés, et de lister applications, instances API Manager et assets Exchange.
date: 2026-09-08
repo: https://github.com/brbousnguar/mulewatch
npm: https://www.npmjs.com/package/mulewatch
stack: TypeScript · Node.js · MCP
license: Apache-2.0
status: v0.1 sur npm et le registre MCP
---

mulewatch branche votre assistant IA sur MuleSoft Anypoint Platform : vous posez une question en langage naturel sur votre parc Mule, il répond avec les vraies API de la plateforme. C'est un outil pour la personne d'astreinte, pas pour celle qui écrit les flux.

Il fait la seule chose que le serveur MCP officiel de MuleSoft ne fait pas : lire et chercher dans les logs applicatifs, y compris l'historique de la Monitoring Archive.

## Ce qu'on peut lui demander

- Les derniers logs d'une application, normalisés entre CloudHub 2.0, Runtime Fabric et l'ancien CloudHub.
- Uniquement les lignes `ERROR` et `FATAL`, avec les totaux par logger et par réplica.
- Les logs d'une date passée, depuis l'Anypoint Monitoring Archive.
- Ce qui est déployé où, les instances API Manager devant, et le contenu d'Exchange.

Tous les outils sont en lecture seule. Pas de déploiement, pas de redémarrage, pas de politique : c'est voulu.

## Le point intéressant

La Monitoring Archive est indexée par réplica, pas par application : une recherche naïve doit sonder chaque réplica que l'app a eu. mulewatch essaie d'abord le réplica qui tourne en ce moment, et ne fait un scan complet que si l'app a été redéployée entre-temps. Sur une app de test avec 669 réplicas archivés, la recherche du jour en a sondé un seul.

Toute l'histoire est ici (en anglais) : [The official MuleSoft MCP server can't read your logs, so I built one that can](/notes/mulewatch-anypoint-logs-mcp.html).

## Le lancer

```bash
claude mcp add mulewatch --env ANYPOINT_CLIENT_ID=... --env ANYPOINT_CLIENT_SECRET=... -- npx -y mulewatch
```

Même principe dans Claude Desktop, Cursor et OpenClaw avec une entrée `npx -y mulewatch`. Pour rester loin de la prod : `ANYPOINT_ALLOWED_ENVIRONMENTS=Dev,Sandbox`.
