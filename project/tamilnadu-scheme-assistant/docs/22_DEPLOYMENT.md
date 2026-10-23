# Deployment Guide

This document outlines the deployment strategy for the Tamil Nadu Multilingual Voice-Based Government Scheme Assistant. The primary focus is local deployment using Docker Compose to ensure all components run offline and reliably on student hardware.

## Target Hardware Requirements

| Hardware | Minimum (Low-end) | Recommended |
| :--- | :--- | :--- |
| **RAM** | 8 GB | 16 GB |
| **CPU** | 4-core | 8-core |
| **Storage**| 20 GB free space | 50 GB free space |
| **GPU** | Not required | Not required |

## Local Deployment (Docker Compose)

The application is deployed using Docker Compose, consisting of three core services:

1.  **Frontend**: React application served via Nginx.
2.  **Backend**: FastAPI application serving the API, handling ASR, TTS, RAG, and orchestration.
3.  **Ollama**: Local LLM server running the Qwen3-4B-Instruct model (or alternatives).

### Docker Compose Configuration (`docker-compose.yml`)

```yaml
version: '3.8'

services:
  frontend:
    build:
      context: ./frontend
      dockerfile: Dockerfile
    ports:
      - "80:80"
    depends_on:
      - backend
    restart: unless-stopped

  backend:
    build:
      context: ./backend
      dockerfile: Dockerfile
    ports:
      - "8000:8000"
    environment:
      - OLLAMA_HOST=http://ollama:11434
      - DATABASE_URL=sqlite:///./data/schemes.db
      - CHROMA_DB_DIR=./data/chromadb
      - MODELS_DIR=./data/models
    volumes:
      - ./backend/data:/app/data
    depends_on:
      - ollama
    restart: unless-stopped

  ollama:
    image: ollama/ollama:latest
    ports:
      - "11434:11434"
    volumes:
      - ./ollama_data:/root/.ollama
    restart: unless-stopped
```

## Environment Setup

1.  **Clone Repository**: `git clone <repo-url>`
2.  **Create Directories**: `mkdir -p backend/data/models backend/data/chromadb ollama_data`
3.  **Environment Variables**: Create a `.env` file in the root directory (using defaults for local dev).

## Model Download Sequence

A setup script (`scripts/download_models.sh` or `.bat`) will execute before the backend starts to cache models locally.

```bash
#!/bin/bash
# scripts/download_models.sh

# 1. Start Ollama in background
ollama serve &
sleep 5

# 2. Pull LLM
ollama pull qwen:4b-instruct-q4_K_M

# 3. Download HF Models (using Python script)
python scripts/fetch_hf_models.py
# (fetch_hf_models.py downloads faster-whisper-large-v3-turbo, intfloat/multilingual-e5-small, ai4bharat/indic-parler-tts)
```

## Startup Sequence

1.  Initialize Docker Compose: `docker-compose up -d`
2.  **Ollama** starts and loads the Qwen model.
3.  **Backend** starts, waits for Ollama health check, loads ASR/TTS/Embedding models into memory, and connects to SQLite/ChromaDB.
4.  **Frontend** Nginx server starts serving static files.

## Health Checks

*   **Ollama**: `GET http://localhost:11434/api/tags`
*   **Backend**: `GET http://localhost:8000/health` (Checks DB connection, ChromaDB status, and model loaded status)
*   **Frontend**: `GET http://localhost:80/`

## Optional Free Hosting (Cloud Fallback)

While local is primary, the project can be hosted for ₹0:
*   **Frontend**: Vercel (Free Tier). Connect GitHub repo for automatic builds.
*   **Backend & Models**: HuggingFace Spaces (Free CPU Tier - 16GB RAM, 2 vCPU). Docker template.
    *   *Limitation*: HF Spaces goes to sleep after inactivity; wake-up takes 2-3 minutes.
*   **Database**: SQLite/ChromaDB stored locally on HF Spaces persistent storage (or re-indexed on startup).
