# Deployment Guide

This guide covers how to deploy the LangChain Deep Agent framework in a production environment using Docker.

## Prerequisites

- Docker Engine 20.10+
- Docker Compose v2.0+
- OpenAI API Key

## Configuration

1. **Environment Variables**
   Ensure your `.env` file is configured with production values:

   ```bash
   # LLM Configuration
   OPENAI_API_KEY=sk-prod-key...
   OPENAI_MODEL=gpt-4o

   # Observability (Recommended)
   LANGSMITH_TRACING=true
   LANGSMITH_API_KEY=lsv2-prod-key...
   LANGSMITH_PROJECT=manufacturing-agent-prod

   # RAG Storage
   CHROMA_PERSIST_DIRECTORY=/app/data/chroma
   CHROMA_HOST=chromadb
   CHROMA_PORT=8000
   ```

2. **Docker Compose Overrides** (Optional)
   Create `docker-compose.prod.yml` for production-specific settings (e.g., restart policies, logging drivers).

## Building the Image

Build the production image:

```bash
docker-compose build
```

## Running in Production

Start the services in detached mode:

```bash
docker-compose up -d
```

### Health Checks

Verify services are running:

```bash
docker-compose ps
```

You can inspect the agent logs:

```bash
docker-compose logs -f app
```

## Data Persistence

- **ChromaDB Data**: Persisted in the `chroma_data` volume (see `docker-compose.yml`).
- **Logs**: Application logs are output to stdout/stderr for collection by your logging driver (e.g., AWS CloudWatch, Datadog).

## Scaling

For high availability, you can run multiple replicas of the agent service behind a load balancer, but note that:
1. **RAG Ingestion** should be done by a single worker or coordinated job.
2. **Conversation History** currently relies on in-memory state for individual turns; for multi-turn persistence across replicas, a Redis-backed checkpoint saver would be needed (future enhancement).

## Updating

To update the application:

1. Pull new code: `git pull origin main`
2. Rebuild: `docker-compose build`
3. Restart: `docker-compose up -d`
