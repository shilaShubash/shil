"""
RAG Retriever for scenario similarity search using ChromaDB.

Handles embedding and retrieval of relevant scenarios based on conversation context.
"""

from typing import List, Dict, Any, Optional
from langchain_chroma import Chroma
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from backend.config import get_config


class ScenarioRetriever:
    """
    Retrieves relevant scenarios from ChromaDB based on conversation summary.
    """

    def __init__(self):
        """Initialize the retriever with embedding model and vector store."""
        config = get_config()

        # Initialize embedding model (Gemini Embedding 001)
        self.embeddings = GoogleGenerativeAIEmbeddings(
            model=config.embedding_model,
            google_api_key=config.google_api_key
        )

        # Initialize ChromaDB vector store
        self.vector_store = Chroma(
            collection_name=config.chroma_collection_name,
            embedding_function=self.embeddings,
            persist_directory=config.chroma_db_path
        )

        self.top_k = config.top_k_scenarios

    def retrieve_scenarios(self, query_text: str) -> List[Dict[str, Any]]:
        """
        Retrieve top-K relevant scenarios based on query text.

        Args:
            query_text: Natural language summary of the case context

        Returns:
            List of scenario dictionaries with keys:
                - id: Scenario identifier
                - title: Scenario title
                - content: Full scenario text
                - similarity_score: Cosine similarity score
        """
        # Perform similarity search
        results = self.vector_store.similarity_search_with_score(
            query_text,
            k=self.top_k
        )

        # Format results
        scenarios = []
        for doc, score in results:
            scenarios.append({
                "id": doc.metadata.get("id", "unknown"),
                "title": doc.metadata.get("title", "Untitled Scenario"),
                "content": doc.page_content,
                "similarity_score": float(score)
            })

        return scenarios

    def check_collection_exists(self) -> bool:
        """
        Check if the scenario collection exists in ChromaDB.

        Returns:
            True if collection exists and has documents, False otherwise
        """
        try:
            # Try to get collection
            collection = self.vector_store._collection
            count = collection.count()
            return count > 0
        except Exception:
            return False

    def get_collection_count(self) -> int:
        """
        Get the number of scenarios in the collection.

        Returns:
            Number of documents in collection, or 0 if error
        """
        try:
            collection = self.vector_store._collection
            return collection.count()
        except Exception:
            return 0
