---
title: Moving a global appliance brand to SAP Commerce Cloud
tagline: Zero-downtime migration from on-premise SAP Hybris to CCv2, with microservices on SAP BTP Kyma
description: How I helped move a global home-appliance manufacturer's B2C platform from on-premise SAP Hybris to SAP Commerce Cloud (CCv2) with zero downtime, optimised OCC APIs, built microservices on SAP BTP Kyma and set up Jenkins CI/CD. 2022–2024.
date: 2026-09-18
client: A global home-appliance manufacturer
period: 2022 – 2024
role: Senior SAP Commerce Cloud consultant
stack: SAP Commerce Cloud (CCv2) · SAP BTP Kyma · Kubernetes · Jenkins
---

A global B2C store running on on-premise SAP Hybris. It worked, but the platform was holding back scalability and how fast the team could ship.

The move: SAP Commerce Cloud (CCv2), with no downtime for customers, and new capabilities built as microservices next to it instead of inside it.

## The shape

<div class="flow" role="group" aria-label="Cloud commerce: storefront to SAP Commerce Cloud to PIM, OMS and payments, with Kyma microservices">
  <div class="flow-node">
    <p class="flow-label">Channels</p>
    <h3>B2C storefronts</h3>
    <ul>
      <li>Global traffic</li>
      <li>OCC REST APIs</li>
    </ul>
  </div>
  <div class="flow-link" aria-hidden="true"><span>⇄</span></div>
  <div class="flow-node flow-node--core">
    <p class="flow-label">Commerce core</p>
    <h3>SAP Commerce Cloud</h3>
    <ul>
      <li>CCv2</li>
      <li>Microservices on SAP BTP Kyma</li>
      <li>Jenkins CI/CD</li>
    </ul>
  </div>
  <div class="flow-link" aria-hidden="true"><span>⇄</span></div>
  <div class="flow-node">
    <p class="flow-label">Back office</p>
    <h3>PIM · OMS · payments</h3>
    <ul>
      <li>Product data</li>
      <li>Order management</li>
      <li>Payment gateways</li>
    </ul>
  </div>
</div>

## What I built

- The cloud-native migration from on-premise Hybris to CCv2, with zero-downtime deployment.
- Faster, more scalable OCC REST APIs for the storefronts.
- Microservices on SAP BTP Kyma (Kubernetes), so new features didn't all land in the commerce core.
- CI/CD pipelines with Jenkins.
- Integration layers to the PIM, the OMS and the payment gateways.

I also mentored the team on agile practices, microservices patterns and API design.

## Where it landed

A cloud-native platform serving global B2C traffic, with better performance and continuous deployment.

Planning a Hybris to CCv2 move? [Say hello](#contact).
