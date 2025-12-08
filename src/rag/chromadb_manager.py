"""
ChromaDB Manager including vector store initialization and collection management.
"""
from typing import List, Dict, Any, Optional
import chromadb
from chromadb.config import Settings
from chromadb.utils import embedding_functions
from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain_core.documents import Document
from src.config import settings
from src.utils import get_logger

logger = get_logger(__name__)

class ChromaDBManager:
    """Manages ChromaDB client and collections for RAG."""
    
    def __init__(self):
        self.persist_directory = settings.chromadb_persist_directory
        self.host = settings.chromadb_host
        self.port = settings.chromadb_port
        
        logger.info(
            "initializing_chromadb",
            host=self.host,
            port=self.port,
            persist_dir=self.persist_directory
        )
        
        # Initialize embedding function
        self.embedding_func = OpenAIEmbeddings(
            model="text-embedding-3-small",
            api_key=settings.openai_api_key
        )
        
        # Initialize LangChain Chroma wrapper
        # Use PersistentClient for local development to avoid needing a separate server process
        self.client = chromadb.PersistentClient(
            path=self.persist_directory
        )
        
    def get_collection(self, collection_name: str) -> Chroma:
        """Get a LangChain-compatible Chroma vector store for a collection."""
        return Chroma(
            client=self.client,
            collection_name=collection_name,
            embedding_function=self.embedding_func,
        )
        
    def add_documents(self, collection_name: str, documents: List[Document]) -> None:
        """Add documents to a collection."""
        try:
            logger.info(
                "adding_documents",
                collection=collection_name,
                count=len(documents)
            )
            
            vector_store = self.get_collection(collection_name)
            vector_store.add_documents(documents)
            
            logger.info("documents_added_success")
            
        except Exception as e:
            logger.error("add_documents_failed", error=str(e))
            raise

    def query_similarity(
        self, 
        collection_name: str, 
        query: str, 
        k: int = 4
    ) -> List[Document]:
        """Query for similar documents."""
        try:
            vector_store = self.get_collection(collection_name)
            results = vector_store.similarity_search(query, k=k)
            return results
        except Exception as e:
            logger.error("query_similarity_failed", error=str(e))
            return []
            
    def delete_collection(self, collection_name: str) -> None:
        """Delete a collection locally."""
        try:
            self.client.delete_collection(collection_name)
            logger.info("collection_deleted", collection=collection_name)
        except Exception as e:
            logger.error("delete_collection_failed", error=str(e))

# Global instance
_chroma_manager = None

def get_chroma_manager() -> ChromaDBManager:
    """Get global ChromaDB manager instance."""
    global _chroma_manager
    if _chroma_manager is None:
        _chroma_manager = ChromaDBManager()
    return _chroma_manager
