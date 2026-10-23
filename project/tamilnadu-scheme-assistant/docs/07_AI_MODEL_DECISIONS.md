# 07 AI Model Decisions

This document outlines the specific AI models chosen for the Tamil Nadu Multilingual Voice-Based Government Scheme Assistant, targeting a ₹0 core functionality operating cost on student laptops (8-16GB RAM, CPU-only).

## 1. Automatic Speech Recognition (ASR)
- **Primary:** `faster-whisper` with `large-v3-turbo` (INT8 quantized)
- **Fallback:** `whisper-small` (GGUF format)
- **Dev/Offline Alternative:** Browser Web Speech API
- **HuggingFace ID:** `Systran/faster-whisper-large-v3-turbo`
- **Parameters:** ~809M (large-v3-turbo)
- **RAM/VRAM:** ~1.5GB RAM for INT8 / 0 VRAM
- **CPU Latency:** ~2-3 seconds per 10s audio
- **Tamil Quality:** High
- **English Quality:** Very High
- **License:** MIT
- **Quantization:** INT8 (CTranslate2)
- **Student Laptop Feasibility:** Excellent.

## 2. Large Language Model (LLM)
- **Primary (8GB RAM):** Qwen3-4B-Instruct via Ollama
- **Primary (16GB RAM):** Llama-3.1-8B-Instruct
- **Ultra-low Fallback:** Sarvam-2B / Gemma-4-E2B
- **HuggingFace ID:** `Qwen/Qwen2.5-3B-Instruct` (Note: Qwen3 is a placeholder for the latest available 3-4B Qwen model)
- **Parameters:** ~3-4B
- **RAM/VRAM:** ~4GB RAM for 4-bit GGUF
- **CPU Latency:** ~10-15 tokens/sec
- **Tamil Quality:** Good (especially Llama 3.1 and Sarvam)
- **English Quality:** Excellent
- **License:** Apache 2.0 / Llama-3.1 License
- **Quantization:** 4-bit (GGUF)
- **Student Laptop Feasibility:** Excellent (4B model fits in 8GB RAM).

## 3. Embeddings (RAG)
- **Primary:** `intfloat/multilingual-e5-small`
- **Fallback (8GB+ RAM):** `BAAI/bge-m3`
- **HuggingFace ID:** `intfloat/multilingual-e5-small`
- **Parameters:** 118M
- **RAM/VRAM:** ~300MB RAM
- **CPU Latency:** < 50ms per query
- **Tamil Quality:** Good
- **English Quality:** Excellent
- **License:** MIT
- **Quantization:** FP32/FP16
- **Student Laptop Feasibility:** Excellent.

## 4. Intent Classification
- **Primary:** IndicBERT fine-tuned classifier
- **HuggingFace ID:** `ai4bharat/indic-bert`
- **Parameters:** 33M (albert base)
- **RAM/VRAM:** ~200MB RAM
- **CPU Latency:** < 20ms
- **Tamil Quality:** Excellent
- **License:** MIT
- **Quantization:** FP32
- **Student Laptop Feasibility:** Excellent.

## 5. Named Entity Recognition (NER)
- **Primary:** AI4Bharat IndicNER
- **HuggingFace ID:** `ai4bharat/IndicNER`
- **Parameters:** ~100-300M
- **RAM/VRAM:** ~500MB RAM
- **CPU Latency:** < 100ms
- **Tamil Quality:** Excellent
- **License:** MIT
- **Quantization:** FP32
- **Student Laptop Feasibility:** Excellent.

## 6. Language Detection
- **Primary:** lingua-py
- **Filter:** Unicode script detection
- **RAM/VRAM:** ~100MB RAM
- **CPU Latency:** < 5ms
- **Student Laptop Feasibility:** Excellent.

## 7. Text-to-Speech (TTS)
- **Primary:** `ai4bharat/indic-parler-tts`
- **Fallback:** `facebook/mms-tts-tam`
- **Ultra-low Fallback:** `espeak-ng`
- **HuggingFace ID:** `ai4bharat/indic-parler-tts`
- **Parameters:** ~200M
- **RAM/VRAM:** ~1GB RAM
- **CPU Latency:** ~2-5s per sentence
- **Tamil Quality:** Excellent
- **English Quality:** Good
- **License:** MIT / CC-BY-NC (check specific Parler model)
- **Quantization:** FP32
- **Student Laptop Feasibility:** Feasible, but CPU inference can be slow.

## 8. Optical Character Recognition (OCR)
- **Primary:** Surya OCR
- **Fallback:** EasyOCR
- **RAM/VRAM:** ~2GB RAM
- **CPU Latency:** ~5-10s per page
- **Tamil Quality:** Very Good
- **License:** GPLv3
- **Student Laptop Feasibility:** Good.

## 9. Reranker
- **Decision:** NOT REQUIRED FOR MVP
- **Why:** Saves ~1GB RAM and 500ms CPU latency. Standard vector search + FTS5 is sufficient for MVP.

---

### Hardware Requirements Table (Target: CPU Only)

| Component | Target RAM Usage | Storage Requirement | Expected Latency (CPU) |
| :--- | :--- | :--- | :--- |
| ASR (INT8) | ~1.5 GB | ~1.5 GB | 2-3 sec |
| LLM (4B 4-bit) | ~3.5 GB | ~2.5 GB | 10-15 tok/sec |
| Embeddings | ~0.3 GB | ~0.5 GB | < 50ms |
| TTS | ~1.0 GB | ~1.0 GB | 2-5 sec |
| Vector DB/Backend | ~0.5 GB | ~1.0 GB | N/A |
| **Total (Max Concurrent)** | **~6.8 GB** | **~6.5 GB** | **Fits in 8GB Laptop** |
