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
        choices=["interactive", "single"],
        default="interactive",
        help="Run mode: interactive chat or single query"
    )
    parser.add_argument(
        "--query",
        type=str,
        help="Query to run in single mode"
    )
    
    args = parser.parse_args()
    
    logger.info(
        "starting_deepagent",
        mode=args.mode,
        environment=settings.app_env,
        langsmith_enabled=settings.is_langsmith_enabled
    )
    
    if args.mode == "single":
        if not args.query:
            logger.error("single_mode_requires_query")
            print("Error: --query required in single mode")
            sys.exit(1)
        
        # TODO: Implement single query mode
        logger.info("single_query_mode", query=args.query)
        print(f"Single query mode - Query: {args.query}")
        print("Implementation coming in Phase 3...")
    else:
        # TODO: Implement interactive mode
        logger.info("interactive_mode_starting")
        print("=" * 60)
        print("LangChain Deep Agent for Manufacturing - Interactive Mode")
        print("=" * 60)
        print("\nImplementation coming in Phase 3...")
        print("\nConfiguration:")
        print(f"  • Model: {settings.openai_model}")
        print(f"  • Environment: {settings.app_env}")
        print(f"  • LangSmith: {'✓ Enabled' if settings.is_langsmith_enabled else '✗ Disabled'}")
        print(f"  • ChromaDB: {settings.chromadb_host}:{settings.chromadb_port}")
        print("\nType 'exit' to quit")
        print("=" * 60)


if __name__ == "__main__":
    main()
