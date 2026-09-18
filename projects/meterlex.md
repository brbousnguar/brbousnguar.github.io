---
title: Meterlex
tagline: What your AI coding subscriptions actually cost
description: Meterlex reads the session logs of Claude Code, Codex, Gemini CLI, Antigravity, Ollama and Copilot CLI, prices every model call at the public API rate and compares it with what your subscriptions cost. Local-first, token counts only.
date: 2026-07-30
repo: https://github.com/brbousnguar/meterlex
stack: Python · SQLite · Docker
license: MIT
status: Actively developed, for personal use
---

Flat monthly AI subscriptions hide how much you actually use them. Meterlex reads the logs your coding tools already write to disk, prices every model call at the public API rate, and shows you the subscription next to what the same usage would cost on consumption.

## How it works

Each machine runs a tiny collector: one Python file, no dependencies. It reads that machine's logs and sends **token counts only** to a hub. The hub is two Docker containers and a SQLite file you host. Transcripts never leave the machine that wrote them.

It currently reads Claude Code, Codex, Antigravity, Gemini CLI, Ollama (including cloud models run through Claude Code), Copilot CLI and OpenClaw agents.

The cost of each call is:

```text
(input × prompt_rate + output × completion_rate
 + cache_read × cache_read_rate + cache_write × cache_write_rate) × fx_rate
```

Savings are API cost minus subscription. Positive means the subscription wins.

## The bug that was off by 2.5×

Claude Code logs every part of a reply (the thinking, the text, each tool call) as its own line, and every one of those lines carries the whole reply's usage. Count lines and you overstate tokens by about **2.5×**.

Meterlex counts each reply once, by message id, at its final numbers. Gemini CLI has a similar habit: it appends a message again every time it updates it, so those get deduplicated too.

## What you see

Four screens over this week, this month or this year, counted in your own time zone:

- **Now**: tokens, list price vs. what you paid, cache share, tokens per day.
- **Machines**: one meter per machine, and which collectors went quiet.
- **Harnesses** and **Models**: per tool and per model, ranked.

It's a personal tool, so the API has no auth. Keep it on localhost or a private network.
