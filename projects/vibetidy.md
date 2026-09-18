---
title: vibetidy
tagline: Make an AI-generated repo look maintained
description: vibetidy is a zero-dependency Node CLI that writes a README from what a repository actually contains, with an LLM that's only allowed to format verified facts, and warns when a feature-sized commit has no issue behind it.
date: 2026-09-08
repo: https://github.com/brbousnguar/vibetidy
npm: https://www.npmjs.com/package/vibetidy
stack: JavaScript · Node.js · zero dependencies
license: MIT
status: v0.1.0 on npm
---

You shipped something from v0, Bolt, Lovable or a long Claude session. It works. The README still says *Getting Started with Create React App*, and nothing records why anything was built. vibetidy fixes those two things and stops.

```bash
npx vibetidy readme                      # generate README.md, review the diff, confirm
npx vibetidy issue-check --install-hook  # nag on feature commits with no issue
```

## Two commands

- **`readme`** scans the repo (manifest, scripts, dependencies, `.env.example`, entry points, folder tree, the existing README) and has an LLM turn only those facts into a README with a fixed structure. It shows a diff and waits for you before writing.
- **`issue-check`** looks at what's staged. A new source file or more than 40 inserted lines is a feature; lockfiles, build output, docs and tests don't count. No issue number in the branch or the commits? It tells you, and can file the issue with `gh` and write a changelog fragment.

## The grounding rule

The scanner is the product; the model is a formatter. The prompt forbids inventing a feature, a flag, an env var, a dependency or a version. Thin facts give you a short, accurate README instead of a long, plausible one.

You can see exactly what would be sent, with no API key:

```bash
npx vibetidy readme --print-context
```

## Small on purpose

- **Zero runtime dependencies.** `npx vibetidy` downloads one package.
- **Any OpenAI-compatible endpoint:** OpenAI, OpenRouter, Anthropic, Groq, DeepSeek, Together, or a local Ollama / LM Studio.
- **It warns, it doesn't block.** A hook that blocks on day one gets `--no-verify`'d on day two. Add `--strict` once the habit sticks.
- CI runs on Ubuntu, macOS and Windows with Node 20, 22 and 24.

The story of what CI caught, and why npm refused the first name: [My README generator isn't allowed to make things up](/notes/vibetidy-grounded-readme.html).
