import os
import sys
import unittest
from unittest.mock import MagicMock

# Ajout du chemin racine du projet pour permettre les imports de 'src'
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
sys.path.insert(0, project_root)

from src.core.agents.concrete_agents import DocumentationAnalyzerAgent, DSIAgent
from src.core.agents.base_agent import AgentMessenger

class TestDocumentationAnalyzerAgent(unittest.TestCase):

    def setUp(self):
        """Mise en place de l'environnement de test."""
        self.messenger = AgentMessenger()
        self.project_root = project_root

        # Création de l'agent analyseur
        self.analyzer_agent = DocumentationAnalyzerAgent(
            agent_id="DocAnalyzer_1",
            objectives=["Maintain documentation consistency"],
            project_root=self.project_root
        )

        # Création d'un agent récepteur (DSI)
        self.receiver_agent = DSIAgent(
            agent_id="DSI_Agent_1",
            objectives=["Oversee technical operations"]
        )

        # Enregistrement des agents auprès du messager
        self.messenger.register_agent(self.analyzer_agent.agent_id)
        self.messenger.register_agent(self.receiver_agent.agent_id)

        # Injection du messager dans les agents
        self.analyzer_agent.set_messenger(self.messenger)
        self.receiver_agent.set_messenger(self.messenger)

    def test_agent_full_cycle(self):
        """
        Teste le cycle complet de l'agent : perceive, decide, act et communication.
        """
        print("\n--- Début du Test : Cycle Complet de l'Agent Analyseur ---")

        # On espionne la méthode receive_message de l'agent récepteur
        self.receiver_agent.receive_message = MagicMock()

        # --- Phase 1: L'agent analyseur agit ---
        decision = self.analyzer_agent.decide()
        self.analyzer_agent.act(decision)

        # --- Phase 2: Simulation de la boucle de l'agent récepteur ---
        # Dans un vrai système, un scheduler ferait ça. Ici, on le fait manuellement.
        messages = self.messenger.get_messages(self.receiver_agent.agent_id)
        for msg in messages:
            self.receiver_agent.receive_message(msg['sender'], msg['content'])

        # --- Phase 3: Vérification ---
        # Vérification que l'agent récepteur a bien été appelé (a reçu un message)
        self.receiver_agent.receive_message.assert_called_once()

        # On peut aussi vérifier le contenu du message reçu
        call_args = self.receiver_agent.receive_message.call_args
        sender_id, message = call_args[0]

        self.assertEqual(sender_id, self.analyzer_agent.agent_id)
        self.assertIn("type", message)
        self.assertEqual(message["type"], "documentation_analysis_report")
        self.assertIn("issues_found", message)
        
        print(f"Rapport reçu par {self.receiver_agent.agent_id}:")
        print(f"  de: {sender_id}")
        print(f"  contenu: {message}")
        print("--- Fin du Test ---")


if __name__ == '__main__':
    unittest.main()
