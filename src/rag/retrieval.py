"""
RAG retrieval tools exposed to agents.
"""
from typing import List, Optional
from langchain_core.tools import tool, StructuredTool
from pydantic import BaseModel, Field
from src.rag.chromadb_manager import get_chroma_manager
from src.utils import get_logger

logger = get_logger(__name__)

class RetrievalInput(BaseModel):
    query: str = Field(description="The search query to find relevant documentation")
    k: int = Field(default=4, description="Number of results to return")

def create_retrieval_tool(collection_name: str, tool_name: str, description: str) -> StructuredTool:
    """Create a LangChain tool for searching a specific RAG collection."""
    
    def search_func(query: str, k: int = 4) -> str:
        """Search the knowledge base."""
        try:
            manager = get_chroma_manager()
            docs = manager.query_similarity(collection_name, query, k)
            
            if not docs:
                return "No relevant documentation found."
                
            # Format results
            result = f"Found {len(docs)} relevant documents:\n\n"
            for i, doc in enumerate(docs, 1):
                source = doc.metadata.get("source", "unknown")
                content = doc.page_content
                result += f"--- Result {i} (Source: {source}) ---\n{content}\n\n"
                
            return result
            
        except Exception as e:
            logger.error("retrieval_error", tool=tool_name, error=str(e))
            return f"Error searching documentation: {str(e)}"

    return StructuredTool(
        name=tool_name,
        description=description,
        func=search_func,
        args_schema=RetrievalInput
    )

# Pre-configured tools

def get_docs_search_tool() -> StructuredTool:
    return create_retrieval_tool(
        collection_name="manufacturing_docs",
        tool_name="search_manufacturing_docs",
        description="Search manufacturing documentation, SOPs, and manual for guidelines and procedures."
    )

def get_maintenance_search_tool() -> StructuredTool:
    return create_retrieval_tool(
        collection_name="maintenance_logs",
        tool_name="search_maintenance_history",
        description="Search historical maintenance logs for past issues and resolutions."
    )
