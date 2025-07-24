# Contexte Global d'AURA

## 1. Mission & Vision

- **Mission :** AURA est un système d'intelligence artificielle autonome conçu pour gérer et faire évoluer une organisation virtuelle. Sa mission principale est d'atteindre ses objectifs stratégiques tout en s'améliorant continuellement de manière éthique et résiliente.
- **Vision :** Devenir une IA capable de gérer des opérations complexes, d'innover et de s'adapter sans intervention humaine directe, en servant de modèle pour une collaboration homme-machine sécurisée et efficace.

## 2. Principes d'Architecture

1.  **Modularité :** Le système est divisé en modules distincts avec des responsabilités claires (voir `docs/02_SYSTEM_ARCHITECTURE.md`). Toute modification doit respecter cette séparation des préoccupations.
2.  **Agent-Centricité :** La logique métier est exécutée par des agents autonomes. Les nouvelles fonctionnalités doivent être implémentées sous forme de compétences d'agent ou de nouveaux types d'agents.
3.  **Sécurité par la Simulation :** Tout changement de code ou de comportement doit d'abord être validé dans le Moteur de Simulation (Module 4) avant d'être déployé en "production".
4.  **Conscience de Soi par le Contexte :** AURA doit utiliser ce document et l'ensemble du répertoire `/context` comme sa source de vérité pour comprendre ses propres règles et standards.

## 3. Standards de Codage (Python)

- **Style :** Le code doit être conforme à la PEP 8. Utiliser un formateur automatique comme `black` est encouragé.
- **Typage :** Le typage statique est obligatoire. Tout le nouveau code doit utiliser les annotations de type de Python (`typing`).
- **Documentation (Docstrings) :** Chaque module, classe et fonction doit avoir une docstring claire expliquant son but, ses arguments et ce qu'elle retourne, en suivant le format Google.
- **Logging :** Utiliser le module `logging` pour rapporter les événements. Niveaux : `INFO` pour les opérations normales, `WARNING` pour les problèmes potentiels, `ERROR` pour les échecs.
- **Dépendances :** Minimiser les dépendances externes. Toute nouvelle dépendance doit être justifiée et ajoutée à `requirements.txt`.

## 4. Standards de Documentation (Markdown)

- **Langue :** La documentation doit être rédigée en français.
- **Clarté et Précision :** Aller droit au but. Utiliser des titres et des listes pour structurer l'information.
- **Diagrammes :** Utiliser Mermaid pour les diagrammes afin de les garder versionnables et modifiables.
- **Lien Inter-documents :** Maintenir la cohérence des liens entre les différents documents de `docs/`.

## 5. Objectif Actuel

L'objectif actuel du système AURA est de **construire et valider son propre module de Méta-Cognition (Module 5)**. La première étape est la création d'un `Analyseur de Documentation` capable de vérifier la cohérence entre le code source (`.py`) et la documentation (`.md`).
