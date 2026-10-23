# 26 — Antigravity Build Instructions

## Overview
This document specifies the step-by-step instructions for executing and implementing the **Tamil Nadu Multilingual Voice-Based Government Scheme Assistant** within the **Antigravity** development environment.

Antigravity operates with direct filesystem, terminal, and execution access. Every phase must be executed systematically following the verified ₹0-cost architecture.

---

## Phase Execution Matrix

| Phase | Phase Name | Primary Focus | Output Files / Artifacts |
| :--- | :--- | :--- | :--- |
| **Phase 0** | Research & Architecture | Ecosystem research & locked decisions | `docs/00` to `docs/47` |
| **Phase 1** | Project Foundation | Directory structure, Backend (FastAPI), Frontend (Vite), DB setup | `backend/`, `frontend/`, `data/` |
| **Phase 2** | Government Data Foundation | Knowledge base population, Tamil/English scheme data, schema | `data/schemes/`, `scripts/ingest_schemes.py` |
| **Phase 3** | RAG Engine | ChromaDB vector store, E5 embedding pipeline, FTS5 keyword search | `rag/`, `ai/embeddings/` |
| **Phase 4** | Eligibility Engine | Deterministic rule parser, criteria evaluator, progressive profiling | `eligibility/` |
| **Phase 5** | AI Assistant & NLU | Intent classification, entity extraction, Ollama/LLM prompt grounding | `ai/nlu/`, `ai/llm/`, `backend/app/services/` |
| **Phase 6** | Voice Engine | Audio capture, faster-whisper ASR, language detection, Indic TTS | `ai/asr/`, `ai/tts/` |
| **Phase 7** | Frontend Web App | Accessible, mobile-first Tamil/English UI, voice recorder, scheme cards | `frontend/src/` |
| **Phase 8** | Security & Privacy | Prompt injection defenses, URL allowlist, session ephemeral stores | `backend/app/core/security.py` |
| **Phase 9** | Evaluation & Benchmarks | Test suite, synthetic queries, ground truth retrieval & eligibility | `evaluation/`, `tests/` |
| **Phase 10** | Local & Free Deployment | Docker Compose, setup scripts, zero-cost deployment configurations | `docker-compose.yml`, `scripts/` |

---

## Detailed Phase Build Specifications

```
PHASE 0 (Research & Specs)
       │
       ▼
PHASE 1 (Foundation: FastAPI + SQLite + Vite Frontend)
       │
       ▼
PHASE 2 (Verified TN Government Scheme Data & Validation)
       │
       ▼
PHASE 3 (Hybrid RAG: Vector + Keyword Search)
       │
       ▼
PHASE 4 (Deterministic Eligibility Rules Engine)
       │
       ▼
PHASE 5 (AI Assistant: NLU + Prompt Grounding)
       │
       ▼
PHASE 6 (Voice Engine: Faster-Whisper ASR + Indic TTS)
       │
       ▼
PHASE 7 (Complete Responsive Web UI)
       │
       ▼
PHASE 8 (Security & Privacy Hardening)
       │
       ▼
PHASE 9 (Verification & Evaluation Suite)
       │
       ▼
PHASE 10 (Docker & Production Deployment)
```

---

### PHASE 1: Project Foundation

#### Goal
Set up the core project foundation including FastAPI backend, React+Vite frontend, SQLite database with FTS5, and local development orchestration.

#### Prerequisites
- Node.js (v18+)
- Python (v3.10+)
- Virtual environment (`venv`)

#### Input Files
- `README.md`
- `docs/06_TECH_STACK_DECISIONS.md`
- `docs/14_DATABASE_SCHEMA.md`

#### Files to Create
- `backend/requirements.txt`
- `backend/app/main.py`
- `backend/app/core/config.py`
- `backend/app/core/database.py`
- `backend/app/models/scheme.py`
- `backend/app/models/session.py`
- `backend/app/api/schemes.py`
- `backend/app/api/health.py`
- `backend/.env.example`
- `frontend/package.json`
- `frontend/src/App.tsx`
- `frontend/src/main.tsx`

#### Dependencies
- **Backend:** `fastapi`, `uvicorn`, `pydantic`, `aiosqlite`, `python-dotenv`
- **Frontend:** `react`, `react-dom`, `vite`, `tailwindcss`, `lucide-react`

#### Verification Commands
```bash
# Backend test run
cd backend && uvicorn app.main:app --host 127.0.0.1 --port 8000
# Frontend build test
cd frontend && npm.cmd run build
```

#### Acceptance Criteria
- `GET http://127.0.0.1:8000/api/health` returns `{"status": "ok"}`
- SQLite database initializes with `schemes` and `schemes_fts` tables
- Frontend dev server starts cleanly without bundling errors

---

### PHASE 2: Government Data Foundation

#### Goal
Populate an authoritative, structured database of Tamil Nadu government schemes with rich Tamil and English metadata, verifiable official URLs, and formal eligibility rule schemas.

#### Prerequisites
- Phase 1 completed
- `docs/11_KNOWLEDGE_BASE_SCHEMA.md`
- `docs/12_DATA_SOURCES.md`

#### Files to Create
- `data/schemes/tn_schemes_verified.json`: Authoritative dataset of core TN welfare schemes (KMUT, Pudhumai Penn, CMCHIS, Moovalur Ramamirtham, OAP, Farmer Subsidies, etc.)
- `scripts/ingest_schemes.py`: Data validation and SQLite database ingestion script
- `backend/app/services/scheme_service.py`: High-performance scheme querying and retrieval service

#### Acceptance Criteria
- Database successfully populated with verified TN schemes
- All schemes contain official `.tn.gov.in` or `.gov.in` URLs and last-verified timestamps
- Full-Text Search (FTS5) queries succeed in both Tamil and English

---

### PHASE 3: RAG Engine (Vector & Hybrid Search)

#### Goal
Implement zero-cost local hybrid retrieval (dense semantic search + sparse FTS5 keyword matching) to extract relevant scheme facts.

#### Prerequisites
- Phase 2 verified
- `docs/09_RAG_ARCHITECTURE.md`
- `docs/39_EMBEDDING_AND_RERANKING_MODELS.md`

#### Files to Create
- `rag/hybrid_retriever.py`: Hybrid search coordinator combining lexical scoring and vector similarity
- `rag/vector_store.py`: ChromaDB wrapper with local SQLite persistence
- `ai/embeddings/embedder.py`: Local embedding generator (`multilingual-e5-small` / ONNX runtime fallback)

#### Acceptance Criteria
- Semantic queries in Tamil (e.g., "விவசாயிகளுக்கு என்ன திட்டம் இருக்கு?") retrieve farmer-related schemes
- English queries (e.g., "health insurance for poor") retrieve CMCHIS
- Tanglish queries (e.g., "college padikra ponnungalukku aid") retrieve Pudhumai Penn scheme

---

### PHASE 4: Deterministic Eligibility Engine

#### Goal
Implement deterministic, rule-based eligibility evaluation. The LLM must NEVER decide eligibility by hallucination.

#### Prerequisites
- Phase 2 scheme JSON with structured rules
- `docs/10_ELIGIBILITY_ENGINE.md`

#### Files to Create
- `eligibility/rule_evaluator.py`: Rule parsing and logical condition matching (Age, Gender, Income, Caste, District, Occupation)
- `eligibility/profiler.py`: Session profile manager and missing information detector
- `backend/app/api/eligibility.py`: REST endpoints for evaluating user profiles against specific schemes

#### Acceptance Criteria
- Categorizes user state into: `ELIGIBLE`, `POTENTIALLY_ELIGIBLE`, `NOT_APPEARING_ELIGIBLE`, `INSUFFICIENT_INFORMATION`
- Accurately details satisfied rules, violated rules, and missing variables (e.g., annual income missing)

---

### PHASE 5: AI Assistant & NLU

#### Goal
Connect query understanding, intent classification, entity extraction, and prompt-grounded LLM responses via Ollama (Qwen2.5/Qwen3 or Sarvam-2B).

#### Prerequisites
- Phase 3 & 4 completed
- `docs/27_AI_PROMPTS.md`
- Local LLM runner (Ollama or local fallback pipeline)

#### Files to Create
- `ai/nlu/intent_classifier.py`: Fast rule + transformer intent classifier
- `ai/nlu/entity_extractor.py`: Profiling entity extractor (age, income, location, occupation)
- `ai/llm/llm_client.py`: Ollama API client with grounded prompt templates
- `backend/app/services/assistant_service.py`: Orchestrator connecting NLU, RAG, Eligibility, and LLM explanation

#### Acceptance Criteria
- Answers are strictly grounded in retrieved scheme data
- Official links and verification dates are automatically appended
- Responds in matching language (Tamil, English, or Tanglish)

---

### PHASE 6: Voice Pipeline (ASR + TTS)

#### Goal
Implement zero-cost voice input and speech synthesis.

#### Prerequisites
- `docs/08_VOICE_ARCHITECTURE.md`
- `docs/38_TTS_MODEL_STRATEGY.md`

#### Files to Create
- `ai/asr/transcriber.py`: `faster-whisper` wrapper with INT8 quantization
- `ai/tts/synthesizer.py`: Indic TTS / MMS-TTS engine with web-native audio streaming
- `backend/app/api/voice.py`: Audio upload, transcription, and TTS endpoints

#### Acceptance Criteria
- Audio inputs in Tamil/English/Tanglish transcribe with acceptable WER
- Tamil text synthesizes to intelligible audio without requiring paid cloud APIs

---

### PHASE 7: Web Frontend

#### Goal
Build a responsive, mobile-first React web application with accessibility and Tamil language support.

#### Prerequisites
- All backend endpoints operational
- `docs/16_FRONTEND_ARCHITECTURE.md`

#### Files to Create
- `frontend/src/components/AudioRecorder.tsx`: Voice input with audio visualizer
- `frontend/src/components/SchemeCard.tsx`: Rich scheme display with eligibility badges
- `frontend/src/components/ChatInterface.tsx`: Multilingual chat container
- `frontend/src/components/ProfileDrawer.tsx`: User profile inspection and editing

#### Acceptance Criteria
- Seamless switching between Tamil and English UI
- One-click voice recording with instant playback and transcription
- High contrast, large fonts, and mobile responsiveness verified

---

### PHASE 8: Security & Privacy Hardening

#### Goal
Apply production defenses against prompt injection, fake URLs, and privacy violations.

#### Prerequisites
- `docs/18_SECURITY.md`
- `docs/19_PRIVACY.md`

#### Files to Create
- `backend/app/core/security.py`: Domain allowlist verification, input sanitization, prompt delimiter guards
- `backend/app/core/rate_limiter.py`: Request throttling

#### Acceptance Criteria
- Rejects non-government URLs and phishing attempts
- RAG evidence is wrapped in strict data boundaries to prevent instruction overriding
- No personal identifiable information is saved to persistent disk

---

### PHASE 9: Testing & Evaluation Benchmarks

#### Goal
Validate end-to-end functionality across all components using reproducible benchmarks.

#### Prerequisites
- `docs/20_EVALUATION.md`
- `docs/21_TESTING.md`

#### Files to Create
- `tests/test_eligibility.py`: Rule validation unit tests
- `tests/test_rag.py`: Search and retrieval accuracy tests
- `tests/test_api.py`: FastAPI endpoint integration tests
- `evaluation/run_benchmarks.py`: Automated performance and groundedness scoring

#### Acceptance Criteria
- 100% of unit tests pass
- Zero hallucinations on unlisted schemes
- Accurate citation of official sources in 100% of responses

---

### PHASE 10: Production Setup & Local Orchestration

#### Goal
Package the complete system into self-contained Docker Compose and local execution scripts.

#### Prerequisites
- Phases 1-9 complete

#### Files to Create
- `docker-compose.yml`: Multi-container configuration (Frontend, Backend, Ollama)
- `docker/Dockerfile.backend`
- `docker/Dockerfile.frontend`
- `scripts/start_local.bat` / `scripts/start_local.sh`: One-click startup scripts

#### Acceptance Criteria
- Clean deployment on any 8GB+ RAM Windows/Linux machine
- Fully operable at ₹0 financial cost without third-party API dependencies
