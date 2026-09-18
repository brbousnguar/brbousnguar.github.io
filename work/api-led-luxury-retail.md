---
title: API-led integration for a luxury furniture retailer
tagline: Replacing point-to-point flows with one observable integration backbone on MuleSoft
description: How I moved a luxury furniture retailer's e-commerce, ERP, CRM and third-party flows from point-to-point links to reusable API-led integration on MuleSoft Anypoint, with DataWeave and Salesforce CRM flows. Ongoing since 2025.
date: 2026-09-18
client: A luxury furniture retailer
period: 2025 – now
role: MuleSoft integration specialist, consultant via SQLI
stack: MuleSoft Anypoint · DataWeave · Salesforce · ERP
---

The retailer's e-commerce site, ERP, CRM and a handful of third-party services were talking to each other directly. Every new need meant another point-to-point flow, and when one failed it was hard to tell where.

Since January 2025 my job has been to move that onto MuleSoft Anypoint, API-led: wrap each system once, and let every flow reuse it.

## The shape

<div class="flow" role="group" aria-label="API-led integration: e-commerce to MuleSoft to ERP, CRM and third parties">
  <div class="flow-node">
    <p class="flow-label">Channels</p>
    <h3>E-commerce</h3>
    <ul>
      <li>Orders</li>
      <li>Customers</li>
      <li>Catalogue</li>
    </ul>
  </div>
  <div class="flow-link" aria-hidden="true"><span>⇄</span></div>
  <div class="flow-node flow-node--core">
    <p class="flow-label">Integration layer</p>
    <h3>MuleSoft Anypoint</h3>
    <ul>
      <li>Experience APIs</li>
      <li>Process APIs · orchestration</li>
      <li>System APIs · DataWeave</li>
    </ul>
  </div>
  <div class="flow-link" aria-hidden="true"><span>⇄</span></div>
  <div class="flow-node">
    <p class="flow-label">Back office</p>
    <h3>ERP · CRM · partners</h3>
    <ul>
      <li>ERP</li>
      <li>Salesforce CRM</li>
      <li>Third-party services</li>
    </ul>
  </div>
</div>

System APIs own the connection to each back-office system. Process APIs orchestrate the business flows. Experience APIs serve the channels. Change one system and only its System API has to move.

## What I built

- Reusable APIs designed in Anypoint Studio and Anypoint Code Builder, following API-led connectivity.
- DataWeave transformations for the mapping, enrichment and orchestration between systems.
- Integration flows between the e-commerce platform, the ERP, the CRM and third-party services.
- Salesforce CRM data flows wired into MuleSoft, so business processes run end to end.
- API specifications, best practices and governance standards for the integration team.

## Where it landed

One observable integration backbone across the order, CRM and ERP flows, instead of a web of direct links. The governance standards became the team's way of working.

## What came out of it

AI is part of the daily workflow on this mission: GitHub Copilot, an Ollama-based CLI that writes commits and PRs, Claude and Codex for code review.

It also produced a side project. I first built a log-reading MCP server for this estate, then released a client-free version as [mulewatch](/projects/mulewatch.html).

Working on something similar? [Say hello](#contact).
