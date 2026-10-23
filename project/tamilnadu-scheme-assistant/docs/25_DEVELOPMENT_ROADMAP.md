# Development Roadmap

This roadmap defines the phase-by-phase implementation plan for the Tamil Nadu Government Scheme Assistant.

## Phase 0: Project Setup & Infrastructure (Day 1)
*   **Goal**: Establish repositories, environment, and core dependencies.
*   **Tasks**: Initialize Git, create Python venv, setup React+Vite, create folder structure.
*   **Files**: `requirements.txt`, `package.json`, `docker-compose.yml`, `README.md`.
*   **Dependencies**: FastAPI, React, Tailwind.
*   **Acceptance**: API returns 200 OK; React app displays basic placeholder.
*   **Time**: 2 hours.

## Phase 1: Data Ingestion & Database Setup (Day 1)
*   **Goal**: Scrape/load initial scheme data and setup SQLite + ChromaDB.
*   **Tasks**: Create SQLite schema, implement JSON data loader, setup ChromaDB client.
*   **Files**: `backend/db/schema.sql`, `backend/db/vector_store.py`, `data/schemes_mock.json`.
*   **Dependencies**: `sqlite3`, `chromadb`.
*   **Acceptance**: Can successfully insert and retrieve a mock scheme from both databases.
*   **Time**: 3 hours.

## Phase 2: Embedding & Retrieval (RAG) Pipeline (Day 2)
*   **Goal**: Implement local text embeddings and semantic search.
*   **Tasks**: Integrate `multilingual-e5-small`, create chunking logic, implement similarity search.
*   **Files**: `backend/models/embedding.py`, `backend/rag/retriever.py`.
*   **Dependencies**: `transformers`, `sentence-transformers`.
*   **Acceptance**: Querying "education for girls" returns the Moovalur Ramamirtham scheme context.
*   **Time**: 4 hours.

## Phase 3: LLM Integration (Ollama) (Day 2)
*   **Goal**: Connect to local Ollama and generate responses based on RAG context.
*   **Tasks**: Install Ollama, pull Qwen3-4B-Instruct, write prompt templates, create LLM service.
*   **Files**: `backend/models/llm.py`, `backend/rag/prompts.py`.
*   **Dependencies**: `requests` (to Ollama API), `ollama`.
*   **Acceptance**: LLM accurately answers a question using *only* the provided context.
*   **Time**: 3 hours.

## Phase 4: Speech-to-Text (ASR) Integration (Day 3)
*   **Goal**: Implement local Tamil voice recognition.
*   **Tasks**: Integrate `faster-whisper`, handle audio file uploads, convert to text.
*   **Files**: `backend/models/asr.py`, `backend/api/routes.py`.
*   **Dependencies**: `faster-whisper`.
*   **Acceptance**: Uploading a Tamil `.wav` file returns accurate Tamil text.
*   **Time**: 3 hours.

## Phase 5: Text-to-Speech (TTS) Integration (Day 3)
*   **Goal**: Implement local Tamil voice generation.
*   **Tasks**: Integrate `indic-parler-tts`, convert LLM output to audio stream.
*   **Files**: `backend/models/tts.py`.
*   **Dependencies**: `transformers`, `soundfile`.
*   **Acceptance**: LLM text output is converted to a playable `.wav` file in Tamil.
*   **Time**: 4 hours.

## Phase 6: API Orchestration (Day 4)
*   **Goal**: Tie ASR -> RAG -> LLM -> TTS together into a single API endpoint.
*   **Tasks**: Create the `/api/chat` endpoint, handle end-to-end flow, add error handling.
*   **Files**: `backend/api/chat.py`, `backend/services/orchestrator.py`.
*   **Dependencies**: FastAPI.
*   **Acceptance**: Single API call takes audio in, returns audio + text out.
*   **Time**: 3 hours.

## Phase 7: Frontend Development (UI/UX) (Day 4)
*   **Goal**: Build the user interface for voice interaction.
*   **Tasks**: Create mic button, chat interface, audio playback, integrate with backend API.
*   **Files**: `frontend/src/App.jsx`, `frontend/src/components/Chat.jsx`.
*   **Dependencies**: `lucide-react`, `shadcn/ui`.
*   **Acceptance**: User can click mic, speak, see transcription, and hear response.
*   **Time**: 5 hours.

## Phase 8: Testing & Refinement (Day 5)
*   **Goal**: Optimize latency, fix bugs, improve prompt engineering.
*   **Tasks**: Quantize models if needed, test edge cases, refine prompts to stop hallucinations.
*   **Files**: All files (refactoring).
*   **Acceptance**: End-to-end latency < 10s on target hardware.
*   **Time**: 6 hours.

## Phase 9: Documentation & Dockerization (Day 5)
*   **Goal**: Prepare for submission.
*   **Tasks**: Write README, finalize Docker Compose, record demo video.
*   **Files**: `docker-compose.yml`, `README.md`.
*   **Acceptance**: `docker-compose up` launches the fully working app on a fresh machine.
*   **Time**: 3 hours.
