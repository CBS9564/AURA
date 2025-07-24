from src.core.agents.base_agent import BaseAgent, AgentMessenger
from typing import Any, Dict, List
import os
import re
import logging
import glob

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
    """
    Agent spécialisé dans la correction intelligente de la documentation.
    Il insère les mentions de fichiers au bon endroit dans le document d'architecture.
    """
    def __init__(self, agent_id: str, objectives: List[str], project_root: str):
        super().__init__(agent_id, "DocumentationCorrector", objectives)
        self.project_root = project_root
        self.tasks = []
        self.module_mapping = {
            "genesis": "## 2. Module 1 : Moteur Cognitif & Personas IA",
            "agents": "## 3. Module 2 : Plateforme Multi-Agents & Communication",
            "knowledge": "## 4. Module 3 : Noyau Fonctionnel d'Entreprise",
            "meta_cognition": "## 6. Module 5 : Méta-Cognition & Auto-Amélioration"
        }
        logging.info(f"Agent Correcteur de Documentation {self.agent_id} initialisé avec une logique contextuelle.")

    def perceive(self) -> Any:
        return self.tasks

    def decide(self) -> Any:
        if self.tasks:
            task = self.tasks.pop(0)
            logging.info(f"Agent {self.agent_id} a une nouvelle tâche de correction contextuelle : {task}")
            return {"action": "fix_documentation_contextually", "task_details": task}
        return {"action": "idle"}

    def _get_module_from_filename(self, filename: str) -> str:
        """Détermine le module architectural à partir du nom de fichier."""
        # Cas spécifiques pour les fichiers à la racine de 'agents'
        if filename in ["agent_scheduler.py", "base_agent.py", "concrete_agents.py"]:
            return "agents"
        # Cas général basé sur le sous-répertoire
        for key in self.module_mapping.keys():
            if f"/{key}/" in filename.replace("\\", "/"):
                return key
        return None

    def act(self, action: Any):
        if action.get("action") == "fix_documentation_contextually":
            details = action["task_details"]
            file_to_add = details["file_to_add"]
            target_doc_path = os.path.join(self.project_root, details["target_doc"])
            
            logging.info(f"Agent {self.agent_id} commence la correction contextuelle pour '{file_to_add}'.")

            try:
                # 1. Déterminer le module cible
                # Pour obtenir le chemin complet, on doit le chercher (c'est une simplification pour l'instant)
                # Idéalement, l'analyseur fournirait le chemin complet.
                # On simule cette recherche pour la démo.
                potential_path = glob.glob(os.path.join(self.project_root, 'src', '**', file_to_add), recursive=True)
                if not potential_path:
                    raise FileNotFoundError(f"Impossible de trouver le chemin pour {file_to_add}")
                
                module_key = self._get_module_from_filename(potential_path[0])
                if not module_key:
                    raise ValueError(f"Impossible de déterminer le module pour {file_to_add}")

                target_section_header = self.module_mapping[module_key]
                
                # 2. Lire le document et insérer au bon endroit
                with open(target_doc_path, 'r', encoding='utf-8') as f:
                    lines = f.readlines()

                new_content = f"*   **{file_to_add}** : Mention auto-générée par l'agent correcteur.\n"
                
                # Trouver la section et le marqueur d'insertion
                section_start_index = -1
                insertion_index = -1
                
                for i, line in enumerate(lines):
                    if line.strip() == target_section_header:
                        section_start_index = i
                        continue
                    
                    # Une fois dans la bonne section, chercher le marqueur de fin
                    if section_start_index != -1 and "<!-- FIN DES COMPOSANTS -->" in line:
                        insertion_index = i
                        break
                
                if insertion_index == -1:
                     raise ValueError(f"Impossible de trouver le point d'insertion (marqueur) dans la section '{target_section_header}'")

                lines.insert(insertion_index, new_content)

                # 3. Écrire le nouveau contenu
                with open(target_doc_path, 'w', encoding='utf-8') as f:
                    f.writelines(lines)

                logging.info(f"Correction réussie. '{file_to_add}' a été ajouté à la section '{target_section_header}'.")
                report = {"type": "correction_report", "status": "success", "details": f"Fichier {file_to_add} ajouté à {details['target_doc']}"}
                self.communicate("DSI_Agent_1", report)

            except Exception as e:
                logging.error(f"Erreur lors de la correction contextuelle par l'agent {self.agent_id}: {e}")
                report = {"type": "correction_report", "status": "failure", "details": str(e)}
                self.communicate("DSI_Agent_1", report)

        elif action.get("action") == "idle":
            logging.info(f"Agent {self.agent_id} est en veille.")

    def receive_message(self, sender_id: str, message: Dict[str, Any]):
        logging.info(f"Agent {self.agent_id} a reçu une tâche de {sender_id}.")
        if message.get("type") == "correction_task":
            self.tasks.append(message)
