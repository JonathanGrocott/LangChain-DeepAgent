"""LangSmith setup and configuration for Deep Agents tracing"""

import os
from typing import Optional
from src.config import settings


def setup_langsmith() -> None:
    """
    Configure LangSmith tracing for Deep Agents.
    
    Sets environment variables that LangChain uses for automatic tracing.
    Call this early in application startup.
    """
    if settings.is_langsmith_enabled:
        os.environ["LANGSMITH_API_KEY"] = settings.langsmith_api_key
        os.environ["LANGSMITH_PROJECT"] = settings.langsmith_project
        os.environ["LANGSMITH_TRACING_V2"] = "true"
        
        print(f"✓ LangSmith tracing enabled for project: {settings.langsmith_project}")
    else:
        # Explicitly disable if not configured
        os.environ["LANGSMITH_TRACING_V2"] = "false"
        
        if settings.langsmith_api_key:
            print("ℹ LangSmith API key found but tracing disabled in settings")
        else:
            print("ℹ LangSmith tracing disabled (no API key configured)")


def get_langsmith_url(run_id: Optional[str] = None) -> Optional[str]:
    """
    Get LangSmith dashboard URL for a specific run.
    
    Args:
        run_id: Optional run ID to link directly to a trace
        
    Returns:
        URL to LangSmith dashboard or None if not configured
    """
    if not settings.is_langsmith_enabled:
        return None
    
    base_url = "https://smith.langchain.com"
    project = settings.langsmith_project
    
    if run_id:
        return f"{base_url}/o/default/projects/p/{project}/r/{run_id}"
    else:
        return f"{base_url}/o/default/projects/p/{project}"
