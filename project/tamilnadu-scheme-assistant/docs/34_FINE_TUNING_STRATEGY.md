# Fine-Tuning Strategy

## 1. Core Decisions

### 1.1 ASR (Speech-to-Text)
- **Decision:** DO NOT FINE-TUNE FOR MVP.
- **Reason:** `faster-whisper large-v3-turbo` (INT8) yields a sufficiently low Word Error Rate (WER) out of the box for standard Tamil speech.
- **Cost:** ₹0
- **Hardware:** 8GB RAM Laptop CPU

### 1.2 NLU Intent Classification
- **Decision:** FINE-TUNE `IndicBERT`.
- **Reason:** We need a fast, low-latency classifier capable of handling Tamil, English, and code-mixed (Tanglish) queries for 17 specific application intents. Pre-trained models do not map to custom application intents out of the box.
- **Details:** Full fine-tuning on ~500 annotated examples.
- **Cost:** ₹0 (can be trained on CPU in minutes).

### 1.3 NLU Named Entity Recognition (NER)
- **Decision:** DO NOT FINE-TUNE FOR MVP.
- **Reason:** AI4Bharat `IndicNER` already extracts standard entities (Location, Name, Date) robustly. Scheme-specific entities will be handled via SQLite/FTS5 exact matching instead of NER fine-tuning.

### 1.4 Large Language Model (LLM)
- **Decision:** DO NOT FINE-TUNE FOR MVP.
- **Reason:** `Qwen3-4B-Instruct` has excellent base multilingual capabilities. Combining it with RAG (Retrieval-Augmented Generation) and highly structured prompts provides fully grounded, hallucination-free responses without the massive overhead of QLoRA tuning on 8GB RAM.
- **Cost:** ₹0

### 1.5 Text-to-Speech (TTS)
- **Decision:** DO NOT FINE-TUNE FOR MVP.
- **Reason:** `indic-parler-tts` and `mms-tts-tam` provide acceptable to high quality synthetic voices out of the box. Voice cloning or style transfer is out of scope for the MVP.

## 2. Alternatives & Risks
- **Why rejected LLM Fine-Tuning:** LLM fine-tuning risks catastrophic forgetting of the model's base conversational abilities and requires GPU access (Google Colab/Kaggle). RAG is safer and allows real-time data updates.
- **Risks:** The lack of ASR fine-tuning may lead to poor transcription of very specific village names or department acronyms.
- **Fallback:** If ASR struggles, rely heavily on fuzzy matching in the retrieval pipeline to correct transcription errors implicitly.
