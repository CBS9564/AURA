from src.core.agents.base_agent import BaseAgent
from src.core.knowledge.knowledge_base import KnowledgeBase
from typing import Any, Dict, List, Optional
import requests
from bs4 import BeautifulSoup
import logging

# Configuration du logging
logging.basicConfig(level=logging.INFO, format='[%(asctime)s] %(levelname)s: %(message)s')

class KnowledgeAcquisitionAgent(BaseAgent):
    """Agent spécialisé dans l'acquisition de connaissances depuis des sources externes (ex: web)."""

    def __init__(self, agent_id: str, objectives: List[str], knowledge_base: KnowledgeBase):
        super().__init__(agent_id, "KnowledgeAcquisition", objectives)
        self.knowledge_base = knowledge_base
        logging.info(f"Agent d'Acquisition de Connaissances {self.agent_id} initialisé.")

    def perceive(self) -> Any:
        """Perçoit les besoins en information ou les sources à explorer."""
        logging.info(f"Agent {self.agent_id} perçoit les besoins en information.")
        # Pour l'ébauche, simule un besoin de recherche sur un sujet spécifique
        return {"type": "search_request", "query": "dernières avancées en IA", "source_type": "web"}

    def decide(self) -> Any:
        """Décide de la stratégie d'acquisition de connaissances."""
        perception = self.perceive()
        if perception and perception["type"] == "search_request":
            logging.info(f"Agent {self.agent_id} décide de rechercher sur le web pour: {perception["query"]}")
            return {"action": "fetch_web_content", "query": perception["query"], "url": "https://example.com/ai-news"} # URL d'exemple
        return {"action": "idle"}

    def act(self, action: Any):
        """Exécute l'action d'acquisition de connaissances."""
        if action["action"] == "fetch_web_content":
            query = action["query"]
            url = action["url"]
            logging.info(f"Agent {self.agent_id} tente de récupérer le contenu de {url} pour '{query}'.")
            try:
                response = requests.get(url, timeout=10) # Timeout pour éviter les blocages
                response.raise_for_status() # Lève une exception pour les codes d'erreur HTTP
                soup = BeautifulSoup(response.text, 'html.parser')
                # Pour l'ébauche, extraire un paragraphe simple
                content = soup.find('p').get_text() if soup.find('p') else "Contenu non trouvé."
                doc_id = f"web_content_{hash(url)}"
                self.knowledge_base.add_document(doc_id, content, {"source_url": url, "query": query})
                logging.info(f"Contenu de '{url}' acquis et ajouté à la base de connaissance.")
                self.communicate("DSI_Agent_1", {"type": "knowledge_acquired", "topic": query, "url": url}) # Exemple de communication
            except requests.exceptions.RequestException as e:
                logging.error(f"Erreur lors de la récupération de {url}: {e}")
            except Exception as e:
                logging.error(f"Erreur inattendue lors de l'acquisition de connaissances: {e}")
        elif action["action"] == "idle":
            logging.info(f"Agent {self.agent_id} est en veille.")

