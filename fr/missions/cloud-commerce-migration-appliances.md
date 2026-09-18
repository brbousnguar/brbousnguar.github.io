---
title: Migrer une marque mondiale d'électroménager vers SAP Commerce Cloud
tagline: Migration sans interruption de SAP Hybris on-premise vers CCv2, avec des microservices sur SAP BTP Kyma
description: Comment j'ai contribué à migrer la plateforme B2C d'un fabricant mondial d'électroménager de SAP Hybris on-premise vers SAP Commerce Cloud (CCv2) sans interruption, optimisé les API OCC, construit des microservices sur SAP BTP Kyma et mis en place la CI/CD Jenkins. 2022–2024.
date: 2026-09-18
client: Un fabricant mondial d'électroménager
period: 2022 – 2024
role: Consultant senior SAP Commerce Cloud
stack: SAP Commerce Cloud (CCv2) · SAP BTP Kyma · Kubernetes · Jenkins
---

Une boutique B2C mondiale sur SAP Hybris on-premise. Ça marchait, mais la plateforme freinait la montée en charge et la vitesse de livraison de l'équipe.

Le chantier : SAP Commerce Cloud (CCv2), sans interruption pour les clients, et les nouvelles fonctionnalités construites en microservices à côté du cœur commerce plutôt que dedans.

## La forme

<div class="flow" role="group" aria-label="Commerce cloud : vitrines vers SAP Commerce Cloud vers PIM, OMS et paiements, avec des microservices Kyma">
  <div class="flow-node">
    <p class="flow-label">Canaux</p>
    <h3>Vitrines B2C</h3>
    <ul>
      <li>Trafic mondial</li>
      <li>API REST OCC</li>
    </ul>
  </div>
  <div class="flow-link" aria-hidden="true"><span>⇄</span></div>
  <div class="flow-node flow-node--core">
    <p class="flow-label">Cœur commerce</p>
    <h3>SAP Commerce Cloud</h3>
    <ul>
      <li>CCv2</li>
      <li>Microservices sur SAP BTP Kyma</li>
      <li>CI/CD Jenkins</li>
    </ul>
  </div>
  <div class="flow-link" aria-hidden="true"><span>⇄</span></div>
  <div class="flow-node">
    <p class="flow-label">Back-office</p>
    <h3>PIM · OMS · paiements</h3>
    <ul>
      <li>Données produit</li>
      <li>Gestion des commandes</li>
      <li>Passerelles de paiement</li>
    </ul>
  </div>
</div>

## Ce que j'ai construit

- La migration cloud-native de Hybris on-premise vers CCv2, avec un déploiement sans interruption.
- Des API REST OCC plus rapides et plus scalables pour les vitrines.
- Des microservices sur SAP BTP Kyma (Kubernetes), pour que les nouveautés n'atterrissent pas toutes dans le cœur commerce.
- Des pipelines CI/CD avec Jenkins.
- Des couches d'intégration vers le PIM, l'OMS et les passerelles de paiement.

J'ai aussi accompagné l'équipe sur les pratiques agiles, les patterns microservices et la conception d'API.

## Le résultat

Une plateforme cloud-native qui sert le trafic B2C mondial, avec de meilleures performances et du déploiement continu.

Une migration Hybris vers CCv2 en vue ? [Écrivez-moi](#contact).
