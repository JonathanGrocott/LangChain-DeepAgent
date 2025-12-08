"""
Predictive Maintenance Scenario
"""
import sys
import os
from pathlib import Path
from src.utils import setup_logging
from src.agents import create_orchestrator_agent
from langchain_core.messages import HumanMessage

# Ensure project root is in path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

setup_logging()

def run_predictive_maintenance():
    print("=" * 60)
    print("🔧 SCENARIO: Predictive Maintenance Analysis")
    print("=" * 60)
    print("Goal: Analyze equipment health trends and recommend maintenance.\n")
    
    # Initialize the agent
    agent = create_orchestrator_agent()
    
    # Define the scenario query
    query = (
        "Analyze CNC-Machine-1. "
        "Check its recent vibration data. "
        "IMPORTANT: Use 'search_manufacturing_docs' to search for 'troubleshooting vibration'. "
        "The docs CONTAIN instructions for this. Quote the troubleshooting steps found in the docs in your answer. "
        "Then recommend if we should schedule maintenance."
    )
    
    print(f"📝 User Query: {query}\n")
    print("🤖 Agent working...\n")
    
    # Execute
    try:
        result = agent.invoke(
            {"messages": [HumanMessage(content=query)]},
            config={"recursion_limit": 50}
        )
    except Exception as e:
        print(f"\n❌ Error during execution: {e}")
        print("Note: Ensure you have internet connection for LangSmith or valid API keys.")
        return
    
    print("\n" + "=" * 60)
    print("📋 Recommendation")
    print("=" * 60)
    print(result["messages"][-1].content)
    print("\n✓ Scenario Complete")

if __name__ == "__main__":
    run_predictive_maintenance()
