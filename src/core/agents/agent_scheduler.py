from typing import List
import time
import logging

from src.core.agents.base_agent import BaseAgent, AgentMessenger

# Configuration du logging
logging.basicConfig(level=logging.INFO, format='[%(asctime)s] [%(levelname)s] %(message)s')

class AgentScheduler:
    """
    Orchestre le cycle de vie et la communication des agents dans le système AURA.
    """

    def __init__(self, messenger: AgentMessenger):
        self.agents: List[BaseAgent] = []
        self.messenger = messenger
        logging.info("Le Scheduler d'Agents a été initialisé.")

    def register_agent(self, agent: BaseAgent):
        """
        Enregistre un agent auprès du scheduler et du messager.
        """
        if agent not in self.agents:
            self.agents.append(agent)
            self.messenger.register_agent(agent.agent_id)
            agent.set_messenger(self.messenger)
            logging.info(f"Agent {agent.agent_id} ({agent.role}) enregistré auprès du scheduler.")

    def run_simulation_cycle(self):
        """
        Exécute un cycle complet de la simulation pour tous les agents enregistrés.
        """
        logging.info("--- Début du cycle de simulation ---")

        # 1. Phase de Perception, Décision, Action pour chaque agent
        for agent in self.agents:
            logging.info(f"Activation du cycle P-D-A pour l'agent {agent.agent_id}.")
            try:
                decision = agent.decide() # La perception est souvent appelée dans la décision
                agent.act(decision)
            except Exception as e:
                logging.error(f"Erreur durant le cycle P-D-A de l'agent {agent.agent_id}: {e}")

        # 2. Phase de Communication (distribution des messages)
        logging.info("Distribution des messages en attente...")
        for agent in self.agents:
            try:
                messages = self.messenger.get_messages(agent.agent_id)
                if messages:
                    logging.info(f"{len(messages)} message(s) en attente pour {agent.agent_id}.")
                for msg in messages:
                    agent.receive_message(msg['sender'], msg['content'])
            except Exception as e:
                logging.error(f"Erreur durant la réception de message pour l'agent {agent.agent_id}: {e}")
        
        logging.info("--- Fin du cycle de simulation ---\n")

    def run_simulation(self, num_cycles: int, cycle_delay: float = 1.0):
        """
        Lance la simulation complète pour un nombre de cycles donné.

        Args:
            num_cycles (int): Le nombre de cycles à exécuter.
            cycle_delay (float): Le temps d'attente en secondes entre chaque cycle.
        """
        logging.info(f"Lancement de la simulation pour {num_cycles} cycle(s).")
        for i in range(num_cycles):
            print(f"\n==================== CYCLE {i + 1}/{num_cycles} ====================")
            self.run_simulation_cycle()
            if i < num_cycles - 1:
                time.sleep(cycle_delay)
        logging.info("Simulation terminée.")
