---
title: ASCII Art Studio
tagline: ASCII art and terminal animations, made in the browser
description: ASCII Art Studio is a local-only web app that renders text as figlet ASCII art, draws emoji as shaded silhouettes, generates terminal animations and converts images to ASCII, then exports a .txt or a runnable .sh loop. No account, no backend, no uploads.
date: 2026-07-29
repo: https://github.com/brbousnguar/ascii-art-studio
stack: TypeScript · Vite · figlet · Docker
status: Working, run it locally
---

A small web app for making ASCII art you can drop into a CLI splash screen, a README or a terminal. Everything renders in the browser: no sign-in, no server, nothing uploaded.

## Three tools

- **Text art:** your text in figlet ASCII, across 20+ fonts and five layouts. Put an emoji in the input and it's drawn as a shaded silhouette next to the text.
- **Animation:** eight pure-code generators turn the text into frames: `runway`, `decrypt`, `typewriter`, `glitch`, `slide`, `wave`, `matrix` and `fade`. `runway` is the Copilot CLI look: a runner sweeps across and reveals the text column by column.
- **Image to ASCII:** four character ramps, with contrast, brightness and invert.

## Take it to your terminal

Copy the result, download every frame as `frames.txt`, or download a self-contained `play.sh` that loops the animation in any terminal.

## Known quirk

The `runway` runner is an emoji, and emoji are two cells wide in a monospace terminal. So on the runner's row, everything to its right shifts by one cell. An ASCII-glyph runner would fix it and is on the roadmap.

## Run it

```bash
docker compose up -d --build
# open http://localhost:8091
```

Built with vanilla TypeScript and Vite, figlet for the fonts (all bundled at build time), and canvas luminance sampling for images and emoji. The container is a Node build stage served by nginx.
