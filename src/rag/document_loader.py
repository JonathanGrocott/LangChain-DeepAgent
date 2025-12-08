"""
Document loading and chunking utilities for RAG ingestion.
"""
import os
from typing import List, Dict, Any, Union
from pathlib import Path
from langchain_community.document_loaders import (
    TextLoader,
    UnstructuredMarkdownLoader,
    DirectoryLoader
)
from langchain_text_splitters import MarkdownHeaderTextSplitter, RecursiveCharacterTextSplitter
from langchain_core.documents import Document
from src.utils import get_logger

logger = get_logger(__name__)

class DocumentProcessor:
    """Handles loading and chunking of documents."""
    
    def __init__(self, chunk_size: int = 1000, chunk_overlap: int = 200):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        
    def load_directory(self, directory_path: str, glob_pattern: str = "**/*.md") -> List[Document]:
        """Load documents from a directory."""
        path = Path(directory_path)
        if not path.exists():
            logger.error("directory_not_found", path=directory_path)
            return []
            
        logger.info("loading_directory", path=directory_path, pattern=glob_pattern)
        
        # Determine loader based on file extension
        if glob_pattern.endswith(".md"):
            loader_cls = UnstructuredMarkdownLoader
        else:
            loader_cls = TextLoader
            
        loader = DirectoryLoader(
            str(path),
            glob=glob_pattern,
            loader_cls=loader_cls,
            show_progress=True
        )
        
        docs = loader.load()
        logger.info("documents_loaded", count=len(docs))
        return docs
        
    def split_documents(self, documents: List[Document]) -> List[Document]:
        """Split documents into semantic chunks."""
        if not documents:
            return []
            
        logger.info("splitting_documents", count=len(documents))
        
        # First pass: Logic based on markdown headers if applicable
        # This is a simple implementation; deep agents often benefit from
        # recursive splitting for broader context.
        
        splitter = RecursiveCharacterTextSplitter(
            chunk_size=self.chunk_size,
            chunk_overlap=self.chunk_overlap,
            separators=["\n## ", "\n### ", "\n#### ", "\n", " ", ""]
        )
        
        chunks = splitter.split_documents(documents)
        
        logger.info("chunks_created", count=len(chunks))
        return chunks

    def process_and_split(self, directory_path: str) -> List[Document]:
        """Load and split documents in one go."""
        docs = self.load_directory(directory_path)
        return self.split_documents(docs)
