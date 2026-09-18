---
title: Counting Claude Code tokens from the logs? You're probably 2.5× too high
description: Claude Code writes one log line per part of a reply, and every line repeats the whole reply's token usage. Count lines and you overcount tokens about 2.5×, output about 4.4×. Key by message id instead. Here's the fix from Meterlex, plus the same trap in Gemini CLI.
date: 2026-09-18
tags: Claude Code, AI tooling, observability, Python
project: https://github.com/brbousnguar/meterlex
---

If you add up token usage from Claude Code's session logs line by line, your total is wrong. On my machine it was **2.5×** too high, and output tokens were **4.4×** too high.

The logs aren't lying. Every line just repeats the usage of the whole reply it belongs to. Count replies, not lines: key by the message id.

I hit this building [Meterlex](/projects/meterlex.html), a tool that prices my AI coding usage at API rates. Here's what's going on and the fix.

## One reply, many lines

Claude Code keeps transcripts in `~/.claude/projects/**/*.jsonl`. A single assistant reply isn't one line. Each part of it is logged on its own line: the thinking, the text, each tool call.

And each of those lines carries the same `usage` block, for the whole reply. Simplified, with made-up numbers, one reply with a text part and a tool call looks like this:

```json
{"type": "assistant", "uuid": "a1…", "message": {"id": "msg_01X…", "usage": {"input_tokens": 12, "output_tokens": 480}}}
{"type": "assistant", "uuid": "b2…", "message": {"id": "msg_01X…", "usage": {"input_tokens": 12, "output_tokens": 480}}}
```

Two lines, two different `uuid`s, one `message.id`. Sum both and you've counted that reply twice. A reply with five tool calls gets counted six or seven times.

## How big the error is

On my Mac's transcripts: **44,158** assistant lines, but only **18,701** actual replies.

Counting lines gave 2.5× the real tokens. Output tokens were 4.4× too high.

That matters if you're doing what Meterlex does: comparing a flat subscription with what the same usage would cost on the API. Overcount the usage and the subscription looks like a way better deal than it is.

## The fix: key by message id

Use `message.id` as the key for a reply, and when you see it again, merge instead of adding. The one subtle bit: a reply's numbers can grow while it streams, so keep each count at its largest value, not the first or the sum.

This is the core of it, from the Meterlex collector:

```python
def _merge_max(a, b):
    """Two records of the same reply: each token count at its largest
    (a reply's numbers only grow as it streams), the earliest time."""
    m = dict(a)
    for f in TOKEN_FIELDS:
        m[f] = max(a[f], b[f])
    m["ts"] = min(a["ts"], b["ts"])
    return m

key = (session_id, msg.get("id") or uuid)
replies[key] = _merge_max(replies[key], t) if key in replies else t
```

Lines without a `message.id` fall back to their `uuid`, so nothing gets dropped.

## Migrating the rows you already stored

If you've been storing per-line rows, re-sending the same transcript with the new key would just add a third copy. So each reply also carries its old per-line `uuid`s as `alt_keys`, and the hub folds any stored row with one of those keys into the new one. Old data cleans itself up the next time a file is read.

## Gemini CLI does it too

Different tool, same trap. Gemini CLI appends a message again every time it updates it. One project's file had **56,651** lines for **908** messages. Same fix: key by message id.

Codex has a milder version: it can repeat a `token_count` event with an unchanged running total. Meterlex skips those.

## Try it

If you track AI usage from local logs, check your keys. Count distinct message ids against lines on one of your own transcripts. The gap is the overcount.

Meterlex does all of this for Claude Code, Codex, Gemini CLI, Antigravity, Ollama, Copilot CLI and OpenClaw, and it's MIT on [GitHub](https://github.com/brbousnguar/meterlex). If your numbers look off in a different way, open an issue.
