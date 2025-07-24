from src.core.agents.base_agent import BaseAgent, AgentMessenger
from typing import Any, Dict, List
import os

# Import de l'analyseur de documentation du module de méta-cognition
from src.core.meta_cognition.documentation_analyzer import DocumentationAnalyzer


class DSIAgent(BaseAgent):
    def __init__(self, agent_id: str, objectives: List[str]):
        super().__init__(agent_id, "DSI", objectives)
        print(f"Agent DSI {self.agent_id} initialisé avec les objectifs : {self.objectives}")

    def perceive(self) -> Any:
        print(f"Agent DSI {self.agent_id} perçoit son environnement.")
        # Logique de perception spécifique au DSI
        return "Infrastructure status: OK"

    def decide(self) -> Any:
        print(f"Agent DSI {self.agent_id} prend une décision.")
        # Logique de décision spécifique au DSI
        return {"action": "monitor_infrastructure", "details": "Check server logs"}

    def act(self, action: Any):
        print(f"Agent DSI {self.agent_id} exécute l'action : {action}")
        # Logique d'action spécifique au DSI
        if action.get("action") == "monitor_infrastructure":
            print("Simule la surveillance de l'infrastructure.")
            # Exemple de communication après une action
            self.communicate("DRH_Agent_1", {"type": "report", "content": "Infrastructure stable."})

class DRHAgent(BaseAgent):
    def __init__(self, agent_id: str, objectives: List[str]):
        super().__init__(agent_id, "DRH", objectives)
        print(f"Agent DRH {self.agent_id} initialisé avec les objectifs : {self.objectives}")

    def perceive(self) -> Any:
        print(f"Agent DRH {self.agent_id} perçoit son environnement.")
        # Logique de perception spécifique au DRH
        return "Workforce needs: Low"

    def decide(self) -> Any:
        print(f"Agent DRH {self.agent_id} prend une décision.")
        # Logique de décision spécifique au DRH
        return {"action": "review_workforce_template", "details": "Check agent_workforce_template"}

    def act(self, action: Any):
        print(f"Agent DRH {self.agent_id} exécute l'action : {action}")
        # Logique d'action spécifique au DRH
        if action.get("action") == "review_workforce_template":
            print("Simule la révision du modèle de main-d'œuvre.")
            # Exemple de communication après une action
            self.communicate("DSI_Agent_1", {"type": "request", "content": "Besoin de ressources pour nouveau projet?"})

class DocumentationAnalyzerAgent(BaseAgent):
    """
    Agent spécialisé dans l'analyse de la cohérence de la documentation du projet.
    """
    def __init__(self, agent_id: str, objectives: List[str], project_root: str):
        super().__init__(agent_id, "DocumentationAnalyzer", objectives)
        self.project_root = project_root
        self.analyzer = DocumentationAnalyzer(self.project_root)
        print(f"Agent Analyseur de Documentation {self.agent_id} initialisé.")

    def perceive(self) -> Any:
        """La perception peut être déclenchée par un timer, un webhook, ou une commande directe."""
        print(f"Agent {self.agent_id} perçoit une demande d'analyse de la documentation.")
        # Pour cette version, on simule un déclenchement systématique.
        return {"trigger": "scheduled_analysis"}

    def decide(self) -> Any:
        """Décide de lancer l'analyse."""
        perception = self.perceive()
        if perception.get("trigger") == "scheduled_analysis":
            print(f"Agent {self.agent_id} décide de lancer une analyse complète.")
            return {"action": "run_analysis"}
        return {"action": "idle"}

    def act(self, action: Any):
        """Exécute l'analyse et communique les résultats."""
        if action.get("action") == "run_analysis":
            print(f"Agent {self.agent_id} exécute l'analyse de la documentation...")
            issues = self.analyzer.analyze()
            
            report = {
                "type": "documentation_analysis_report",
                "status": "completed",
                "issues_found": len(issues),
                "issues": issues
            }
            
            # L'agent communique le rapport à un agent superviseur (ex: DSI)
            # ou à un canal de logging central.
            self.communicate("DSI_Agent_1", report)
            print(f"Agent {self.agent_id} a terminé l'analyse et envoyé son rapport.")
        
        elif action.get("action") == "idle":
            print(f"Agent {self.agent_id} est en veille.")
