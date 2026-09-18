---
title: vibetidy
tagline: Donner l'air entretenu à un repo généré par IA
description: vibetidy est un CLI Node sans dépendance qui écrit un README à partir de ce que contient vraiment un dépôt, avec un LLM qui n'a le droit que de mettre en forme des faits vérifiés, et qui prévient quand un commit de la taille d'une fonctionnalité n'a pas d'issue.
date: 2026-09-08
repo: https://github.com/brbousnguar/vibetidy
npm: https://www.npmjs.com/package/vibetidy
stack: JavaScript · Node.js · zéro dépendance
license: MIT
status: v0.1.0 sur npm
---

Vous avez sorti quelque chose avec v0, Bolt, Lovable ou une longue session Claude. Ça marche. Le README dit encore *Getting Started with Create React App*, et rien ne garde la trace de pourquoi chaque chose a été construite. vibetidy règle ces deux points, et s'arrête là.

```bash
npx vibetidy readme                      # génère README.md, montre le diff, demande confirmation
npx vibetidy issue-check --install-hook  # relance sur les commits de fonctionnalité sans issue
```

## Deux commandes

- **`readme`** scanne le dépôt (manifeste, scripts, dépendances, `.env.example`, points d'entrée, arborescence, README existant) et fait mettre en forme uniquement ces faits par un LLM, dans une structure fixe. Il montre un diff et attend votre accord avant d'écrire.
- **`issue-check`** regarde ce qui est indexé. Un nouveau fichier source ou plus de 40 lignes ajoutées, c'est une fonctionnalité ; lockfiles, build, docs et tests ne comptent pas. Pas de numéro d'issue dans la branche ou les commits ? Il le signale, et peut créer l'issue avec `gh` et écrire un fragment de changelog.

## La règle d'ancrage

Le scanner est le produit ; le modèle ne fait que mettre en forme. Le prompt interdit d'inventer une fonctionnalité, une option, une variable d'environnement, une dépendance ou une version. Peu de faits donnent un README court et exact, pas un README long et plausible.

On peut voir exactement ce qui serait envoyé, sans clé d'API :

```bash
npx vibetidy readme --print-context
```

## Petit, exprès

- **Zéro dépendance à l'exécution.** `npx vibetidy` télécharge un seul paquet.
- **N'importe quel endpoint compatible OpenAI :** OpenAI, OpenRouter, Anthropic, Groq, DeepSeek, Together, ou un Ollama / LM Studio local.
- **Il prévient, il ne bloque pas.** Un hook qui bloque le premier jour se fait contourner avec `--no-verify` le deuxième. Ajoutez `--strict` quand l'habitude est prise.
- La CI tourne sur Ubuntu, macOS et Windows avec Node 20, 22 et 24.

L'histoire de ce que la CI a attrapé, et pourquoi npm a refusé le premier nom (en anglais) : [My README generator isn't allowed to make things up](/notes/vibetidy-grounded-readme.html).
