"""LangChain Deep Agent for Manufacturing - Configuration Settings"""

from typing import Literal, Optional
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables"""
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore"
    )
    
    # OpenAI Configuration
    openai_api_key: str = Field(..., description="OpenAI API key")
    openai_model: str = Field(default="gpt-4o", description="OpenAI model to use")
    openai_temperature: float = Field(default=0.7, ge=0.0, le=2.0)
    
    # LangSmith Configuration (Optional)
    langsmith_api_key: Optional[str] = Field(default=None, description="LangSmith API key for tracing")
    langsmith_project: str = Field(default="langchain-deepagent-manufacturing")
    langsmith_tracing: bool = Field(default=False, description="Enable LangSmith tracing")
    
    # ChromaDB Configuration
    chromadb_host: str = Field(default="localhost")
    chromadb_port: int = Field(default=8000)
    chromadb_persist_directory: str = Field(default="./chroma_data")
    
    # Deep Agents Configuration
    deepagent_filesystem_root: str = Field(default="./.deep_agents")
    deepagent_log_level: Literal["DEBUG", "INFO", "WARNING", "ERROR"] = Field(default="INFO")
    
    # MCP Server Configuration
    mcp_highbyte_enabled: bool = Field(default=True)
    mcp_teradata_enabled: bool = Field(default=True)
    mcp_sqlserver_enabled: bool = Field(default=True)
    
    # Application Settings
    app_env: Literal["development", "staging", "production"] = Field(default="development")
    log_level: Literal["DEBUG", "INFO", "WARNING", "ERROR"] = Field(default="INFO")
    
    @property
    def is_production(self) -> bool:
        """Check if running in production environment"""
        return self.app_env == "production"
    
    @property
    def is_langsmith_enabled(self) -> bool:
        """Check if LangSmith tracing is enabled and configured"""
        return self.langsmith_tracing and self.langsmith_api_key is not None


# Global settings instance
settings = Settings()
