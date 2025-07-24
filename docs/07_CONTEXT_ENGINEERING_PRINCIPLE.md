# Documentation AURA : Principe d'Ingénierie de Contexte

## 1. Définition

L'Ingénierie de Contexte est une discipline fondamentale pour AURA, inspirée par les travaux de la communauté IA (notamment le dépôt `context-engineering-intro`). Elle consiste à structurer et à fournir systématiquement un ensemble complet d'informations (le "contexte") à une IA pour qu'elle puisse réaliser des tâches complexes de manière autonome, cohérente et alignée avec les standards et objectifs d'un projet.

Ce principe va au-delà de la simple "ingénierie de prompt". Il ne s'agit pas seulement de bien formuler une question, mais de construire un environnement informationnel riche et structuré dans lequel les agents d'AURA peuvent opérer.

## 2. Application dans AURA

L'Ingénierie de Contexte est au cœur du **Module 5: Méta-Cognition & Auto-Amélioration**. Pour qu'AURA puisse s'analyser et s'améliorer, elle doit avoir une compréhension profonde de sa propre structure.

Le contexte est fourni à travers un répertoire dédié `context/` à la racine du projet.

## 3. Composants du Contexte

Le répertoire `context/` contiendra, à terme, plusieurs types de documents :

*   **`aura_context.md`**: Le document maître. Il définit la mission, les principes d'architecture, les standards de codage, le style de la documentation, et les objectifs généraux d'AURA. C'est la "constitution" du projet.
*   **`examples/`**: Un sous-répertoire contenant des extraits de code idiomatique. Quand le `Générateur de Code` (Module 5) doit implémenter une nouvelle fonctionnalité, il doit s'inspirer de ces exemples pour respecter les conventions.
*   **`personas/`**: Des descriptions détaillées des rôles et des profils des agents standards (ex: "KnowledgeAcquisitionAgent"), pour que l'Architecte de Personas (Module 1) puisse les instancier de manière cohérente.
*   **`templates/`**: Des modèles pour les tâches récurrentes, comme les rapports de bug, les analyses de performance, ou les nouvelles propositions d'architecture.

## 4. Workflow d'Auto-Amélioration Basé sur le Contexte

1.  **Perception :** Un agent du Module 5 (ex: l'Analyseur de Qualité de Code) identifie un problème (ex: un code non-conforme aux standards).
2.  **Chargement du Contexte :** L'agent charge le `aura_context.md` et les exemples pertinents depuis `context/examples/`.
3.  **Prise de Décision :** En s'appuyant sur le contexte, l'agent formule une solution (ex: un patch de refactoring). Le contexte garantit que la solution est alignée avec l'architecture et les conventions du projet.
4.  **Action :** Le `Générateur de Code` produit le patch.
5.  **Vérification :** Le patch est testé dans le Moteur de Simulation (Module 4), en utilisant potentiellement des templates de test également définis dans le contexte.

Ce principe est la pierre angulaire qui permettra à AURA de passer d'un système réactif à un système proactif et véritablement "conscient" de sa propre nature.
