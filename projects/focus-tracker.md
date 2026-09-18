---
title: FocusTracker
tagline: A native macOS focus timer that keeps your data where you want it
description: FocusTracker is a native macOS focus timer with a menu-bar countdown, categories, session notes and a monthly dashboard. Sessions stay in a local file on your Mac or go to your own Supabase database.
date: 2026-07-15
repo: https://github.com/brbousnguar/focus-tracker
download: https://github.com/brbousnguar/focus-tracker/releases/latest/download/FocusTracker.dmg
stack: Swift · SwiftUI · AppKit
license: MIT
status: v1.0.0, universal DMG
---

A focus timer that lives in the menu bar, logs every session, and shows you where your time actually went. Native Swift, no account needed.

## What it does

- A Clock-style timer: start, pause, resume, restart, cancel, right from the menu bar.
- Reusable categories, session names linked to them, and an optional note per session.
- A monthly dashboard: total hours, session count, active days, and category-colored charts by day or month.
- A session editor by exact date. Add a past session with just its finish time and duration, and it works out the start.

## Your data, your choice

By default everything stays on your Mac in `~/Library/Application Support/FocusTracker/local-sessions.json`. No account, no token.

If you want your sessions on several machines, point it at your own Supabase project instead: run the included `schema.sql`, then give the app the table's REST URL and your anon key. The key is stored only in the local config file, and the field hides it unless you hold the eye button.

Two small safety nets sit next to the data: an append-only `sessions.jsonl` log, and an `outbox.json` retry queue for when the remote database is unreachable.

## Install

Download the [latest DMG](https://github.com/brbousnguar/focus-tracker/releases/latest/download/FocusTracker.dmg) and drag the app to Applications. It's a universal build for Apple silicon and Intel, not notarized yet, so macOS asks you to approve the first launch once in **Privacy & Security**. Each release ships with a SHA-256 checksum.

Or run it from source on macOS 13+ with Swift 5.9:

```bash
git clone https://github.com/brbousnguar/focus-tracker.git
cd focus-tracker/macos && swift run
```
