import yaml
from dataclasses import asdict
from typing import Type, Dict, Any

from src.core.genesis.prompt_schema import PromptSeminal
from src.core.agents.base_agent import AgentMessenger
from src.core.agents.concrete_agents import DSIAgent, DRHAgent

class InitialConstructor:
    def __init__(self, prompt_file_path: str):
        self.prompt_file_path = prompt_file_path
        self.prompt_seminal: PromptSeminal = None
        self.messenger = AgentMessenger()
        self.agents: Dict[str, Any] = {}

    def load_and_validate_prompt(self) -> PromptSeminal:
        """Charge et valide le fichier YAML du prompt séminal."""
        try:
            with open(self.prompt_file_path, 'r', encoding='utf-8') as f:
                raw_data = yaml.safe_load(f)
            
            self.prompt_seminal = self._from_dict(PromptSeminal, raw_data)
            print(f"Prompt séminal chargé et validé depuis {self.prompt_file_path}")
            return self.prompt_seminal
        except FileNotFoundError:
            print(f"Erreur : Le fichier de prompt séminal n'a pas été trouvé à {self.prompt_file_path}")
            raise
        except yaml.YAMLError as e:
            print(f"Erreur de parsing YAML dans {self.prompt_file_path}: {e}")
            raise
        except Exception as e:
            print(f"Erreur inattendue lors du chargement du prompt: {e}")
            raise

    def _from_dict(self, cls: Type, data: dict):
        """Convertit un dictionnaire en dataclass de manière récursive."""
        if not hasattr(cls, '__dataclass_fields__'):
            return data # Not a dataclass, return as is

        field_values = {}
        for field_name, field_type in cls.__dataclass_fields__.items():
            if field_name in data:
                value = data[field_name]
                if hasattr(field_type.type, '__dataclass_fields__'):
                    # Nested dataclass
                    field_values[field_name] = self._from_dict(field_type.type, value)
                elif getattr(field_type.type, '__origin__', None) is list:
                    # Handle List types
                    list_item_type = field_type.type.__args__[0]
                    field_values[field_name] = [self._from_dict(list_item_type, item) for item in value]
                else:
                    field_values[field_name] = value
            # else: field is missing, dataclasses will handle default values or raise error
        return cls(**field_values)

    def initiate_genesis_sequence(self):
        """Lance la séquence de genèse autonome d'AURA."""
        if not self.prompt_seminal:
            print("Le prompt séminal n'a pas été chargé. Veuillez appeler load_and_validate_prompt en premier.")
            return

        print("\n--- Lancement de la Séquence de Genèse Autonome ---")
        print(f"Instance AURA : {self.prompt_seminal.metadata.instance_name}")
        print(f"Mission : {self.prompt_seminal.mission_statement}")

        # Étape 1: Validation et Parsing (déjà fait par load_and_validate_prompt)

        # Étape 2: Activation du "Constructeur Initial" (cette classe elle-même)
        print("Activation du Constructeur Initial.")

        # Étape 3: Instanciation des Pôles Fondateurs
        print("Instanciation des Pôles Fondateurs...")
        
        # Création et enregistrement du messager
        self.messenger = AgentMessenger()

        # Instanciation de l'Agent DSI
        dsi_objectives = ["Construire l'infrastructure virtuelle interne.", "Assurer la sécurité des systèmes."]
        dsi_agent = DSIAgent("DSI_Agent_1", dsi_objectives)
        dsi_agent.set_messenger(self.messenger)
        self.messenger.register_agent(dsi_agent.agent_id)
        self.agents[dsi_agent.agent_id] = dsi_agent
        print(f"  - Agent DSI ({dsi_agent.agent_id}) créé et enregistré.")

        # Instanciation de l'Agent DRH
        drh_objectives = ["Préparer les fiches de poste pour les agents.", "Gérer le recrutement virtuel."]
        drh_agent = DRHAgent("DRH_Agent_1", drh_objectives)
        drh_agent.set_messenger(self.messenger)
        self.messenger.register_agent(drh_agent.agent_id)
        self.agents[drh_agent.agent_id] = drh_agent
        print(f"  - Agent DRH ({drh_agent.agent_id}) créé et enregistré.")

        # Simulation d'une interaction initiale
        print("\nSimulation d'une interaction initiale entre agents...")
        dsi_agent.act(dsi_agent.decide()) # DSI agit et envoie un message
        drh_agent.act(drh_agent.decide()) # DRH agit et envoie un message

        # Récupération et traitement des messages
        print("\nTraitement des messages en attente...")
        for agent_id, agent_instance in self.agents.items():
            received_messages = self.messenger.get_messages(agent_id)
            for msg in received_messages:
                agent_instance.receive_message(msg["sender"], msg["content"])

        # Étape 4: Déploiement en Cascade (simulé)
        print("\nDéploiement en Cascade des agents (simulation)...")
        print("  - Agent CEO créé.")
        print("  - Directeurs de pôles créés.")
        print("  - Équipes opérationnelles créées.")

        # Étape 5: Initialisation Opérationnelle (simulée)
        print("Initialisation opérationnelle des agents.")

        # Étape 6: Fin de la Genèse
        print("\n--- Genèse d'AURA terminée --- ")
        print(f"Instance {self.prompt_seminal.metadata.instance_name} créée et opérationnelle. Prête pour la phase de simulation.")