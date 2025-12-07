"""
Full End-to-End Test for Deep Agent Manufacturing System

This script tests the complete pipeline:
1. Orchestrator receives query
2. Spawns subagents as needed
3. Subagents use MCP tools
4. Results are formatted and returned

Make sure you have added your OPENAI_API_KEY to .env before running!
"""

import sys
import os
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent))

from src.utils import setup_logging, setup_langsmith

# Initialize logging and tracing
setup_logging()
setup_langsmith()

print("=" * 70)
print("🏭 LangChain Deep Agent - Full System Test")
print("=" * 70)

# Check for API key
from src.config import settings

if not settings.openai_api_key or settings.openai_api_key.startswith("sk-test"):
    print("\n❌ ERROR: No valid OPENAI_API_KEY found in .env file")
    print("\nPlease:")
    print("1. Open .env file")
    print("2. Add your OpenAI API key: OPENAI_API_KEY=sk-your-key-here")
    print("3. Run this test again")
    sys.exit(1)

print(f"\n✓ Configuration loaded")
print(f"  • Model: {settings.openai_model}")
print(f"  • LangSmith: {'✓ Enabled' if settings.is_langsmith_enabled else '✗ Disabled'}")

# Test queries - simple to complex
test_queries = [
    {
        "name": "Simple Equipment List",
        "query": "What equipment is available in our manufacturing system?"
    },
    {
        "name": "Equipment Status",
        "query": "What is the current status of CNC-Machine-1?"
    },
    {
        "name": "Production Analysis",
        "query": "Get the production metrics for the last 7 days"
    },
]

print("\n" + "=" * 70)
print("Test Scenarios")
print("=" * 70)
print(f"\nWe have {len(test_queries)} test queries to run.")
print("Each tests different parts of the system:\n")
for i, test in enumerate(test_queries, 1):
    print(f"{i}. {test['name']}")

selection = input(f"\nWhich test would you like to run? (1-{len(test_queries)}, or 'all'): ").strip()

if selection.lower() == 'all':
    selected_tests = test_queries
else:
    try:
        idx = int(selection) - 1
        if 0 <= idx < len(test_queries):
            selected_tests = [test_queries[idx]]
        else:
            print(f"Invalid selection. Running first test.")
            selected_tests = [test_queries[0]]
    except:
        print(f"Invalid input. Running first test.")
        selected_tests = [test_queries[0]]

print("\n" + "=" * 70)
print("Running Tests")
print("=" * 70)

from src.agents import run_query

for i, test in enumerate(selected_tests, 1):
    print(f"\n{'='*70}")
    print(f"Test {i}: {test['name']}")
    print(f"{'='*70}")
    print(f"\n📝 Query: {test['query']}")
    print(f"\n🤖 Agent Processing...\n")
    
    try:
        result = run_query(test['query'])
        
        if result["success"]:
            print("✓ SUCCESS")
            print(f"\n{'-'*70}")
            print("Response:")
            print(f"{'-'*70}")
            print(result["response"])
            print(f"{'-'*70}\n")
            
            # Show message count
            msg_count = len(result.get("messages", []))
            print(f"ℹ️  Total messages exchanged: {msg_count}")
            
        else:
            print(f"\n❌ FAILED")
            print(f"Error: {result.get('error', 'Unknown error')}")
            
    except Exception as e:
        print(f"\n❌ EXCEPTION: {str(e)}")
        import traceback
        traceback.print_exc()

print("\n" + "=" * 70)
print("Test Complete!")
print("=" * 70)

if settings.is_langsmith_enabled:
    print(f"\n📊 View detailed traces in LangSmith:")
    print(f"   https://smith.langchain.com")

print("\nFor interactive mode, run:")
print("   python3 -m src.main --mode interactive")
print("\n" + "=" * 70)
