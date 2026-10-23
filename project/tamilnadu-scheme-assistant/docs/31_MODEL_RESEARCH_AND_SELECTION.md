# Model Research and Selection

## 1. Automatic Speech Recognition (ASR)
- **Decision:** `faster-whisper large-v3-turbo` (INT8 quantized)
- **Reason:** Provides excellent Tamil Word Error Rate (WER) while fitting within memory constraints through INT8 quantization. Fast CPU inference.
- **Alternatives:** `openai/whisper-large-v3`, `openai/whisper-small`
- **Why rejected:** `large-v3` is too slow on CPU. `small` lacks sufficient accuracy for Tamil domain terms.
- **Cost:** ₹0
- **Hardware:** 8GB-16GB RAM laptop, CPU only
- **License:** MIT
- **Risks:** Might struggle with very heavy regional dialects.
- **Fallback:** `whisper-small` GGUF

## 2. Large Language Model (LLM)
- **Decision:** `Qwen/Qwen3-4B-Instruct` via Ollama (4-bit GGUF)
- **Reason:** Best balance of size and multilingual capability (including Tamil). Fits comfortably in 8GB RAM while leaving room for DB and ASR.
- **Alternatives:** `Llama-3.1-8B`, `sarvamai/sarvam-2b`, `google/gemma-4-e2b`
- **Why rejected:** Llama 3.1 8B requires 16GB RAM for smooth concurrent operation. Sarvam/Gemma fallbacks have slightly less reasoning capacity for RAG.
- **Cost:** ₹0
- **Hardware:** 8-16GB RAM, CPU (Ollama)
- **License:** Apache 2.0 (or Qwen License)
- **Risks:** Occasional hallucination in Tamil generation.
- **Fallback:** `sarvam-2b` or `gemma-4-e2b`

## 3. Embedding Model
- **Decision:** `intfloat/multilingual-e5-small`
- **Reason:** 384 dimensions, ~470MB. Extremely fast on CPU, top tier multilingual MTEB benchmark performance for its size.
- **Alternatives:** `BAAI/bge-m3`
- **Why rejected:** `bge-m3` is excellent but heavy (~2.2GB), reserved only for 16GB+ systems.
- **Cost:** ₹0
- **Hardware:** Minimal CPU RAM (<1GB)
- **License:** MIT
- **Risks:** May miss complex semantic nuances compared to larger models.
- **Fallback:** `BAAI/bge-m3` (if 8GB+ RAM available)

## 4. Vector Database
- **Decision:** `ChromaDB` (local, persistent)
- **Reason:** Easy local persistence via SQLite, no heavy client-server setup needed, perfect for MVP.
- **Alternatives:** Milvus Lite, FAISS, Qdrant
- **Why rejected:** FAISS lacks native document metadata filtering out-of-the-box. Qdrant/Milvus require separate binaries or Docker containers which add overhead.
- **Cost:** ₹0
- **Hardware:** Disk space + CPU
- **License:** Apache 2.0
- **Risks:** Performance degrades >100k docs (not an issue for MVP).
- **Fallback:** FAISS with manual metadata mapping.

## 5. Reranker
- **Decision:** NOT REQUIRED FOR MVP
- **Reason:** Corpus size is small (<500 government schemes). Embedding quality from e5-small is sufficient.
- **Alternatives:** `BAAI/bge-reranker-m3`
- **Why rejected:** Adds latency to the pipeline on CPU without significant accuracy gains for small document sets.
- **Cost:** ₹0
- **Hardware:** N/A
- **License:** N/A
- **Risks:** Slightly lower precision on long-tail queries.
- **Fallback:** Add cross-encoder reranker in v2.

## 6. Text-to-Speech (TTS)
- **Decision:** `ai4bharat/indic-parler-tts`
- **Reason:** High-quality natural-sounding Tamil speech generation.
- **Alternatives:** `facebook/mms-tts-tam`, `espeak-ng`
- **Why rejected:** MMS has lower naturalness, espeak is robotic.
- **Cost:** ₹0
- **Hardware:** CPU
- **License:** Apache 2.0
- **Risks:** Slower inference time on CPU.
- **Fallback:** `facebook/mms-tts-tam` for speed, `espeak-ng` for ultra-low latency.

## 7. Intent Classification (NLU)
- **Decision:** `ai4bharat/IndicBERT` (fine-tuned)
- **Reason:** Dedicated fast classifier for intent (e.g., query, complaint, status). Faster than prompting an LLM for classification.
- **Alternatives:** LLM zero-shot, FastText
- **Why rejected:** LLM is too slow for every turn. FastText lacks contextual understanding.
- **Cost:** ₹0
- **Hardware:** Minimal CPU footprint
- **License:** MIT
- **Risks:** Requires custom training dataset.
- **Fallback:** Heuristic keyword matching.

## 8. Named Entity Recognition (NER)
- **Decision:** AI4Bharat `IndicNER`
- **Reason:** Pretrained model ready to extract Tamil entities (locations, names, dates).
- **Alternatives:** LLM extraction
- **Why rejected:** LLM is slow and expensive for simple entity extraction.
- **Cost:** ₹0
- **Hardware:** CPU
- **License:** MIT
- **Risks:** Might miss niche government terminology.
- **Fallback:** Regex and dictionary lookups.

## 9. Language Detection
- **Decision:** `lingua-py`
- **Reason:** High accuracy for short text and mixed-language inputs. Fast and works entirely offline.
- **Alternatives:** `fasttext` language identifier
- **Why rejected:** Fasttext sometimes struggles with code-mixed Tanglish.
- **Cost:** ₹0
- **Hardware:** CPU
- **License:** Apache 2.0
- **Risks:** Over-classification on single words.
- **Fallback:** Unicode script detection as fast pre-filter.

## 10. OCR (Document Processing)
- **Decision:** `Surya OCR`
- **Reason:** Superior performance on complex layouts and multilingual documents compared to legacy tools.
- **Alternatives:** `EasyOCR`, Tesseract, `pdfminer.six`
- **Why rejected:** Tesseract struggles with Tamil formatting. EasyOCR is slightly less accurate for dense tables.
- **Cost:** ₹0
- **Hardware:** CPU (though slower than GPU)
- **License:** GPL-3.0
- **Risks:** Slow inference on large PDFs on CPU.
- **Fallback:** `EasyOCR` (faster), `pdfminer.six` for native text PDFs.
