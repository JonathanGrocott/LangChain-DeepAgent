"""CLI entry point for Deep Agent application"""

import sys
import argparse
from src.config import settings
from src.utils import setup_logging, setup_langsmith, get_logger

# Initialize logging and tracing
setup_logging()
setup_langsmith()

logger = get_logger(__name__)


def main():
    """Main entry point for the Deep Agent CLI"""
    parser = argparse.ArgumentParser(
        description="LangChain Deep Agent for Manufacturing"
    )
    parser.add_argument(
        "--mode", 
        type=str, 
        choices=["interactive", "single", "ingest"], 
        default="interactive",
        help="Run mode: interactive chat, single query, or document ingestion"
    )
    parser.add_argument("--query", type=str, help="Query for single mode")
    parser.add_argument("--docs", type=str, help="Path to documents for ingestion mode")
    
    args = parser.parse_args()
    
    logger.info(
        "starting_deepagent",
        mode=args.mode,
        environment=settings.app_env,
        langsmith_enabled=settings.is_langsmith_enabled
    )
    
    if args.mode == "ingest":
        if not args.docs:
            logger.error("ingest_mode_requires_docs")
            print("Error: --docs <path> required in ingest mode")
            sys.exit(1)
            
        from src.rag.chromadb_manager import get_chroma_manager
        from src.rag.document_loader import DocumentProcessor
        
        print("\n" + "=" * 60)
        print(f"Ingesting documents from: {args.docs}")
        print("=" * 60)
        
        try:
            processor = DocumentProcessor()
            docs = processor.process_and_split(args.docs)
            
            if not docs:
                print("No documents found or processed.")
                sys.exit(1)
                
            print(f"\nProcessing {len(docs)} chunks...")
            
            manager = get_chroma_manager()
            manager.add_documents("manufacturing_docs", docs)
            
            print("\n✓ Ingestion complete!")
            print("=" * 60)
            sys.exit(0)
            
        except Exception as e:
            print(f"\n❌ Error during ingestion: {e}")
            sys.exit(1)

    if args.mode == "single":
        if not args.query:
            logger.error("single_mode_requires_query")
            print("Error: --query required in single mode")
            sys.exit(1)
        
        # Single query mode
        logger.info("single_query_mode", query=args.query)
        print("\n" + "=" * 60)
        print("LangChain Deep Agent - Single Query")
        print("=" * 60)
        print(f"\nQuery: {args.query}\n")
        
        from src.agents import run_query
        
        result = run_query(args.query)
        
        if result["success"]:
            print("\nResponse:")
            print("-" * 60)
            print(result["response"])
            print("\n" + "=" * 60)
        else:
            print(f"\n✗ Error: {result['error']}")
            sys.exit(1)
    else:
        # Interactive mode
        logger.info("interactive_mode_starting")
        print("=" * 60)
        print("LangChain Deep Agent for Manufacturing - Interactive Mode")
        print("=" * 60)
        print("\nConfiguration:")
        print(f"  • Model: {settings.openai_model}")
        print(f"  • Environment: {settings.app_env}")
        print(f"  • LangSmith: {'✓ Enabled' if settings.is_langsmith_enabled else '✗ Disabled'}")
        print(f"  • ChromaDB: {settings.chromadb_host}:{settings.chromadb_port}")
        print("\nThe agent can:")
        print("  - Fetch real-time equipment data")
        print("  - Analyze production metrics")
        print("  - Generate maintenance reports")
        print("  - Query work orders and inventory")
        print("\nType 'exit' or 'quit' to end the session")
        print("=" * 60 + "\n")
        
        from src.agents import run_query
        
        while True:
            try:
                query = input("\n🏭 You: ").strip()
                
                if not query:
                    continue
                
                if query.lower() in ["exit", "quit", "q"]:
                    print("\nGoodbye!")
                    break
                
                print("\n🤖 Agent: ", end="", flush=True)
                
                result = run_query(query)
                
                if result["success"]:
                    print(result["response"])
                else:
                    print(f"\n✗ Error: {result['error']}")
                    
            except KeyboardInterrupt:
                print("\n\nGoodbye!")
                break
            except Exception as e:
                logger.error("interactive_error", error=str(e))
                print(f"\n✗ Unexpected error: {e}")


if __name__ == "__main__":
    main()
