# LangChain Deep Agent for Manufacturing

A flexible, production-ready deep agent framework built with LangChain's **Deep Agents** library for manufacturing use cases. The framework supports specialized subagents that can be dynamically spawned to handle complex manufacturing workflows with MCP (Model Context Protocol) server integration.

## Features

- 🤖 **Deep Agents Framework**: Built on LangChain's `deepagents` with hierarchical agent architecture
- 🏭 **Manufacturing-Focused**: Designed for production monitoring, predictive maintenance, and quality control
- 🔌 **MCP Integration**: Mock MCP servers for HighByte (OPC-UA), Teradata, and SQL Server
- 🧠 **RAG Capabilities**: ChromaDB integration for manufacturing documentation and historical logs
- 📊 **Observability**: Full LangSmith integration for tracing and debugging
- 🐳 **Production-Ready**: Docker containerization included

## Architecture

The system uses a **pipeline-based architecture** with specialized subagents:

1. **Orchestrator Agent**: Main agent that receives requests and coordinates subagents
2. **Data Retrieval Agent**: Fetches data from MCP servers
3. **Analysis Agent**: Analyzes data for trends and anomalies
4. **Reporting Agent**: Formats results into actionable reports

## Prerequisites

- Python 3.10+
- Poetry (for dependency management)
- Docker & Docker Compose (optional, for containerized deployment)
- OpenAI API key
- LangSmith API key (optional, for observability)

## Quick Start

### 1. Clone and Setup

```bash
git clone <repository-url>
cd LangChain-DeepAgent

# Copy environment template
cp .env.example .env

# Edit .env and add your API keys
nano .env  # or use your preferred editor
```

### 2. Install Dependencies

```bash
# Install Poetry if you haven't already
curl -sSL https://install.python-poetry.org | python3 -

# Install project dependencies
poetry install

# Activate virtual environment
poetry shell
```

### 3. Run Examples

```bash
# Production monitoring example
python examples/production_monitoring.py

# Interactive CLI mode
python -m src.main --mode interactive
```

### 4. Docker Deployment (Optional)

```bash
# Start all services (ChromaDB + Deep Agent)
docker-compose up --build

# In another terminal, run examples
docker exec -it langchain-deepagent python examples/production_monitoring.py
```

## Project Structure

```
LangChain-DeepAgent/
├── src/
│   ├── config/          # Configuration and settings
│   ├── agents/          # Orchestrator and subagent definitions
│   ├── mcp/             # MCP server infrastructure
│   ├── rag/             # ChromaDB and RAG tools
│   └── utils/           # Logging and LangSmith setup
├── examples/            # Example scenarios
├── tests/               # Test suite
├── docs/                # Additional documentation
├── pyproject.toml       # Poetry dependencies
├── Dockerfile           # Container definition
└── docker-compose.yml   # Multi-container setup
```

## Configuration

All configuration is managed through environment variables in `.env`:

- **OpenAI**: `OPENAI_API_KEY`, `OPENAI_MODEL`
- **LangSmith**: `LANGSMITH_API_KEY`, `LANGSMITH_TRACING`
- **ChromaDB**: `CHROMADB_HOST`, `CHROMADB_PORT`
- **MCP Servers**: Enable/disable individual mock servers

See `.env.example` for all available options.

## Development

### Running Tests

```bash
poetry run pytest
```

### Code Formatting

```bash
# Format code
poetry run black src/ tests/

# Lint code
poetry run ruff check src/ tests/
```

## Examples

### Production Monitoring

Monitor production line status with data from multiple sources:

```python
# See examples/production_monitoring.py
# Demonstrates orchestrator spawning data-retrieval → analysis → reporting pipeline
```

### Predictive Maintenance

Analyze equipment health and recommend maintenance actions:

```python
# See examples/predictive_maintenance.py
# Uses RAG for historical context and MCP for current metrics
```

## Documentation

- [Architecture Overview](docs/architecture.md)
- [Deployment Guide](docs/deployment.md)
- [Extending the Framework](docs/extending.md)

## License

MIT License - see LICENSE file for details

## Contributing

Contributions welcome! Please read CONTRIBUTING.md for guidelines.

## Support

For issues and questions, please open a GitHub issue.
