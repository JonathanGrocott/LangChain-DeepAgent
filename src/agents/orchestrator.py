"""Main Orchestrator Deep Agent for Manufacturing

This is the primary entry point for the Deep Agent system.
"""

from typing import Any, Dict, List, Optional
from langchain.chat_models import init_chat_model
from deepagents import create_deep_agent

from src.config import settings
from src.config.subagent_configs import SUBAGENT_REGISTRY
from src.agents.prompts import (
    ORCHESTRATOR_PROMPT,
    DATA_RETRIEVAL_PROMPT,
    ANALYSIS_PROMPT,
    REPORTING_PROMPT,
)
from src.mcp import get_mcp_client
from src.rag.retrieval import get_docs_search_tool, get_maintenance_search_tool
from src.utils import get_logger

logger = get_logger(__name__)


def create_orchestrator_agent():
    """
    Create the main orchestrator deep agent.
    
    The orchestrator coordinates the entire manufacturing analysis workflow
    by spawning specialized subagents as needed.
    
    Returns:
        Deep agent instance configured as orchestrator
    """
    logger.info("creating_orchestrator_agent")
    
    # Initialize LLM with explicit API key from settings
    model = init_chat_model(
        model=settings.openai_model,
        model_provider="openai",
        api_key=settings.openai_api_key,
        temperature=settings.openai_temperature,
    )
    
    # Get MCP tools (all tools available to orchestrator can delegate to subagents)
    mcp_client = get_mcp_client()
    mcp_tools = mcp_client.get_all_tools()
    
    logger.info(
        "mcp_tools_loaded",
        count=len(mcp_tools),
        tools=[tool.name for tool in mcp_tools]
    )
    
    # Configure subagents
    # The orchestrator can spawn these subagents using the built-in 'task' tool
    # Deep Agents expects each subagent to be a dict with: name, description, system_prompt, tools
    subagents_config = [
        {
            "name": "data-retrieval",
            "description": "Fetches data from manufacturing systems (HighByte, Teradata, SQL Server)",
            "system_prompt": DATA_RETRIEVAL_PROMPT,
            "tools": mcp_client.get_tools_for_server("highbyte") + \
                     mcp_client.get_tools_for_server("teradata") + \
                     mcp_client.get_tools_for_server("sqlserver"),
        },
        {
            "name": "analysis",
            "description": "Analyzes manufacturing data for trends, anomalies, and insights",
            "system_prompt": ANALYSIS_PROMPT,
            "tools": [
                get_docs_search_tool(),
                get_maintenance_search_tool()
            ],
        },
        {
            "name": "reporting",
            "description": "Creates formatted reports from analysis results",
            "system_prompt": REPORTING_PROMPT,
            "tools": [],  # Reporting only uses built-in file tools
        },
    ]
    
    # Create the orchestrator agent
    # Deep Agents provides built-in tools:
    # - write_todos: Task planning
    # - task: Spawn subagents
    # - File tools: read_file, write_file, edit_file, ls, glob, grep
    agent = create_deep_agent(
        model=model,
        system_prompt=ORCHESTRATOR_PROMPT,
        tools=mcp_tools,  # Orchestrator has access to all MCP tools
        subagents=subagents_config,
    )
    
    logger.info(
        "orchestrator_agent_created",
        model=settings.openai_model,
        mcp_tools=len(mcp_tools),
        subagents=[sa["name"] for sa in subagents_config]
    )
    
    return agent


# Global orchestrator instance
_orchestrator: Any = None


def get_orchestrator() -> Any:
    """
    Get or create the global orchestrator agent instance.
    
    Returns:
        Orchestrator deep agent
    """
    global _orchestrator
    if _orchestrator is None:
        _orchestrator = create_orchestrator_agent()
    return _orchestrator


def run_query(query: str, thread_id: Optional[str] = None) -> Dict[str, Any]:
    """
    Run a query through the orchestrator agent.
    
    Args:
        query: User query about manufacturing systems
        thread_id: Optional conversation thread ID for persistence
        
    Returns:
        Agent response with final message and metadata
    """
    logger.info("running_query", query=query[:100], thread_id=thread_id)
    
    orchestrator = get_orchestrator()
    
    # Format input for deep agent
    input_data = {
        "messages": [
            {
                "role": "user",
                "content": query
            }
        ]
    }
    
    # Add thread_id if provided (for conversation persistence)
    config = {}
    if thread_id:
        config["configurable"] = {"thread_id": thread_id}
    
    try:
        # Invoke the agent
        result = orchestrator.invoke(input_data, config=config if config else None)
        
        # Extract the final message
        final_message = result["messages"][-1].content
        
        logger.info(
            "query_completed",
            response_length=len(final_message),
            message_count=len(result["messages"])
        )
        
        return {
            "success": True,
            "response": final_message,
            "messages": result["messages"],
            "thread_id": thread_id,
        }
        
    except Exception as e:
        logger.error(
            "query_failed",
            error=str(e),
            query=query[:100]
        )
        return {
            "success": False,
            "error": str(e),
            "query": query,
        }
