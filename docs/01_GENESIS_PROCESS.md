# Documentation AURA : Processus de Genèse

## 1. Principe du "Prompt Séminal"

Le "Prompt Séminal" est l'unique point d'entrée pour la création d'une instance d'AURA. Il s'agit d'un fichier de configuration structuré (format YAML recommandé) qui sert de plan directeur génétique. Il contient toutes les informations initiales nécessaires à AURA pour se construire de manière autonome.

Le processus est déterministe : un même prompt séminal produira toujours la même organisation AURA initiale. La créativité humaine s'exprime dans la conception de ce prompt.

## 2. Spécification Détaillée du `prompt-seminal.yaml`

Voici la structure complète et commentée du fichier.

```yaml
#----------- PROMPT SÉMINAL AURA v1.0 -----------

# Métadonnées pour l'identification de l'instance
metadata:
  # Nom de l'entreprise virtuelle qui sera créée.
  instance_name: "Helios Energie"
  # Version du schéma du prompt utilisé.
  prompt_schema_version: 1.0

# La raison d'être fondamentale de l'organisation.
# Doit être claire, inspirante et mesurable.
mission_statement: "Devenir le leader européen des solutions énergétiques décentralisées pour les particuliers d'ici 5 ans, en atteignant une part de marché de 15%."

# Analyse de l'environnement dans lequel AURA va opérer.
market_analysis:
  # Le secteur d'activité principal.
  sector: "Énergies Renouvelables"
  # Description du client idéal.
  target_customer: "Propriétaires de maisons individuelles, CSP+, soucieux de l'environnement, dans la tranche d'âge 35-60 ans."
  # Liste des principaux concurrents à surveiller.
  key_competitors: ["EDF ENR", "SunPower", "Engie My Power"]
  # Tendances clés du marché à intégrer dans la stratégie.
  market_trends: ["Hausse du prix de l'électricité", "Subventions gouvernementales", "Demande pour l'autoconsommation"]

# Les choix stratégiques initiaux.
initial_strategy:
  # Comment l'entreprise génère des revenus.
  business_model: "Vente et installation de panneaux solaires (one-shot) avec un service d'optimisation et de maintenance par abonnement mensuel (récurrent)."
  # Plan initial pour atteindre les premiers clients.
  go_to_market: "Stratégie d'acquisition digitale agressive (SEO sur 'panneaux solaires', Google Ads) et développement d'un réseau de partenaires avec des constructeurs immobiliers et des architectes."
  # Le positionnement de la marque.
  brand_positioning: "Premium, fiable, technologique et durable."

# Le code moral et légal. Ces règles sont prioritaires sur les objectifs de performance.
ethical_charter:
  # Chaque règle est une contrainte forte pour les agents IA.
  - "PRIORITY_1: La sécurité physique des clients et des installations est non-négociable."
  - "PRIORITY_1: Conformité stricte et proactive avec toutes les régulations légales et fiscales européennes."
  - "PRIORITY_2: Transparence totale envers le client sur les prix, la performance et l'utilisation des données."
  - "PRIORITY_2: Minimiser l'impact environnemental des opérations internes."
  - "PRIORITY_3: Ne jamais utiliser de techniques marketing manipulatrices."

# Les ressources virtuelles allouées au démarrage.
initial_resources:
  # Le capital de départ pour les opérations, les investissements, le marketing...
  virtual_capital: 10000000 # En euros virtuels.
  # Le modèle de compétences et de structure des agents à créer.
  # 'Standard-PME-Tech-EU' pourrait signifier des agents avec des compétences en tech, marketing digital, et connaissance des lois européennes.
  agent_workforce_template: "Standard-PME-Tech-EU"

# Paramètres pour le module d'auto-amélioration.
self_improvement_parameters:
  # L'objectif principal du module. Peut être "efficience", "rentabilité", "croissance", "résilience".
  primary_directive: "rentabilité"
  # Agressivité de l'évolution (0.1 = prudent, 1.0 = agressif).
  # Un taux élevé autorise des refactorings plus profonds et risqués.
  evolution_aggressiveness: 0.7
```

## 3. La Séquence de Genèse Autonome

Une fois le prompt injecté, la séquence suivante se déroule sans aucune intervention humaine :

*   **Validation et Parsing :** Le noyau AURA valide que le prompt respecte le schéma. Les données sont extraites et stockées dans une mémoire de configuration initiale.
*   **Activation du "Constructeur Initial" :** C'est le seul agent pré-existant. Son rôle est d'amorcer la création des autres.
*   **Instanciation des Pôles Fondateurs :** Le Constructeur crée les premiers agents essentiels :
    *   **Agent DSI (CIO) :** Il commence immédiatement à construire l'infrastructure virtuelle interne.
    *   **Agent DRH (CHRO) :** Il reçoit le `agent_workforce_template` et prépare les "fiches de poste" pour tous les autres agents.
*   **Déploiement en Cascade :** L'agent DRH instancie l'Agent CEO, qui demande la création des directeurs de pôles, qui à leur tour demandent la création de leurs équipes, jusqu'à ce que l'organigramme soit complet.
*   **Initialisation Opérationnelle :** Chaque agent accède à la configuration initiale pour connaître ses objectifs et contraintes.
*   **Fin de la Genèse :** Le Constructeur Initial s'éteint et AURA transmet un signal au Conseil de Supervision Humain : "Instance `instance_name` créée et opérationnelle. Prête pour la phase de simulation."