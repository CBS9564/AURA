from src.core.agents.base_agent import BaseAgent, AgentMessenger
from typing import Any, Dict, List

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
