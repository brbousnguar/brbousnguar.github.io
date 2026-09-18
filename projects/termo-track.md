---
title: Termo Track
tagline: Room temperature from a BLE sensor, straight into Claude
description: Termo Track listens to ThermoPro Bluetooth sensors, stores readings in SQLite, shows live temperature and humidity in a React dashboard next to the outside weather, and exposes it all to AI clients through MCP. Local-first, no cloud account.
date: 2026-06-13
repo: https://github.com/brbousnguar/termo-track
stack: Python · FastAPI · SQLite · React · MCP
status: Running at home
---

A ThermoPro sensor broadcasts temperature and humidity over Bluetooth. Termo Track picks that up, keeps the history, and lets both a dashboard and Claude read it. No vendor app, no cloud account.

## How the data flows

1. `scanner_daemon.py` receives the sensor's BLE advertisements (with `bleak`).
2. It writes each reading into SQLite.
3. FastAPI serves REST and a WebSocket from that same database.
4. The React dashboard reads the API and gets live pushes over `/ws`, with a stale-data warning when the sensor goes quiet.
5. `mcp_server.py` exposes the same data to AI clients over stdio or HTTP.

One SQLite file, three readers. That's the whole architecture.

## Inside vs. outside

The dashboard compares indoor readings with the outside weather from Open-Meteo, which needs no API key. Recent windows use the forecast API; month and year views use the historical archive.

## What Claude can ask

MCP tools: `get_current_reading`, `get_sensor_history`, `get_sensor_stats`, `get_comfort_level`, `get_outside_weather` and `get_indoor_outdoor_comparison`.

So "was the bedroom more humid than outside last week?" is one question, not a spreadsheet.
