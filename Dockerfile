# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory in the container
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    tesseract-ocr \
    libtesseract-dev \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY pyproject.toml .
COPY README.md .
COPY ner_a_mcp/ ./ner_a_mcp/

# Install the package in editable mode or just its dependencies
RUN pip install --no-cache-dir .

# Expose any ports if the server runs in HTTP mode (FastMCP supports this)
# Default MCP uses stdio, which doesn't need a port, but FastAPI/SSE does.
EXPOSE 8000

# Command to run the MCP server
# For stdio mode:
CMD ["python", "ner_a_mcp/server.py"]

# For SSE (HTTP) mode, you would change the entry point in server.py to use sse
