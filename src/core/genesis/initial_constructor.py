import yaml
from dataclasses import asdict
from typing import Type

from src.core.genesis.prompt_schema import PromptSeminal

class InitialConstructor:
    def __init__(self, prompt_file_path: str):
        self.prompt_file_path = prompt_file_path
        self.prompt_seminal: PromptSeminal = None

    def load_and_validate_prompt(self) -> PromptSeminal:
        """Charge et valide le fichier YAML du prompt séminal."""
        try:
            with open(self.prompt_file_path, 'r', encoding='utf-8') as f:
                raw_data = yaml.safe_load(f)
            
            # Valider les données brutes avec le schéma PromptSeminal
            # Cela nécessite une bibliothèque de validation comme Pydantic ou Marshmallow
            # Pour l'ébauche, nous allons simplement tenter de construire l'objet dataclass
            # et nous fier aux erreurs de type si les données ne correspondent pas.
            
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
        # Ici, nous aurions la logique pour créer les agents DSI, DRH, etc.
        # Pour l'ébauche, nous allons simuler leur création.
        print("  - Agent DSI (CIO) créé.")
        print("  - Agent DRH (CHRO) créé.")

        # Étape 4: Déploiement en Cascade (simulé)
        print("Déploiement en Cascade des agents...")
        print("  - Agent CEO créé.")
        print("  - Directeurs de pôles créés.")
        print("  - Équipes opérationnelles créées.")

        # Étape 5: Initialisation Opérationnelle (simulée)
        print("Initialisation opérationnelle des agents.")

        # Étape 6: Fin de la Genèse
        print("\n--- Genèse d'AURA terminée --- ")
        print(f"Instance {self.prompt_seminal.metadata.instance_name} créée et opérationnelle. Prête pour la phase de simulation.")

# Exemple d'utilisation (à exécuter dans un script séparé pour tester)
# if __name__ == "__main__":
#     # Créez un fichier prompt-seminal.yaml pour tester
#     # Exemple de contenu :
#     # metadata:
#     #   instance_name: "TestAURA"
#     #   prompt_schema_version: 1.0
#     # mission_statement: "Tester la genèse."
#     # market_analysis:
#     #   sector: "Test"
#     #   target_customer: "Test Customer"
#     #   key_competitors: ["Comp1"]
#     #   market_trends: ["Trend1"]
#     # initial_strategy:
#     #   business_model: "Test Model"
#     #   go_to_market: "Test Go To Market"
#     #   brand_positioning: "Test Brand"
#     # ethical_charter:
#     #   - "Rule 1"
#     # initial_resources:
#     #   virtual_capital: 1000
#     #   agent_workforce_template: "Test Template"
#     # self_improvement_parameters:
#     #   primary_directive: "efficiency"
#     #   evolution_aggressiveness: 0.5
#     #   learning_scope: ["code_optimization"]
#     #   feedback_loops: ["digital_twin_performance"]
#
#     constructor = InitialConstructor("path/to/your/prompt-seminal.yaml")
#     try:
#         constructor.load_and_validate_prompt()
#         constructor.initiate_genesis_sequence()
#     except Exception as e:
#         print(f"La genèse a échoué: {e}")