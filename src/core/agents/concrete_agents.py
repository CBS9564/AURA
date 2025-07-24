from src.core.agents.base_agent import BaseAgent, AgentMessenger
from typing import Any, Dict, List
import os
import re
import logging

# Import de l'analyseur de documentation du module de méta-cognition
from src.core.meta_cognition.documentation_analyzer import DocumentationAnalyzer


class DSIAgent(BaseAgent):
    def __init__(self, agent_id: str, objectives: List[str]):
        super().__init__(agent_id, "DSI", objectives)
        self.knowledge = {}
        self.pending_correction_task = None # Suit la tâche de correction active
        logging.info(f"Agent DSI {self.agent_id} initialisé avec les objectifs : {self.objectives})")

    def perceive(self) -> Any:
        """Le DSI perçoit les messages qui lui sont adressés."""
        return self.knowledge

    def decide(self) -> Any:
        """Le DSI décide des actions à entreprendre en fonction des rapports reçus."""
        # Priorité 1: Traiter un rapport d'analyse s'il n'y a pas de correction en cours
        if "last_report" in self.knowledge and not self.pending_correction_task:
            report = self.knowledge.pop("last_report")
            if report.get("type") == "documentation_analysis_report" and report.get("issues_found", 0) > 0:
                undocumented_files = [issue for issue in report["issues"] if "Fichier non documenté" in issue]
                if undocumented_files:
                    filename_to_fix = re.search(r"\'(.*?)\'", undocumented_files[0]).group(1)
                    
                    logging.info(f"Agent {self.agent_id} a détecté un fichier non documenté '{filename_to_fix}' et décide de déléguer la correction.")
                    self.pending_correction_task = filename_to_fix # Marque la tâche comme active
                    return {
                        "action": "delegate_documentation_correction",
                        "target_agent": "DocCorrector_1",
                        "file_to_document": filename_to_fix
                    }
        
        # Priorité 2: Surveillance standard
        logging.info(f"Agent {self.agent_id} décide de continuer la surveillance standard.")
        return {"action": "monitor_infrastructure"}

    def act(self, action: Any):
        """Le DSI exécute l'action décidée."""
        if action.get("action") == "delegate_documentation_correction":
            logging.info(f"Agent {self.agent_id} délègue la tâche de correction pour le fichier {action['file_to_document']}.")
            task = {
                "type": "correction_task",
                "file_to_add": action['file_to_document'],
                "target_doc": "docs/02_SYSTEM_ARCHITECTURE.md"
            }
            self.communicate(action['target_agent'], task)
        
        elif action.get("action") == "monitor_infrastructure":
            logging.info(f"Agent {self.agent_id} exécute la surveillance de l'infrastructure.")
            self.communicate("DRH_Agent_1", {"type": "report", "content": "Infrastructure stable."})

    def receive_message(self, sender_id: str, message: Dict[str, Any]):
        """Le DSI reçoit des messages et met à jour sa base de connaissances."""
        msg_type = message.get("type")
        logging.info(f"Agent {self.agent_id} a reçu un message de {sender_id}: {msg_type}")
        
        if msg_type == "documentation_analysis_report":
            self.knowledge["last_report"] = message
        elif msg_type == "correction_report" and message.get("status") == "success":
            # La tâche est terminée, on peut la retirer des tâches en cours
            corrected_file = re.search(r"Fichier (.*?) ajouté", message["details"]).group(1)
            if corrected_file == self.pending_correction_task:
                logging.info(f"Agent {self.agent_id} a reçu confirmation de la correction pour '{corrected_file}'. Tâche terminée.")
                self.pending_correction_task = None
        else:
            pass

class DRHAgent(BaseAgent):
    def __init__(self, agent_id: str, objectives: List[str]):
        super().__init__(agent_id, "DRH", objectives)
        logging.info(f"Agent DRH {self.agent_id} initialisé avec les objectifs : {self.objectives}")

    def perceive(self) -> Any:
        return "Workforce needs: Low"

    def decide(self) -> Any:
        return {"action": "review_workforce_template"}

    def act(self, action: Any):
        if action.get("action") == "review_workforce_template":
            logging.info(f"Agent {self.agent_id} exécute l'action : {action}")
            self.communicate("DSI_Agent_1", {"type": "request", "content": "Besoin de ressources pour nouveau projet?"})

class DocumentationAnalyzerAgent(BaseAgent):
    """Agent spécialisé dans l'analyse de la cohérence de la documentation."""
    def __init__(self, agent_id: str, objectives: List[str], project_root: str):
        super().__init__(agent_id, "DocumentationAnalyzer", objectives)
        self.project_root = project_root
        self.analyzer = DocumentationAnalyzer(self.project_root)
        logging.info(f"Agent Analyseur de Documentation {self.agent_id} initialisé.")

    def perceive(self) -> Any:
        return {"trigger": "scheduled_analysis"}

    def decide(self) -> Any:
        if self.perceive().get("trigger") == "scheduled_analysis":
            return {"action": "run_analysis"}
        return {"action": "idle"}

    def act(self, action: Any):
        if action.get("action") == "run_analysis":
            logging.info(f"Agent {self.agent_id} exécute l'analyse de la documentation...")
            issues = self.analyzer.analyze()
            report = {"type": "documentation_analysis_report", "status": "completed", "issues_found": len(issues), "issues": issues}
            self.communicate("DSI_Agent_1", report)
            logging.info(f"Agent {self.agent_id} a terminé l'analyse et envoyé son rapport.")
        elif action.get("action") == "idle":
            logging.info(f"Agent {self.agent_id} est en veille.")

class DocumentationCorrectorAgent(BaseAgent):
    """Agent spécialisé dans la correction de la documentation."""
    def __init__(self, agent_id: str, objectives: List[str], project_root: str):
        super().__init__(agent_id, "DocumentationCorrector", objectives)
        self.project_root = project_root
        self.tasks = []
        logging.info(f"Agent Correcteur de Documentation {self.agent_id} initialisé.")

    def perceive(self) -> Any:
        return self.tasks

    def decide(self) -> Any:
        if self.tasks:
            task = self.tasks.pop(0) # Prend la première tâche
            logging.info(f"Agent {self.agent_id} a une nouvelle tâche de correction : {task}")
            return {"action": "fix_documentation", "task_details": task}
        return {"action": "idle"}

    def act(self, action: Any):
        if action.get("action") == "fix_documentation":
            details = action["task_details"]
            file_to_add = details["file_to_add"]
            target_doc_path = os.path.join(self.project_root, details["target_doc"])
            
            logging.info(f"Agent {self.agent_id} corrige la documentation : ajout de '{file_to_add}' dans '{target_doc_path}'.")
            
            try:
                with open(target_doc_path, 'a', encoding='utf-8') as f:
                    f.write(f"\n\n*   **{file_to_add} (auto-généré)** : Mention auto-générée par l'agent correcteur pour assurer la cohérence documentation-code.")
                
                report = {"type": "correction_report", "status": "success", "details": f"Fichier {file_to_add} ajouté à {details['target_doc']}"}
                self.communicate("DSI_Agent_1", report)

            except Exception as e:
                logging.error(f"Erreur lors de la correction de la documentation par l'agent {self.agent_id}: {e}")
                report = {"type": "correction_report", "status": "failure", "details": str(e)}
                self.communicate("DSI_Agent_1", report)

        elif action.get("action") == "idle":
            logging.info(f"Agent {self.agent_id} est en veille.")

    def receive_message(self, sender_id: str, message: Dict[str, Any]):
        logging.info(f"Agent {self.agent_id} a reçu une tâche de {sender_id}.")
        if message.get("type") == "correction_task":
            self.tasks.append(message)
