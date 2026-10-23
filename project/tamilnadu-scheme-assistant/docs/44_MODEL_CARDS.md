# Model Cards

## 1. Decision: AI Components Registry
**Decision**: Standardize model card documentation for all used models.
**Reason**: Transparency, maintainability, and quick reference for hackathon judges.
**Alternatives**: Ad-hoc documentation.
**Why Rejected**: Hard to track model specific configurations and limits.
**Cost**: ₹0.
**Hardware**: CPU constraints defined per card.
**License**: Open-source varied.

---

## 2. ASR Model Card
- **Model Name**: faster-whisper (large-v3-turbo)
- **Intended Use**: Transcribe Tamil and English voice inputs to text.
- **Limitations**: Struggles with heavy background noise; INT8 quantization slightly reduces accuracy.
- **Ethical Considerations**: Handles voice data locally, preserving privacy.
- **Performance Metrics**: Target WER < 15% on Tamil test set.

## 3. LLM Model Card
- **Model Name**: Qwen3-4B-Instruct via Ollama
- **Intended Use**: Generating responses, RAG synthesis, and final user answers.
- **Limitations**: Context window limited to keep RAM usage low; may hallucinate scheme rules if not strictly grounded by RAG.
- **Ethical Considerations**: Prompt-engineered to avoid biased or harmful advice.
- **Performance Metrics**: ~10 tokens/sec on 8GB RAM CPU.

## 4. Intent Classifier Model Card
- **Model Name**: Custom Fine-tuned IndicBERT
- **Intended Use**: Classifying user queries into 17 predefined intents (e.g., `check_eligibility`, `find_scheme`).
- **Limitations**: Only trained on synthetic data; may fail on highly convoluted sentences.
- **Ethical Considerations**: Safe, classification only.
- **Performance Metrics**: Target F1-score > 0.85 on evaluation set.

## 5. NER Model Card
- **Model Name**: AI4Bharat IndicNER
- **Intended Use**: Extracting entities (Age, Location, Income) from queries.
- **Limitations**: Pre-trained on general text, might miss highly specific TN government terminology.
- **Ethical Considerations**: Does not store extracted entities permanently.
- **Performance Metrics**: Pre-trained metrics apply (F1 ~0.80 on Indic datasets).

## 6. Embedding Model Card
- **Model Name**: intfloat/multilingual-e5-small
- **Intended Use**: Vectorizing scheme documents and user queries for semantic search.
- **Limitations**: 512 token limit per chunk.
- **Ethical Considerations**: Neutral embeddings.
- **Performance Metrics**: High MRR on multilingual retrieval benchmarks.

## 7. TTS Model Card
- **Model Name**: ai4bharat/indic-parler-tts (Primary)
- **Intended Use**: Synthesize Tamil audio from LLM text responses.
- **Limitations**: Generation can be slow on CPU.
- **Ethical Considerations**: Voice synthesis is clear and robotic enough to not impersonate humans.
- **Performance Metrics**: Target RTF (Real-Time Factor) < 2.0 on CPU.
