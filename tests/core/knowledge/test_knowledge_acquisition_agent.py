import pytest
from unittest.mock import MagicMock, patch
import requests # Ajout de l'import requests
from src.core.knowledge.knowledge_acquisition_agent import KnowledgeAcquisitionAgent
from src.core.knowledge.knowledge_base import KnowledgeBase

@pytest.fixture
def mock_knowledge_base():
    """Mock de la KnowledgeBase pour les tests."""
    mock_kb = MagicMock(spec=KnowledgeBase)
    mock_kb.add_document.return_value = None
    return mock_kb

@pytest.fixture
def mock_requests_get():
    """Mock de requests.get pour simuler les réponses web."""
    with patch('requests.get') as mock_get:
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.raise_for_status.return_value = None
        mock_response.text = "<html><body><p>Ceci est un article sur les dernières avancées en IA.</p></body></html>"
        mock_get.return_value = mock_response
        yield mock_get

def test_knowledge_acquisition_agent_init(mock_knowledge_base):
    agent = KnowledgeAcquisitionAgent("KA_Agent_1", ["Acquérir des connaissances"], mock_knowledge_base)
    assert agent.agent_id == "KA_Agent_1"
    assert agent.role == "KnowledgeAcquisition"
    assert agent.knowledge_base == mock_knowledge_base

def test_knowledge_acquisition_agent_perceive(mock_knowledge_base):
    agent = KnowledgeAcquisitionAgent("KA_Agent_1", ["Acquérir des connaissances"], mock_knowledge_base)
    perception = agent.perceive()
    assert perception["type"] == "search_request"
    assert perception["query"] == "dernières avancées en IA"

def test_knowledge_acquisition_agent_decide(mock_knowledge_base):
    agent = KnowledgeAcquisitionAgent("KA_Agent_1", ["Acquérir des connaissances"], mock_knowledge_base)
    decision = agent.decide()
    assert decision["action"] == "fetch_web_content"
    assert decision["query"] == "dernières avancées en IA"
    assert "example.com" in decision["url"]

def test_knowledge_acquisition_agent_act_success(mock_knowledge_base, mock_requests_get):
    agent = KnowledgeAcquisitionAgent("KA_Agent_1", ["Acquérir des connaissances"], mock_knowledge_base)
    mock_messenger = MagicMock() # Créer un mock spécifique pour le messager
    agent.set_messenger(mock_messenger)
    
    action = {"action": "fetch_web_content", "query": "dernières avancées en IA", "url": "https://example.com/ai-news"}
    agent.act(action)
    
    mock_requests_get.assert_called_once_with("https://example.com/ai-news", timeout=10)
    mock_knowledge_base.add_document.assert_called_once()
    args, kwargs = mock_knowledge_base.add_document.call_args
    assert "Ceci est un article sur les dernières avancées en IA." in args[1]
    assert args[2]["source_url"] == "https://example.com/ai-news"
    assert mock_messenger.send_message.called # Asserter sur la m�thode send_message du mock sp�cifique

def test_knowledge_acquisition_agent_act_http_error(mock_knowledge_base, mock_requests_get):
    agent = KnowledgeAcquisitionAgent("KA_Agent_1", ["Acquérir des connaissances"], mock_knowledge_base)
    mock_messenger = MagicMock()
    agent.set_messenger(mock_messenger)
    
    mock_requests_get.return_value.raise_for_status.side_effect = requests.exceptions.HTTPError("404 Not Found")
    
    action = {"action": "fetch_web_content", "query": "erreur test", "url": "https://example.com/error"}
    agent.act(action)
    
    mock_requests_get.assert_called_once_with("https://example.com/error", timeout=10)
    mock_knowledge_base.add_document.assert_not_called()
    assert not mock_messenger.communicate.called

def test_knowledge_acquisition_agent_act_request_exception(mock_knowledge_base, mock_requests_get):
    agent = KnowledgeAcquisitionAgent("KA_Agent_1", ["Acquérir des connaissances"], mock_knowledge_base)
    mock_messenger = MagicMock()
    agent.set_messenger(mock_messenger)
    
    mock_requests_get.side_effect = requests.exceptions.ConnectionError("Connection timed out")
    
    action = {"action": "fetch_web_content", "query": "timeout test", "url": "https://example.com/timeout"}
    agent.act(action)
    
    mock_requests_get.assert_called_once_with("https://example.com/timeout", timeout=10)
    mock_knowledge_base.add_document.assert_not_called()
    assert not mock_messenger.communicate.called

def test_knowledge_acquisition_agent_act_idle(mock_knowledge_base):
    agent = KnowledgeAcquisitionAgent("KA_Agent_1", ["Acquérir des connaissances"], mock_knowledge_base)
    mock_messenger = MagicMock()
    agent.set_messenger(mock_messenger)
    
    action = {"action": "idle"}
    agent.act(action)
    
    mock_knowledge_base.add_document.assert_not_called()
    assert not mock_messenger.communicate.called