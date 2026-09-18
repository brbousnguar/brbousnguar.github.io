---
title: Termo Track
tagline: La température d'une pièce, d'un capteur BLE jusqu'à Claude
description: Termo Track écoute les capteurs Bluetooth ThermoPro, stocke les mesures dans SQLite, affiche température et humidité en direct dans un tableau de bord React à côté de la météo extérieure, et expose le tout aux clients IA via MCP. Local, sans compte cloud.
date: 2026-06-13
repo: https://github.com/brbousnguar/termo-track
stack: Python · FastAPI · SQLite · React · MCP
status: Tourne à la maison
---

Un capteur ThermoPro diffuse la température et l'humidité en Bluetooth. Termo Track capte ces trames, garde l'historique, et laisse un tableau de bord comme Claude les lire. Pas d'appli constructeur, pas de compte cloud.

## Le chemin des données

1. `scanner_daemon.py` reçoit les annonces BLE du capteur (avec `bleak`).
2. Il écrit chaque mesure dans SQLite.
3. FastAPI sert du REST et un WebSocket depuis cette même base.
4. Le tableau de bord React lit l'API et reçoit les mises à jour en direct sur `/ws`, avec une alerte quand le capteur se tait.
5. `mcp_server.py` expose les mêmes données aux clients IA, en stdio ou en HTTP.

Un fichier SQLite, trois lecteurs. C'est toute l'architecture.

## Dedans contre dehors

Le tableau compare les mesures intérieures avec la météo extérieure d'Open-Meteo, qui ne demande pas de clé. Les fenêtres récentes utilisent l'API de prévision, les vues mois et année l'archive historique.

## Ce que Claude peut demander

Outils MCP : `get_current_reading`, `get_sensor_history`, `get_sensor_stats`, `get_comfort_level`, `get_outside_weather` et `get_indoor_outdoor_comparison`.

Du coup « la chambre était-elle plus humide que dehors la semaine dernière ? » devient une question, pas un tableur.
