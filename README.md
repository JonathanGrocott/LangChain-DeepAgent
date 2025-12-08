# LangChain Deep Agent Framework for Manufacturing

A production-ready [Deep Agents](https://python.langchain.com/) framework designed for manufacturing environments. This system demonstrates a hierarchical agent architecture that integrates real-time data monitoring (HighByte), predictive maintenance (RAG + Analytics), and automated reporting.

## 🚀 Key Features

-   **Deep Agent Orchestration**: Hierarchical planning with specialized subagents (Retrieval, Analysis, Reporting).
-   **MCP Integration**: First-class support for **Model Context Protocol** servers (simulated HighByte, Teradata, SQL Server).
-   **RAG Knowledge Base**: Integrated ChromaDB for semantic search over manufacturing documentation (SOPs, Maintenance Guides).
-   **Production Ready**: Dockerized deployment, LangSmith observability, and robust configuration management.
-   **Extensible**: Modular design for adding new MCP servers or specialized subagents.

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

## 🏭 Example Scenarios

The project includes pre-built scenarios in `examples/scenarios/` demonstrating key capabilities:

1.  **Production Monitoring** (`production`):
    - Fetches real-time machine data (HighByte)
    - Analyzes performance vs targets
    - Summarizes line efficiency

2.  **Predictive Maintenance** (`maintenance`):
    - Analyzes equipment health tags
    - Searches RAG knowledge base for troubleshooting guides
    - Recommends maintenance actions

### Running Examples

```bash
# Run specific scenario
python3 examples/run_examples.py production
python3 examples/run_examples.py maintenance

# Run all
python3 examples/run_examples.py all
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
LangChain-DeepAgent/.
├── src/                  # Source code
│   ├── agents/           # LangChain Deep Agent definitions
│   ├── config/           # Configuration settings
│   ├── mcp/              # MCP server integrations
│   ├── rag/              # RAG knowledge base
│   ├── utils/            # Logging and helpers
│   └── main.py           # Entry point
├── tests/                # Test suite
│   ├── integration/      # Pytest integration tests
│   └── ...               # Unit tests
├── examples/             # Ready-to-run scenarios
│   ├── scenarios/
│   └── run_examples.py
├── docs/                 # Documentation
│   └── deployment.md
├── .env                  # Environment variables (git-ignored)
├── docker-compose.yml    # Docker services
├── Dockerfile            # Production build
├── pyproject.toml        # Poetry dependencies
└── README.md             # Project documentation
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
