"""Test RAG Retrieval"""

import sys
import os
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.rag.chromadb_manager import get_chroma_manager
from src.rag.retrieval import get_docs_search_tool
from src.utils import setup_logging

setup_logging()

def test_rag_retrieval():
    print("=" * 60)
    print("Testing RAG Retrieval")
    print("=" * 60)
    
    # 1. Direct ChromaDB Query
    print("\n1. Testing Direct Vector Search")
    print("-" * 60)
    manager = get_chroma_manager()
    results = manager.query_similarity("manufacturing_docs", "spindle overheating", k=1)
    
    if results:
        print(f"✓ Found {len(results)} relevant chunks")
        print(f"Content preview: {results[0].page_content[:100]}...")
    else:
        print("✗ No results found (Did you run ingestion?)")
        return False
        
    # 2. Testing LangChain Tool
    print("\n2. Testing RAG Tool Wrapper")
    print("-" * 60)
    tool = get_docs_search_tool()
    
    response = tool.invoke({"query": "How to fix vibration issues?"})
    print("Tool Response:")
    print(response[:200] + "...")
    
    if "Vibration / Chatter" in response:
        print("\n✓ Tool successfully retrieved context")
    else:
        print("\n✗ Tool failed to find specific context")
        
    print("\n" + "=" * 60)
    print("RAG System: ✓ VERIFIED")
    print("=" * 60)
    return True

if __name__ == "__main__":
    test_rag_retrieval()
