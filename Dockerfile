# Multi-stage build for production deployment
FROM python:3.10-slim as builder

# Install Poetry
RUN pip install poetry==1.8.0

# Set working directory
WORKDIR /app

# Copy dependency files
COPY pyproject.toml ./

# Configure poetry to not create virtual env (using container isolation)
RUN poetry config virtualenvs.create false

# Install dependencies
RUN poetry install --no-dev --no-interaction --no-ansi

# Production stage
FROM python:3.10-slim

WORKDIR /app

# Copy installed dependencies from builder
COPY --from=builder /usr/local/lib/python3.10/site-packages /usr/local/lib/python3.10/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

# Copy application code
COPY src/ ./src/
COPY examples/ ./examples/

# Create directories for Deep Agents filesystem and ChromaDB
RUN mkdir -p .deep_agents chroma_data

# Expose port for potential web interface
EXPOSE 8000

# Set environment
ENV PYTHONUNBUFFERED=1
ENV DEEPAGENT_FILESYSTEM_ROOT=/app/.deep_agents

# Default command (can be overridden)
CMD ["python", "-m", "src.main", "--mode", "interactive"]
