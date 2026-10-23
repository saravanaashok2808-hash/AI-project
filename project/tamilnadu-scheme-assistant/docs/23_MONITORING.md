# Monitoring & Observability

This document outlines the monitoring strategy for the scheme assistant. To ensure privacy and zero cost, no third-party cloud analytics or tracking services (e.g., Datadog, Sentry, Google Analytics) are used. All logging and monitoring are done locally.

## Core Principles
- **Privacy First**: No PII or user audio is logged or transmitted.
- **Local Only**: Metrics are stored locally in SQLite or structured log files.
- **₹0 Cost**: Built entirely with standard library tools and basic endpoints.

## 1. Request Latency Tracking

We track latency for the major pipeline steps to ensure responsiveness on CPU-only hardware.

| Component | Target Latency (CPU) | Logging Location |
| :--- | :--- | :--- |
| **ASR (faster-whisper)** | < 2.0s | Application Logs |
| **RAG (Embedding + ChromaDB)** | < 0.5s | Application Logs |
| **LLM (Ollama - TTFT)** | < 1.5s | Application Logs |
| **LLM (Ollama - Generation)** | ~15-20 tokens/sec | Application Logs |
| **TTS (ai4bharat/indic-parler-tts)**| < 3.0s | Application Logs |
| **End-to-End Voice-to-Voice** | < 10s | Application Logs |

## 2. Structured Logging (JSON)

The FastAPI backend uses Python's `logging` module configured to output JSON. This allows easy parsing if we ever build a local admin dashboard.

**Example Log Entry:**
```json
{
  "timestamp": "2023-10-25T14:32:01Z",
  "level": "INFO",
  "event": "query_processed",
  "session_id": "uuid-1234",
  "metrics": {
    "asr_duration_ms": 1200,
    "rag_duration_ms": 300,
    "llm_duration_ms": 4500,
    "tts_duration_ms": 2100,
    "total_duration_ms": 8100
  },
  "status": "success"
}
```

## 3. Error Rate Tracking

Errors are logged with specific exception types and stack traces.
- `ASRError`: Failed to transcribe audio.
- `LLMTimeout`: Ollama failed to respond in time.
- `RAGEmpty`: No relevant context found in ChromaDB.
- `TTSFailure`: Failed to generate audio.

Error rates are tracked in a lightweight SQLite table `system_metrics` for local review.

## 4. Retrieval Quality Metrics

Since we don't have human-in-the-loop for real-time rating, we rely on LLM self-evaluation during the generation phase and log the results:
- **Context Relevance**: The LLM prompt asks it to output a `[SOURCES_USED: Yes/No]` token before the response. We parse this to track if RAG is actually helping.
- **Unanswered Queries**: If the LLM falls back to the "I don't know" prompt, we log the query intent to improve the database later.

## 5. Health Endpoints

The backend exposes a `/health` endpoint for Docker Compose and general status checks.

```json
// GET /health
{
  "status": "healthy",
  "components": {
    "database": "connected",
    "chromadb": "connected",
    "ollama": "reachable",
    "models_loaded": {
      "asr": true,
      "embedding": true,
      "tts": true
    }
  },
  "uptime_seconds": 3600,
  "memory_usage_mb": 4500
}
```
