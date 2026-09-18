---
title: AI Models Costs
tagline: AI API prices side by side, with no backend
description: A static React dashboard comparing public API prices across American, Chinese, European and specialist AI providers, for text, reasoning, image, audio, video, embeddings and more, normalized to USD per 1M tokens where possible.
date: 2026-06-15
repo: https://github.com/brbousnguar/ai-models-costs
live: https://heybrahim.com/ai-models-costs/
stack: TypeScript · React · Vite
status: Live, prices refreshed by script
---

Comparing AI API prices means opening a dozen pricing pages that all use different units. This dashboard puts them in one table: American, Chinese and European providers, plus specialists like Z.AI and Moonshot/Kimi.

It covers text, reasoning, multimodal, image, audio, video, live translation, documents, embeddings, rerank and tooling.

## Curated, not scraped

Vendor pricing pages are all different, and pretending every price can be safely scraped would be lying. So the rows are curated from official sources, and a refresh script does the honest part:

```bash
npm run refresh-prices
```

It checks each provider's official pricing pages, stamps every row with `lastChecked`, and marks a provider `source-unavailable` if none of its pages answered. The row stays, flagged, instead of silently going stale.

Provider pages live in one JSON registry, which the dashboard also shows as a Sources view.

## Units

Token prices are normalized to USD per 1M tokens when the provider publishes that unit. Everything else keeps its native unit: per image, minute, hour, character, page, request or generated second.

## No backend

The build is fully static: no database, no API calls at runtime. It deploys to GitHub Pages from Actions, and you can [use it live](https://heybrahim.com/ai-models-costs/).
