"""
Integration tests for the LangChain Deep Agent pipeline.
"""
import pytest
import os
from src.agents import create_orchestrator_agent
from src.config import settings
from langchain_core.messages import HumanMessage
from dotenv import load_dotenv

load_dotenv()

# Check if we have a valid API key for integration testing
HAS_API_KEY = bool(os.getenv("OPENAI_API_KEY")) and not os.getenv("OPENAI_API_KEY").startswith("sk-test")

@pytest.fixture
def agent():
    """Fixture to provide an orchestrator agent instance."""
    return create_orchestrator_agent()

def test_agent_initialization(agent):
    """Test that the agent can be initialized correctly."""
    assert agent is not None
    # Verify it's a compiled graph (LangGraph)
    assert hasattr(agent, "invoke")

@pytest.mark.skipif(not HAS_API_KEY, reason="Requires valid OPENAI_API_KEY")
def test_simple_query_execution(agent):
    """Test a simple query to verify LLM connectivity and basic tool usage."""
    query = "Hello, who are you and what can you do?"
    result = agent.invoke(
        {"messages": [HumanMessage(content=query)]},
        config={"recursion_limit": 10}
    )
    
    assert "messages" in result
    last_message = result["messages"][-1]
    assert last_message.content
    assert len(result["messages"]) > 1

@pytest.mark.skipif(not HAS_API_KEY, reason="Requires valid OPENAI_API_KEY")
def test_production_data_retrieval(agent):
    """Test that the agent can route to data retrieval subagent."""
    # This query should trigger the production monitoring flow
    query = "What is the status of Conveyor-A?"
    
    result = agent.invoke(
        {"messages": [HumanMessage(content=query)]},
        config={"recursion_limit": 20}
    )
    
    last_message = result["messages"][-1]
    content = last_message.content.lower()
    
    # Needs to mention either "running", "idle", or some status from the mock
    assert "conveyor-a" in content
    # Should mention status or health
    assert any(term in content for term in ["status", "health", "speed", "rpm"])

@pytest.mark.skipif(not HAS_API_KEY, reason="Requires valid OPENAI_API_KEY")
def test_rag_integration(agent):
    """Test that the agent can use RAG tools."""
    # This matches the sample data we ingested
    query = "How do I troubleshoot spindle overheating?"
    
    result = agent.invoke(
        {"messages": [HumanMessage(content=query)]},
        config={"recursion_limit": 20}
    )
    
    last_message = result["messages"][-1]
    content = last_message.content.lower()
    
    # Should find instructions from the guide
    assert "cooling fan" in content or "coolant" in content or "vents" in content
