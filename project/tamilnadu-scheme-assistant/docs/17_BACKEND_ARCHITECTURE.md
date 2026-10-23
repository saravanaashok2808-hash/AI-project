# Backend Architecture

## 1. Decision: Framework & Pattern
* **Framework:** FastAPI (Python)
* **Design Pattern:** Modular Monolith with Service Layer Pattern.
* **Reasoning:** FastAPI handles async I/O well (needed for LLM/ASR streaming). A modular monolith avoids the complexity of microservices for an MVP.
* **Alternatives Rejected:** Flask (lacks native async/Pydantic), Django (too heavy for API-first AI wrappers).
* **Cost:** ₹0.

## 2. Core Components
* **API Layer (Routers):** Handles HTTP requests, Pydantic validation.
* **Service Layer:** Business logic, orchestrates AI models.
* **Data Access Layer:** SQLite/ChromaDB queries.

## 3. AI Service Integration
* **ASR Service:** `faster-whisper` (large-v3-turbo INT8).
* **NLU Service:** IndicBERT intent classification & IndicNER.
* **LLM Service:** Connects to local `Ollama` running `Qwen3-4B-Instruct` (4-bit GGUF).
* **TTS Service:** `ai4bharat/indic-parler-tts` directly via Transformers.
* **Hardware Profile:** Optimized for 8-16GB RAM without GPU.

## 4. Database & RAG
* **Relational DB:** SQLite with `aiosqlite` and FTS5 for scheme metadata and sessions.
* **Vector DB:** ChromaDB (local, persistent) for RAG chunk retrieval.
* **Embedding Model:** `intfloat/multilingual-e5-small`.

## 5. Other Subsystems
* **Eligibility Service:** Evaluates user profile attributes against scheme rules.
* **Session Management:** In-memory + SQLite fallback. Stores conversation history.
* **Middleware:** Error handling (transforms to standard JSON), Logging, CORS.
* **Config:** `pydantic-settings` pulling from `.env`.

## 6. Startup/Shutdown Lifecycle
```python
@app.on_event("startup")
async def startup_event():
    # Load AI models into memory
    # Initialize DB connections
    # Check Ollama service health
```
