---
title: Intégration API-led pour une enseigne de mobilier haut de gamme
tagline: Remplacer les flux point à point par un socle d'intégration unique et observable sur MuleSoft
description: Comment j'ai fait passer les flux e-commerce, ERP, CRM et partenaires d'une enseigne de mobilier haut de gamme d'une toile de liens point à point à une intégration API-led réutilisable sur MuleSoft Anypoint, avec DataWeave et des flux Salesforce CRM. En cours depuis 2025.
date: 2026-09-18
client: Une enseigne de mobilier haut de gamme
period: 2025 – aujourd'hui
role: Spécialiste intégration MuleSoft, consultant via SQLI
stack: MuleSoft Anypoint · DataWeave · Salesforce · ERP
---

Le site e-commerce de l'enseigne, son ERP, son CRM et quelques services tiers se parlaient en direct. Chaque nouveau besoin ajoutait un flux point à point, et quand l'un d'eux cassait, difficile de savoir où.

Depuis janvier 2025, mon travail consiste à faire passer tout ça sur MuleSoft Anypoint, en API-led : chaque système est exposé une seule fois, et chaque flux réutilise ces API.

## La forme

<div class="flow" role="group" aria-label="Intégration API-led : e-commerce vers MuleSoft vers ERP, CRM et partenaires">
  <div class="flow-node">
    <p class="flow-label">Canaux</p>
    <h3>E-commerce</h3>
    <ul>
      <li>Commandes</li>
      <li>Clients</li>
      <li>Catalogue</li>
    </ul>
  </div>
  <div class="flow-link" aria-hidden="true"><span>⇄</span></div>
  <div class="flow-node flow-node--core">
    <p class="flow-label">Couche d'intégration</p>
    <h3>MuleSoft Anypoint</h3>
    <ul>
      <li>API Experience</li>
      <li>API Process · orchestration</li>
      <li>API System · DataWeave</li>
    </ul>
  </div>
  <div class="flow-link" aria-hidden="true"><span>⇄</span></div>
  <div class="flow-node">
    <p class="flow-label">Back-office</p>
    <h3>ERP · CRM · partenaires</h3>
    <ul>
      <li>ERP</li>
      <li>Salesforce CRM</li>
      <li>Services tiers</li>
    </ul>
  </div>
</div>

Les API System portent la connexion à chaque système du back-office. Les API Process orchestrent les flux métier. Les API Experience servent les canaux. Si un système change, seule son API System bouge.

## Ce que j'ai construit

- Des API réutilisables conçues dans Anypoint Studio et Anypoint Code Builder, selon l'approche API-led.
- Des transformations DataWeave pour le mapping, l'enrichissement et l'orchestration entre systèmes.
- Des flux d'intégration entre la plateforme e-commerce, l'ERP, le CRM et les services tiers.
- Des flux de données Salesforce CRM branchés sur MuleSoft, pour des processus métier de bout en bout.
- Des spécifications d'API, des bonnes pratiques et des standards de gouvernance pour l'équipe intégration.

## Le résultat

Un socle d'intégration unique et observable pour les flux commande, CRM et ERP, à la place d'une toile de liens directs. Les standards de gouvernance sont devenus la façon de travailler de l'équipe.

## Ce qui en est sorti

L'IA fait partie du quotidien sur cette mission : GitHub Copilot, un CLI basé sur Ollama qui rédige commits et PR, Claude et Codex pour la revue de code.

Et un projet perso : j'ai d'abord construit un serveur MCP de lecture de logs pour ce parc, puis publié une version sans rien du client, [mulewatch](/fr/projets/mulewatch.html).

Un projet similaire ? [Écrivez-moi](#contact).
