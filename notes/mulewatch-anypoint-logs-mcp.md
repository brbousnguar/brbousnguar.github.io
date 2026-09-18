---
title: Reading MuleSoft Anypoint logs from an AI agent: why I built mulewatch
description: MuleSoft's official MCP server builds and deploys Mule apps but cannot read application logs. mulewatch is a read-only MCP server that fetches live and archived Anypoint logs, finding the right replica in a handful of calls.
date: 2026-09-18
tags: MuleSoft, Anypoint Platform, MCP, observability
project: https://github.com/brbousnguar/mulewatch
---

**TL;DR** — MuleSoft ships an official MCP server, but it is a development tool: it scaffolds, generates and deploys, and it does not retrieve application logs. During an incident, logs are the first thing you need. [mulewatch](https://github.com/brbousnguar/mulewatch) is an open-source, read-only MCP server that gives Claude, Cursor or any MCP client the live Runtime Manager logs *and* the historical Monitoring Archive — resolving the right replica in a few calls instead of hundreds. It runs with `npx -y mulewatch` and your own connected app.

## What does the official MuleSoft MCP server cover?

MuleSoft publishes [`mulesoft-mcp-server`](https://docs.mulesoft.com/mulesoft-mcp-server). It is built for the person *writing* the integration: it creates Mule projects, generates flows and API specs, and deploys applications, mostly from a local project open in an IDE.

That is a good tool for building. It is the wrong shape for operating. At the time of writing (September 2026) it has no tool for retrieving or searching application logs, and it assumes a checked-out Mule project that the on-call engineer usually doesn't have.

## Why are logs the part that matters?

When an order stops reaching the ERP at 2 a.m., the questions are always the same:

- Which application failed, in which environment?
- What did it log around the time of the failure?
- Did it fail once, or has it been failing since the last deployment?

Every one of those needs logs. An AI agent that can list your APIs but can't read a stack trace can't help with any of them. So mulewatch does one job — observability — and stays out of deployment entirely.

## Why isn't the Runtime Manager log tail enough?

The logs you see in Runtime Manager are a **live tail**: a small rolling buffer per application. On a busy app it can scroll out within minutes, whatever `startTime` and `endTime` you pass. If the incident happened last night, the tail has already forgotten it.

The history lives somewhere else: the **Anypoint Monitoring Archive API**. It stores log files in ten-minute windows, landing each file roughly ten minutes after its window closes, and keeps them far longer. It needs Anypoint Monitoring to be enabled for the organization.

## How does the Monitoring Archive index logs?

This is the part that makes archive search slow if you do it naively. The archive is indexed **per replica**, not per application. Each entity is named `{appName}_{replicaId}`, and every redeploy creates new replicas. You cannot ask for "the logs of `order-sync-api` on 9 August"; you have to know which replica was running that day and ask for its files.

An application that has been redeployed often accumulates hundreds of replica entities. Probing each one is slow, and the Archive API allows **60 requests per minute**.

## How does mulewatch find the right replica quickly?

It takes two paths and reports which one it used:

1. **Live-replica fast path.** It reads the replica ids visible in the current Runtime Manager tail and tries those first. Pods usually live between redeploys, so the replica running now normally produced the logs of the recent past too. A typical lookup costs a handful of archive calls.
2. **Full-scan fallback.** If that replica has no files for the requested dates — because the app was redeployed since — it lists every replica the application has ever had and probes each one, bounded by a `maxEntities` cap.

On a production application used for testing, the archive held **669 replica entities**. A search for the current day went through the fast path, probed **one** entity, found 127 archive files and parsed 2,859 log lines. A date from before the last redeploy correctly fell back to the full scan, which is the slow case the cap exists for.

The client throttles itself below the 60 requests/minute limit and backs off on `429`, so a long search slows down instead of failing.

## Why is every tool read-only?

Because an LLM should not be restarting production Mule applications, and the official server already covers deployment for people who want it. mulewatch has no deploy, stop, restart or policy tools at all.

It also scopes the whole server, not one tool, to the environments you allow:

```dotenv
ANYPOINT_ALLOWED_ENVIRONMENTS=Dev,Sandbox
```

With that set, every tool refuses anything outside the list and says why. Pair it with a connected app that only has access to those environments and production is out of reach twice over.

## What trips people up when connecting to Anypoint?

One thing, almost every time: **environments belong to business groups, not to the root organization.** Connected-app credentials resolve to the root org, which often has zero environments — so the first call comes back empty and it looks like the credentials are wrong.

mulewatch has an `anypoint_list_business_groups` tool for exactly this. List the groups, then pass the right id as `orgId` or pin it with `ANYPOINT_ORG_ID`.

The second trap is scopes. Anypoint answers a missing scope with a bare `403 Forbidden`; mulewatch catches it and names the scope you probably need (`Read Applications`, Monitoring `Viewer`, `View APIs Configuration`…).

## How do I try it?

Create a connected app in **Access Management → Connected Apps** ("acts on its own behalf"), grant the read scopes, and point your MCP client at `npx`:

```json
{
  "mcpServers": {
    "mulewatch": {
      "command": "npx",
      "args": ["-y", "mulewatch"],
      "env": {
        "ANYPOINT_CLIENT_ID": "your_connected_app_client_id",
        "ANYPOINT_CLIENT_SECRET": "your_connected_app_client_secret"
      }
    }
  }
}
```

For Claude Code:

```bash
claude mcp add mulewatch --env ANYPOINT_CLIENT_ID=... --env ANYPOINT_CLIENT_SECRET=... -- npx -y mulewatch
```

Start with `anypoint_whoami`: it shows which credentials, business group and environment allowlist the server is running with. Then ask in plain language — *"show me the ERROR lines of order-sync-api in Prod yesterday between 1 and 3 a.m."* — and the agent picks `anypoint_search_archived_logs`.

## What's the current status?

Version 0.1, Apache-2.0, on [npm](https://www.npmjs.com/package/mulewatch) and the [MCP registry](https://registry.modelcontextprotocol.io/?q=mulewatch). Every read path was exercised against a live Anypoint organization, except API Manager instances, which still need a test with the `View APIs Configuration` scope. Issues and pull requests are welcome on [GitHub](https://github.com/brbousnguar/mulewatch).

*MuleSoft, Anypoint Platform and CloudHub are trademarks of Salesforce, Inc. mulewatch is an independent project, not affiliated with or endorsed by Salesforce.*
