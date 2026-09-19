---
title: gemmaquiz
tagline: Turn any subject into a quiz with a local Gemma model
description: gemmaquiz turns a rough subject into a multiple-choice quiz: a local Gemma model on Ollama cleans up the topic, reads the real Wikipedia article and writes the questions. No cloud LLM, no API keys.
date: 2026-08-12
repo: https://github.com/brbousnguar/gemmaquiz
stack: JavaScript · Express · Ollama · Gemma
license: MIT
status: Working, run it locally
video: /assets/video/gemmaquiz-demo.mp4
video_square: /assets/video/gemmaquiz-demo-square.mp4
poster: /assets/img/demo/gemmaquiz.jpg
video_caption: Real run on my Mac mini with a local Gemma model. Voiceover in my own voice, cloned with AI. Waits sped up, and labelled.
video_duration: 23.1
---

Type a subject, even misspelled, and get a quiz about it. The model runs on your machine through Ollama; the only thing that goes out is a Wikipedia lookup.

```text
subject ──▶ gemma refines ──▶ you approve ──▶ wikipedia extract ──▶ gemma writes quiz ──▶ you play
```

## How it works

1. A local Gemma model turns your rough input into a clean Wikipedia topic (`revoltion french` → `French Revolution`), and you approve it.
2. It reads the real Wikipedia article for that topic.
3. It writes a multiple-choice quiz from the article: 3, 5, 10, 15 or 20 questions.
4. You play, with instant feedback and a short explanation per question.

Grounding the questions in the article is the point: the model writes from real text instead of from memory.

## Two settings worth knowing

- **Default model `gemma4:e2b`.** Benchmarked on an Intel Arc GPU it runs at about 28–32 tokens/s, versus about 16 for `gemma4:latest`: roughly 2× faster, and plenty good for quizzes. Set `OLLAMA_MODEL=gemma4:latest` for peak quality.
- **Thinking is off.** Gemma is a thinking model, but for structured JSON like topic cleanup and quiz generation, the reasoning adds latency without better results. `OLLAMA_THINK=1` turns it back on.

## Run it

```bash
ollama pull gemma4:e2b
git clone https://github.com/brbousnguar/gemmaquiz.git
cd gemmaquiz && npm install && npm start
```

Open `http://localhost:3000`. It binds to all interfaces, so other devices on your network can play too. The only runtime dependency is Express, and the frontend is vanilla JS with no build step.
