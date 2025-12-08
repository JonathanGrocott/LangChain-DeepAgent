"""
Production Monitoring Scenario
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

def run_production_monitoring():
    print("=" * 60)
    print("🏭 SCENARIO: Production Monitoring")
    print("=" * 60)
    print("Goal: Analyze real-time production performance using HighByte data.\n")
    
    # Initialize the agent
    agent = create_orchestrator_agent()
    
    # Define the scenario query
    query = (
        "Check the status of Conveyor-A. "
        "Its target speed is 1.0 m/s. "
        "Compare its current speed against the target "
        "and check for any active equipment alerts. "
        "Summarize the performance."
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
    print("📊 Final Report")
    print("=" * 60)
    print(result["messages"][-1].content)
    print("\n✓ Scenario Complete")

if __name__ == "__main__":
    run_production_monitoring()
