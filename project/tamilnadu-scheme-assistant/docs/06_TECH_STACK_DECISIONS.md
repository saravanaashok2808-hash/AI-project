# 06 Tech Stack Decisions

All technology decisions are optimized for running on a standard student laptop (8-16GB RAM, no GPU) with ₹0 operating cost for core MVP functionality.

## 1. Backend Framework
**Decision:** Python FastAPI (Python 3.10+)
- **Evidence:** Native async support, high performance (Starlette), automatic validation (Pydantic), seamless integration with Python AI/ML ecosystem.
- **Alternatives:** Flask, Django, Express.js.
- **Why rejected:** Flask/Django lack native async performance for streaming IO. Node.js/Express requires brittle inter-process communication with Python AI scripts.
- **License:** MIT
- **Hardware Profile:** Low CPU/RAM overhead (~100MB idle).
- **₹0 feasibility:** 100% Free and open-source.
- **Risks:** Memory leaks when hosting ML models in the same process.
- **Fallback:** Flask (if async becomes too complex).

## 2. Frontend Framework
**Decision:** React + Vite + Tailwind CSS + shadcn/ui (Node.js 18+)
- **Evidence:** Fast builds (Vite), component reuse, accessible UI (shadcn/ui), utility-first styling (Tailwind).
- **Alternatives:** Next.js, Vue, Angular.
- **Why rejected:** Next.js SSR is unnecessary overhead for a local/client-heavy app. Vue/Angular have smaller communities for pre-built accessible components.
- **License:** MIT
- **Hardware Profile:** Lightweight client-side execution.
- **₹0 feasibility:** 100% Free.
- **Risks:** Bundle size bloating with large audio libraries.
- **Fallback:** Plain HTML/JS + CSS (if build tools fail).

## 3. Database
**Decision:** SQLite with FTS5
- **Evidence:** Zero-configuration, local file-based, fast full-text search (FTS5) for scheme text.
- **Alternatives:** PostgreSQL, MySQL, MongoDB.
- **Why rejected:** Too heavy for a local student laptop deployment. Requires separate server processes.
- **License:** Public Domain
- **Hardware Profile:** Minimal footprint.
- **₹0 feasibility:** 100% Free.
- **Risks:** Concurrent write locks (mitigated by read-heavy workload).
- **Fallback:** JSON files.

## 4. Vector Database
**Decision:** ChromaDB (Local, Persistent)
- **Evidence:** Native Python support, uses SQLite/Parquet under the hood, no separate server needed.
- **Alternatives:** Qdrant, Milvus, Pinecone, FAISS.
- **Why rejected:** Pinecone is cloud-only (violates ₹0 local rule). Milvus/Qdrant require Docker/server overhead. FAISS lacks metadata filtering.
- **License:** Apache 2.0
- **Hardware Profile:** ~200MB RAM overhead.
- **₹0 feasibility:** 100% Free.
- **Risks:** Slower on extremely large datasets (not an issue for <10,000 schemes).
- **Fallback:** FAISS (if ChromaDB proves too heavy).

## 5. LLM Inference
**Decision:** Ollama
- **Evidence:** Provides 4-bit quantization (GGUF) out of the box, optimized for CPU/Metal, drop-in OpenAI-compatible API.
- **Alternatives:** vLLM, llama.cpp (direct), HuggingFace Transformers.
- **Why rejected:** vLLM requires GPU. HF Transformers is too slow/heavy on CPU. llama.cpp is good but Ollama wraps it with a better API and model management.
- **License:** MIT
- **Hardware Profile:** 8GB RAM minimum for 4B models.
- **₹0 feasibility:** 100% Free.
- **Risks:** Background process management across different OS.
- **Fallback:** llama-cpp-python.

## 6. ASR Inference
**Decision:** faster-whisper
- **Evidence:** CTranslate2 backend is up to 4x faster than standard whisper on CPU. Supports INT8 quantization.
- **Alternatives:** OpenAI Whisper (original), Transformers pipeline, Whisper.cpp.
- **Why rejected:** Original Whisper is too slow on CPU. Whisper.cpp requires C++ compilation.
- **License:** MIT
- **Hardware Profile:** ~1.5GB RAM for INT8 models.
- **₹0 feasibility:** 100% Free.
- **Risks:** CTranslate2 compatibility on older Windows machines.
- **Fallback:** Web Speech API (browser native, but requires internet).

## 7. NLU / RAG Embeddings
**Decision:** HuggingFace Transformers
- **Evidence:** Industry standard, easy loading of SentenceTransformers.
- **Alternatives:** API-based (OpenAI/Cohere), ONNX Runtime.
- **Why rejected:** API violates local/₹0 requirement. ONNX is good but requires conversion overhead for MVP.
- **License:** Apache 2.0
- **Hardware Profile:** ~500MB RAM for small embedding models.
- **₹0 feasibility:** 100% Free.
- **Risks:** Slow loading times.
- **Fallback:** ONNX Runtime.

## 8. TTS (Text-to-Speech)
**Decision:** Direct model loading (PyTorch/Transformers)
- **Evidence:** Best way to run Indic models locally.
- **Alternatives:** Cloud APIs (Google/AWS), OS native TTS.
- **Why rejected:** Cloud APIs cost money. OS native TTS has poor Tamil support.
- **License:** Model dependent (mostly Apache 2.0/MIT)
- **Hardware Profile:** ~1GB RAM.
- **₹0 feasibility:** 100% Free.
- **Risks:** Slow generation on CPU.
- **Fallback:** espeak-ng.

## 9. OCR (Optical Character Recognition)
**Decision:** Surya OCR (Primary) + pdfminer.six (Native PDFs)
- **Evidence:** Surya provides state-of-the-art multilingual OCR. pdfminer.six handles digital text perfectly.
- **Alternatives:** Tesseract, EasyOCR.
- **Why rejected:** Tesseract struggles with complex Tamil layouts. EasyOCR is a fallback but slightly less accurate than Surya.
- **License:** GPLv3 (Surya) / MIT (pdfminer)
- **Hardware Profile:** ~2GB RAM for Surya.
- **₹0 feasibility:** 100% Free.
- **Risks:** Surya is slow on CPU.
- **Fallback:** EasyOCR.

## 10. Language Detection
**Decision:** lingua-py + Unicode Script Detection
- **Evidence:** lingua-py is highly accurate for short text. Unicode script detection provides a zero-latency pre-filter.
- **Alternatives:** fasttext, langdetect.
- **Why rejected:** fasttext is heavier. langdetect is less accurate for Tanglish.
- **License:** MIT
- **Hardware Profile:** ~100MB RAM.
- **₹0 feasibility:** 100% Free.
- **Risks:** Tanglish detection edge cases.
- **Fallback:** fasttext.

## 11. Deployment
**Decision:** Docker Compose (Local)
- **Evidence:** Ensures reproducible environments for student laptops.
- **Alternatives:** Manual pip/npm installs.
- **Why rejected:** Prone to dependency hell on Windows.
- **License:** Apache 2.0
- **Hardware Profile:** Slight container overhead.
- **₹0 feasibility:** 100% Free.
- **Risks:** Docker Desktop resource usage on Windows.
- **Fallback:** Manual setup scripts.
