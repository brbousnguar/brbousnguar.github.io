---
title: My README generator isn't allowed to make things up
description: vibetidy writes READMEs for AI-generated repos, but the LLM only formats facts a scanner verified. Building it, CI caught two things the project advertised that didn't work, and npm refused a name that looked free. Here's what I learned.
date: 2026-09-18
tags: LLM, developer tools, Node.js, npm, CI
project: https://github.com/brbousnguar/vibetidy
---

Ask an LLM to write a README and you get something long, confident and partly invented: flags that don't exist, env vars nobody reads, a setup step from a different project.

So in [vibetidy](/projects/vibetidy.html) the LLM doesn't get to decide what's true. A scanner reads the repo, and the model only turns those verified facts into prose.

Funny thing: while building a tool about not advertising what isn't real, CI caught me doing exactly that. Twice.

## The scanner is the product

`vibetidy readme` scans the repository first: the manifest, scripts, dependencies, `.env.example`, entry points, the folder tree, the existing README. Only those facts go to the model, and the prompt says it plainly: never invent a feature, a flag, an environment variable, a dependency or a version.

When the facts are thin, you get a short README that's right instead of a long one that's plausible. And you can check what the model would see before spending a token:

```bash
npx vibetidy readme --print-context
```

No API key needed for that. It prints the scanned facts and the full prompt, and exits.

## Bug one: a flag I documented but never registered

`issue-check --help` listed `--no-changelog`. The README's options table listed it too. Using it exited with `Unknown option '--no-changelog'`.

The flag was never registered in the parser. Node's `parseArgs` only honours a `--no-` prefix with `allowNegative`, which needs a newer Node than the `>=20.10.0` the package advertises. So it became a plain `--skip-changelog`.

The fix was one line. The interesting part is that nothing caught it: the docs looked right, the code read plausibly, every test passed. So I added a test for the whole class of bug. It pulls every flag out of each command's `--help` output and asserts the parser accepts it:

```js
for (const flag of flagsIn(help)) {
  const res = runCli([command, flag, 'x', '--help']);
  assert.notEqual(res.status, 2, `${flag} is documented but rejected`);
}
```

To make sure it bites, I planted a fake `--phantom-flag` in the usage text. The suite failed with the exact rejection message.

## Bug two: the tests never ran on Node 20

Opening that PR turned CI red on `main`: 5 legs out of 9.

`npm test` ran `node --test "test/**/*.test.js"`. Glob support in `node --test` only landed in Node 21. On Node 20 the quoted pattern is taken as a literal path, so every 20.x leg failed with `Could not find .../test/**/*.test.js`. The suite had never run on the Node version `engines` promised.

The fix is almost funny: plain `node --test`, with no pattern at all. Default discovery has worked since Node 18. CI went green on all nine legs (Ubuntu, macOS and Windows, times Node 20, 22 and 24).

Same class as bug one: something advertised that didn't work. The 9-leg matrix is why I found both.

## npm said no to a name that looked free

The tool started as `tidyrepo`. `npm view tidyrepo` returned a 404, so the name looked available.

Then `npm publish` failed with a 403. npm's similarity check strips punctuation, so `tidyrepo` collided with an existing `tidy-repo`. A 404 isn't proof a name is free: check the hyphenated and underscored versions too.

It's `vibetidy` now, which honestly fits better.

## Try it

It's MIT, zero runtime dependencies, and works with OpenAI, OpenRouter, Anthropic, Groq, DeepSeek, Together, or a local Ollama:

```bash
npx vibetidy readme --print-context      # see the facts, no key needed
npx vibetidy readme                      # generate, review the diff, confirm
npx vibetidy issue-check --install-hook  # nag on feature commits with no issue
```

If it writes something your repo doesn't back up, that's a bug. Open an issue on [GitHub](https://github.com/brbousnguar/vibetidy).
