from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional

class BaseAgent(ABC):
    """Classe de base abstraite pour tous les agents d'AURA."""

    def __init__(self, agent_id: str, role: str, objectives: List[str]):
        self.agent_id = agent_id
        self.role = role
        self.objectives = objectives
        self.memory: Dict[str, Any] = {}
        self.messenger: Optional[AgentMessenger] = None # Sera injecté par la plateforme

    def set_messenger(self, messenger: 'AgentMessenger'):
        self.messenger = messenger

    @abstractmethod
    def perceive(self) -> Any:
        """Méthode abstraite pour la perception de l'environnement ou des messages."""
        pass

    @abstractmethod
    def decide(self) -> Any:
        """Méthode abstraite pour la prise de décision de l'agent."""
        pass

    @abstractmethod
    def act(self, action: Any):
        """Méthode abstraite pour l'exécution d'une action par l'agent."""
        pass

    def communicate(self, recipient_id: str, message: Dict[str, Any]):
        """Envoie un message à un autre agent via le messager."""
        if self.messenger:
            self.messenger.send_message(self.agent_id, recipient_id, message)
        else:
            print(f"Agent {self.agent_id}: Messager non configuré. Impossible d'envoyer le message.")

    def receive_message(self, sender_id: str, message: Dict[str, Any]):
        """Reçoit un message d'un autre agent."""
        print(f"Agent {self.agent_id} a reçu un message de {sender_id}: {message}")
        # Ici, l'agent traiterait le message, mettrait à jour sa mémoire, etc.


class AgentMessenger:
    """Messager simple en mémoire pour la communication inter-agents."""
    def __init__(self):
        self.message_queues: Dict[str, List[Dict[str, Any]]] = {}

    def register_agent(self, agent_id: str):
        """Enregistre un agent pour qu'il puisse recevoir des messages."""
        if agent_id not in self.message_queues:
            self.message_queues[agent_id] = []
            print(f"Messager: Agent {agent_id} enregistré.")

    def send_message(self, sender_id: str, recipient_id: str, message: Dict[str, Any]):
        """Envoie un message à la file d'attente d'un destinataire."""
        if recipient_id in self.message_queues:
            full_message = {"sender": sender_id, "content": message}
            self.message_queues[recipient_id].append(full_message)
            print(f"Messager: Message de {sender_id} à {recipient_id} ajouté à la file.")
        else:
            print(f"Messager: Destinataire {recipient_id} non enregistré. Message non envoyé.")

    def get_messages(self, agent_id: str) -> List[Dict[str, Any]]:
        """Récupère tous les messages en attente pour un agent."""
        messages = self.message_queues.get(agent_id, [])
        self.message_queues[agent_id] = [] # Vide la file après récupération
        return messages

