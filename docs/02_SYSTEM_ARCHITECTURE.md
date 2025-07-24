# Documentation AURA : Architecture Système

## 1. Vue d'Ensemble

L'architecture d'AURA est modulaire, conçue pour la résilience et l'évolutivité. Elle est composée de cinq modules principaux qui interagissent en permanence.

```
 +--------------------------------------+
     |     Module 5: Méta-Cognition &       |   (Le Cerveau Évolutif)
     |        Auto-Amélioration             |
     +------------------^-------------------+
                        | Analyse/Modifie
+----------------------------V------------------------------------------------+
|                   Module 4: Moteur de Simulation & Gouvernance              | (Le Bac à Sable & La Loi)
|                                                                             |
|  +---------------------------+  +-----------------------------------------+ |
|  |     Module 1: Moteur      |  |     Module 2: Plateforme Multi-Agents   | | (Le Cœur Pensant)
|  |    Cognitif & Personas    |  |          & Communication                | |
|  +---------------------------+  +-----------------------------------------+ |
|                                                                             |
|  +-----------------------------------------------------------------------+  |
|  |               Module 3: Noyau Fonctionnel d'Entreprise                |  | (Le Corps Opérationnel)
|  +-----------------------------------------------------------------------+  |
|                                                                             |
+-----------------------------------------------------------------------------+
```

## 2. Module 1 : Moteur Cognitif & Personas IA

*   **Rôle :** Doter chaque agent d'une "personnalité" et d'une capacité de raisonnement. C'est le cerveau individuel de chaque unité.
*   **Composants Clés :**
    *   **BaseAgent (Implémentation Fondamentale) :** La classe abstraite `BaseAgent` (`src/core/agents/base_agent.py`) définit la structure commune et les méthodes fondamentales (perceive, decide, act, communicate) pour tous les agents d'AURA.
    *   **Architecte de Personas :** Un système qui, à partir d'une fiche de poste (ex: "CFO"), configure un agent avec des objectifs (maximiser la rentabilité), des traits (prudent, analytique), et des compétences (analyse financière, modélisation).
    *   **Moteur de Raisonnement :** Noyau logique de l'agent qui utilise une combinaison de techniques pour analyser une situation et choisir une action.
    *   **Mémoire Individuelle :** Chaque agent possède une mémoire à court et long terme qui influence ses futures décisions.
*   **Interactions :** Ce module est le cœur de chaque agent. Il interagit constamment avec la plateforme multi-agents pour communiquer et avec le noyau fonctionnel pour agir.

## 3. Module 2 : Plateforme Multi-Agents & Communication

*   **Rôle :** Fournir l'environnement social et hiérarchique où les agents existent, collaborent, négocient et se concurrencent.
*   **Composants Clés :**
    *   **Scheduler d'Agents (Nouveau) :** Le cœur battant du système. L'`AgentScheduler` (`src/core/agents/agent_scheduler.py`) est responsable de l'orchestration du cycle de vie de tous les agents. À chaque "tick" de l'horloge système, il active le cycle `perceive-decide-act` de chaque agent et assure la distribution des messages en attente. C'est lui qui donne vie à la simulation.
    *   **Bus de Communication Asynchrone :** Le système nerveux central, permettant aux agents d'échanger des messages structurés (ordres, rapports, etc.). L'implémentation initiale est `AgentMessenger` (`src/core/agents/base_agent.py`), un messager simple en mémoire.
    *   **Gestionnaire de Hiérarchie :** Applique la structure organisationnelle.
    *   **Moteur de Workflow et de Négociation :** Orchestre les processus complexes impliquant plusieurs agents.
*   **Interactions :** Sert de liant entre tous les agents définis par le Module 1. Le Scheduler est le composant actif qui pilote l'ensemble des interactions.

## 4. Module 3 : Noyau Fonctionnel d'Entreprise

*   **Rôle :** Fournir aux agents les "mains" et les "sens" pour agir sur le monde (virtuel ou réel) et percevoir son état. C'est l'ensemble des outils métiers internes.
*   **Composants Clés :**
    *   **Modules Métiers Natifs :** ERP (gestion de production), CRM (gestion client), Module Comptable (gestion financière).
    *   **Base de Connaissance Vectorielle :** Une mémoire centrale et partagée, interrogeable par les agents. Implémentée par la classe `KnowledgeBase` (`src/core/knowledge/knowledge_base.py`), elle permet le stockage et la recherche sémantique d'informations.
    *   **Agents d'Acquisition de Connaissances :** Des agents spécialisés (`KnowledgeAcquisitionAgent` dans `src/core/knowledge/knowledge_acquisition_agent.py`) qui scannent des sources externes (notamment le web) pour mettre à jour la base de connaissance.
*   **Interactions :** Les agents utilisent ces outils pour exécuter leurs tâches (le CMO utilise le CRM, le COO utilise l'ERP, l'Agent d'Acquisition de Connaissances alimente la `KnowledgeBase`, etc.).

## 5. Module 4 : Moteur de Simulation & Gouvernance

*   **Rôle :** Assurer la sécurité, la conformité et permettre des tests sans risque.
*   **Composants Clés :**
    *   **"Digital Twin" (Jumeau Numérique) :** Un simulateur qui crée une copie exacte de l'entreprise et de son marché pour les tests.
    *   **Moteur de Règles de Gouvernance :** Le "code de la loi" pour les IA, qui applique de force les contraintes de la Charte Éthique.
    *   **Interface de Supervision Humaine :** Le tableau de bord utilisé par le Conseil de Supervision pour monitorer AURA.
*   **Interactions :** C'est l'environnement principal pour les tests du Module 5. Le moteur de règles supervise chaque décision prise par les agents.

## 6. Module 5 : Méta-Cognition & Auto-Amélioration

*   **Rôle :** Permettre à AURA de s'analyser elle-même et de s'améliorer de manière autonome, tant au niveau du code que de la documentation.
*   **Composants Clés :**
    *   **Analyseur de Performance (Profiler) :** Surveille les KPIs et l'efficacité des processus pour identifier des cibles d'amélioration.
    *   **Analyseur de Qualité de Code (Nouveau) :** Analyse le code pour la maintenabilité, l'adhérence aux standards, la complexité et les vulnérabilités de sécurité.
    *   **Analyseur de Documentation (Nouveau) :** Vérifie la précision, l'exhaustivité, la clarté, la lisibilité et la cohérence de la documentation.
    *   **Générateur de Code & Architecte de Solution :** Conçoit et écrit des solutions logicielles (patch, refactoring) et est capable de générer/optimiser des cas de test. Il peut également générer et mettre à jour la documentation.
    *   **Pipeline CI/CD Interne :** Un processus de déploiement automatisé et sécurisé qui teste le nouveau code et les mises à jour de documentation dans le Digital Twin avant toute application au système en production.
*   **Interactions :** Ce module observe tous les autres modules et a la capacité (strictement contrôlée) de les modifier. Les propositions de modifications de documentation importantes passent par une boucle de revue humaine.