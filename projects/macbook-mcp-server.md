---
title: MacBook MCP Server
tagline: Ask Claude how your Mac is doing
description: A small Python MCP server that exposes a MacBook's CPU, memory, disk, battery, network, GPU and top processes as MCP tools and a resource, over stdio or streamable HTTP for remote access through Tailscale.
date: 2026-03-26
repo: https://github.com/brbousnguar/macbook-mcp-server
stack: Python · MCP SDK
license: Apache-2.0
status: Working, personal use
---

A small MCP server that lets Claude check on a Mac: CPU, memory, disk, battery, network, GPU, and the processes eating the most CPU or RAM. Ask "why is my fan so loud?" and it can actually look.

## What it exposes

Tools:

- `get_system_overview`
- `get_disk_usage`
- `get_battery`
- `get_network`
- `get_gpu`
- `get_top_resource_processes`

And one resource, `status://system/overview`, for clients that read resources instead of calling tools.

## Local or remote

On the same machine, run it over `stdio` and add it to Claude Desktop. That's the simple path.

For a Mac you want to check from somewhere else, it also speaks streamable HTTP:

```bash
PYTHONPATH=src MCP_TRANSPORT=streamable-http MCP_HOST=127.0.0.1 MCP_PORT=8765 python3 -m macbook_status_mcp.server
```

Don't put that on the public internet. The MCP spec itself warns about DNS rebinding for remote HTTP servers. Keep it private on Tailscale, bound to the Tailscale IP, with the optional bearer token (`MCP_SHARED_TOKEN`). A `launchd` template keeps it running after a reboot.

## Why plain Python

Machine monitoring is a code problem, not a workflow problem, so this uses the native Python MCP SDK. Alerting through something like n8n can sit on top later.
