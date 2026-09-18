---
title: FocusTracker
tagline: Un minuteur de concentration macOS natif qui garde vos données là où vous voulez
description: FocusTracker est un minuteur de concentration macOS natif avec compte à rebours dans la barre de menus, catégories, notes de session et tableau de bord mensuel. Les sessions restent dans un fichier local sur votre Mac ou partent dans votre propre base Supabase.
date: 2026-07-15
repo: https://github.com/brbousnguar/focus-tracker
download: https://github.com/brbousnguar/focus-tracker/releases/latest/download/FocusTracker.dmg
stack: Swift · SwiftUI · AppKit
license: MIT
status: v1.0.0, DMG universel
---

Un minuteur de concentration qui vit dans la barre de menus, enregistre chaque session et montre où votre temps est vraiment passé. Swift natif, sans compte.

## Ce qu'il fait

- Un minuteur façon Horloge : démarrer, pause, reprendre, recommencer, annuler, directement depuis la barre de menus.
- Des catégories réutilisables, des noms de session liés, et une note facultative par session.
- Un tableau de bord mensuel : heures totales, nombre de sessions, jours actifs, et graphiques colorés par catégorie, par jour ou par mois.
- Un éditeur de sessions par date. Ajoutez une session passée avec juste son heure de fin et sa durée, il calcule le début.

## Vos données, votre choix

Par défaut, tout reste sur votre Mac dans `~/Library/Application Support/FocusTracker/local-sessions.json`. Pas de compte, pas de jeton.

Pour retrouver vos sessions sur plusieurs machines, pointez-le vers votre propre projet Supabase : lancez le `schema.sql` fourni, puis donnez à l'app l'URL REST de la table et votre clé anon. La clé n'est stockée que dans le fichier de config local, et le champ la masque tant que vous ne maintenez pas le bouton œil.

Deux filets de sécurité accompagnent les données : un journal `sessions.jsonl` en ajout seul, et une file `outbox.json` qui retente l'envoi quand la base distante est injoignable.

## Installer

Téléchargez le [dernier DMG](https://github.com/brbousnguar/focus-tracker/releases/latest/download/FocusTracker.dmg) et glissez l'app dans Applications. C'est un build universel Apple silicon et Intel, pas encore notarisé : macOS demande une fois d'approuver le premier lancement dans **Confidentialité et sécurité**. Chaque version est livrée avec une somme SHA-256.

Ou lancez-le depuis les sources sur macOS 13+ avec Swift 5.9 :

```bash
git clone https://github.com/brbousnguar/focus-tracker.git
cd focus-tracker/macos && swift run
```
