import pytest
import chromadb
from unittest.mock import MagicMock
from src.core.knowledge.knowledge_base import KnowledgeBase

# Mock embedding function for deterministic tests
class MockEmbeddingFunction:
    def __call__(self, texts: list[str]) -> list[list[float]]:
        embeddings = []
        for text in texts:
            # Assign distinct, predictable vectors to specific keywords/phrases
            if "intelligence artificielle" in text or "qu'est-ce que l'IA ?" in text:
                embeddings.append([1.0, 0.0, 0.0]) # Vector for IA concepts
            elif "apprentissage automatique" in text:
                embeddings.append([0.9, 0.1, 0.0]) # Slightly different for ML
            elif "robots" in text:
                embeddings.append([0.0, 1.0, 0.0]) # Vector for Robotics
            elif "premier document" in text:
                embeddings.append([0.0, 0.0, 1.0]) # Vector for doc1
            elif "Nouveau contenu" in text:
                embeddings.append([0.5, 0.5, 0.5]) # Vector for updated content
            elif "Contenu original" in text:
                embeddings.append([0.4, 0.4, 0.4]) # Vector for original content
            else:
                embeddings.append([0.0, 0.0, 0.0]) # Default for irrelevant/empty queries
        return embeddings

@pytest.fixture(scope="function")
def setup_knowledge_base():
    """Fixture pour initialiser la base de connaissance de test en mémoire avec un mock d'embedding."""
    # Utilise le mode in_memory pour les tests unitaires
    kb = KnowledgeBase(in_memory=True, collection_name="test_collection")
    kb.embedding_function = MockEmbeddingFunction() # Override the embedding function
    yield kb
    # Le nettoyage est géré par le mode in_memory et la portée de la fixture

def test_add_document(setup_knowledge_base):
    kb = setup_knowledge_base
    doc_id = "doc1"
    content = "Ceci est le premier document sur l'IA."
    metadata = {"source": "test_file", "page": 1}

    kb.add_document(doc_id, content, metadata)

    retrieved_doc = kb.get_document_by_id(doc_id)
    assert retrieved_doc is not None
    assert retrieved_doc["document"] == content
    assert retrieved_doc["metadata"] == metadata

def test_query_documents(setup_knowledge_base):
    kb = setup_knowledge_base
    kb.add_document("doc_ia", "L'intelligence artificielle est un domaine fascinant.", {"topic": "IA"})
    kb.add_document("doc_ml", "L'apprentissage automatique est une branche de l'IA.", {"topic": "ML"})
    kb.add_document("doc_robot", "Les robots utilisent souvent l'IA.", {"topic": "Robotique"})

    # La requête pour "qu'est-ce que l'IA ?" devrait retourner des documents liés à l'IA/ML
    results = kb.query_documents("qu'est-ce que l'IA ?", n_results=2)
    assert len(results) == 2
    
    returned_documents = {r["document"] for r in results}
    assert "L'intelligence artificielle est un domaine fascinant." in returned_documents
    assert "L'apprentissage automatique est une branche de l'IA." in returned_documents

def test_empty_query(setup_knowledge_base):
    kb = setup_knowledge_base
    results = kb.query_documents("rien", n_results=1)
    assert len(results) == 0

def test_add_duplicate_id(setup_knowledge_base):
    kb = setup_knowledge_base
    doc_id = "duplicate_id"
    original_content = "Contenu original."
    new_content = "Nouveau contenu pour le même ID."
    
    kb.add_document(doc_id, original_content)
    kb.add_document(doc_id, new_content) # This should update the document via upsert

    retrieved_doc = kb.get_document_by_id(doc_id)
    assert retrieved_doc is not None
    assert retrieved_doc["document"] == new_content
    assert "_default" in retrieved_doc["metadata"] and retrieved_doc["metadata"]["_default"] is True