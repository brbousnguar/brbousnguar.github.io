---
title: mulewatch
tagline: Read-only MCP server for MuleSoft Anypoint logs
description: mulewatch is an open-source, read-only MCP server that lets Claude, Cursor or any MCP client read live and archived MuleSoft Anypoint logs, list deployed apps, API Manager instances and Exchange assets.
date: 2026-09-08
repo: https://github.com/brbousnguar/mulewatch
npm: https://www.npmjs.com/package/mulewatch
stack: TypeScript · Node.js · MCP
license: Apache-2.0
status: v0.1 on npm and the MCP registry
---

mulewatch plugs your AI assistant into MuleSoft Anypoint Platform so you can ask about a Mule estate in plain English and get answers from the real platform APIs. It's built for the person holding the pager, not the person writing the flow.

It does the one thing the official MuleSoft MCP server doesn't: read and search application logs, including the historical ones in the Monitoring Archive.

## What you can ask it

- Latest logs of an app, normalized across CloudHub 2.0, Runtime Fabric and legacy CloudHub.
- Just the `ERROR` and `FATAL` lines, with counts by logger and replica.
- Logs from a past date, pulled from the Anypoint Monitoring Archive.
- What's deployed where, which API Manager instances front it, and what's in Exchange.

Every tool is read-only. There's no deploy, restart or policy tool, on purpose.

## The interesting bit

The Monitoring Archive is indexed per replica, not per app, so a naive search has to probe every replica an app ever had. mulewatch tries the replica that's running right now first, and only falls back to a full scan when the app was redeployed since. On a test app with 669 archived replicas, a search for today probed exactly one.

I wrote the whole story up here: [The official MuleSoft MCP server can't read your logs, so I built one that can](/notes/mulewatch-anypoint-logs-mcp.html).

## Run it

```bash
claude mcp add mulewatch --env ANYPOINT_CLIENT_ID=... --env ANYPOINT_CLIENT_SECRET=... -- npx -y mulewatch
```

It works the same in Claude Desktop, Cursor and OpenClaw with an `npx -y mulewatch` entry. Lock it to safe environments with `ANYPOINT_ALLOWED_ENVIRONMENTS=Dev,Sandbox`.
