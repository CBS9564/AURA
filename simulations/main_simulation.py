import os
import sys
import logging

# Configuration du logging pour la simulation
logging.basicConfig(level=logging.INFO, format='[%(asctime)s] [%(levelname)s] [%(name)s] %(message)s')

# Ajout du chemin racine du projet pour permettre les imports de 'src'
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, project_root)

from src.core.agents.agent_scheduler import AgentScheduler
from src.core.agents.base_agent import AgentMessenger
from src.core.agents.concrete_agents import DSIAgent, DRHAgent, DocumentationAnalyzerAgent

def main():
    """
    Point d'entrée principal pour lancer une simulation AURA.
    """
    log = logging.getLogger("MainSimulation")
    log.info("Initialisation de l'environnement de simulation AURA...")

    # 1. Création des composants de base
    messenger = AgentMessenger()
    scheduler = AgentScheduler(messenger)

    # 2. Création et enregistrement des agents
    log.info("Instanciation des agents...")
    
    dsi_agent = DSIAgent(
        agent_id="DSI_Agent_1",
        objectives=["Superviser l'infrastructure technique et la cohérence du projet."]
    )
    
    drh_agent = DRHAgent(
        agent_id="DRH_Agent_1",
        objectives=["Gérer les ressources humaines (agents)."]
    )
    
    doc_analyzer_agent = DocumentationAnalyzerAgent(
        agent_id="DocAnalyzer_1",
        objectives=["Maintenir la cohérence de la documentation."],
        project_root=project_root
    )

    scheduler.register_agent(dsi_agent)
    scheduler.register_agent(drh_agent)
    scheduler.register_agent(doc_analyzer_agent)

    # 3. Lancement de la simulation
    num_cycles = 3 # Nombre de cycles à simuler
    log.info(f"L'environnement est prêt. Lancement de la simulation pour {num_cycles} cycles.")
    
    scheduler.run_simulation(num_cycles=num_cycles, cycle_delay=2)

    log.info("Fin du script de simulation.")

if __name__ == "__main__":
    main()
