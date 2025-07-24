import chromadb
from chromadb.utils import embedding_functions
from typing import List, Dict, Any, Optional
import logging

# Configuration du logging
logging.basicConfig(level=logging.INFO, format='[%(asctime)s] %(levelname)s: %(message)s')

class KnowledgeBase:
    """Implémentation de la Base de Connaissance Vectorielle utilisant ChromaDB.
    Peut fonctionner en mode persistant (avec path) ou en mémoire (avec client ou in_memory=True).
    """

    def __init__(self, path: Optional[str] = None, collection_name: str = "aura_knowledge", 
                 client: Optional[chromadb.Client] = None, in_memory: bool = False):
        
        self.collection_name = collection_name
        self.embedding_function = embedding_functions.SentenceTransformerEmbeddingFunction(model_name="all-MiniLM-L6-v2")

        if in_memory:
            self.in_memory_store: Dict[str, Dict[str, Any]] = {}
            self.is_in_memory = True
            logging.info(f"Base de connaissance en mémoire initialisée: {collection_name}")
        else:
            self.is_in_memory = False
            if client:
                self.client = client
            else:
                self.client = chromadb.PersistentClient(path=path if path else "./chroma_db")
            
            self.collection = self.client.get_or_create_collection(
                name=collection_name,
                embedding_function=self.embedding_function
            )
            logging.info(f"Base de connaissance ChromaDB persistante initialisée: {collection_name}")

    def _dot_product(self, vec1: List[float], vec2: List[float]) -> float:
        """Calcule le produit scalaire de deux vecteurs."""
        return sum(v1 * v2 for v1, v2 in zip(vec1, vec2))

    def add_document(self, document_id: str, content: str, metadata: Optional[Dict[str, Any]] = None):
        """Ajoute ou met à jour un document dans la base de connaissance."""
        effective_metadata = metadata if metadata is not None else {}
        if not effective_metadata:
            effective_metadata = {"_default": True}

        if self.is_in_memory:
            embedding = self.embedding_function([content])[0]
            self.in_memory_store[document_id] = {
                "document": content,
                "metadata": effective_metadata,
                "embedding": embedding
            }
            logging.info(f"Document '{document_id}' ajouté/mis à jour en mémoire.")
        else:
            try:
                self.collection.upsert(
                    documents=[content],
                    metadatas=[effective_metadata],
                    ids=[document_id]
                )
                logging.info(f"Document '{document_id}' ajouté/mis à jour dans la base de connaissance persistante.")
            except Exception as e:
                logging.error(f"Erreur lors de l'ajout/mise à jour du document '{document_id}': {e}")

    def query_documents(self, query_text: str, n_results: int = 5) -> List[Dict[str, Any]]:
        """Recherche des documents similaires dans la base de connaissance."""
        if self.is_in_memory:
            query_embedding = self.embedding_function([query_text])[0]
            
            scored_documents = []
            for doc_id, doc_data in self.in_memory_store.items():
                similarity = self._dot_product(query_embedding, doc_data["embedding"])
                scored_documents.append({
                    "document": doc_data["document"],
                    "distance": 1 - similarity, # Convertir la similarité en distance (0=identique, 1=opposé)
                    "metadata": doc_data["metadata"],
                    "_similarity": similarity # Garder la similarité pour le tri
                })
            
            # Trier par similarité décroissante
            scored_documents.sort(key=lambda x: x["_similarity"], reverse=True)
            
            logging.info(f"Requête '{query_text}' effectuée en mémoire. {len(scored_documents)} résultats trouvés.")
            return scored_documents[:n_results]
        else:
            try:
                results = self.collection.query(
                    query_texts=[query_text],
                    n_results=n_results,
                    include=['documents', 'distances', 'metadatas']
                )
                logging.info(f"Requête '{query_text}' effectuée. {len(results['documents'][0])} résultats trouvés.")
                
                formatted_results = []
                if results and results['documents'] and results['documents'][0]:
                    for i in range(len(results['documents'][0])):
                        formatted_results.append({
                            "document": results['documents'][0][i],
                            "distance": results['distances'][0][i],
                            "metadata": results['metadatas'][0][i]
                        })
                return formatted_results
            except Exception as e:
                logging.error(f"Erreur lors de la requête '{query_text}': {e}")
                return []

    def get_document_by_id(self, document_id: str) -> Optional[Dict[str, Any]]:
        """Récupère un document par son ID."""
        if self.is_in_memory:
            doc_data = self.in_memory_store.get(document_id)
            if doc_data:
                logging.info(f"Document '{document_id}' récupéré en mémoire.")
                return {"document": doc_data["document"], "metadata": doc_data["metadata"]}
            logging.info(f"Document '{document_id}' non trouvé en mémoire.")
            return None
        else:
            try:
                results = self.collection.get(
                    ids=[document_id],
                    include=['documents', 'metadatas']
                )
                if results and results['documents'] and results['documents'][0]:
                    logging.info(f"Document '{document_id}' récupéré.")
                    return {
                        "document": results['documents'][0],
                        "metadata": results['metadatas'][0]
                    }
                logging.info(f"Document '{document_id}' non trouvé.")
                return None
            except Exception as e:
                logging.error(f"Erreur lors de la récupération du document '{document_id}': {e}")
                return None

    def delete_collection(self):
        """Supprime la collection de la base de connaissance (utile pour les tests)."""
        if self.is_in_memory:
            self.in_memory_store.clear()
            logging.info(f"Collection en mémoire '{self.collection_name}' vidée.")
        else:
            try:
                self.client.delete_collection(name=self.collection.name)
                logging.info(f"Collection persistante '{self.collection.name}' supprimée.")
            except Exception as e:
                logging.error(f"Erreur lors de la suppression de la collection '{self.collection.name}': {e}")