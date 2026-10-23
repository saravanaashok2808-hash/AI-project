# Model Versioning

## 1. Decision: Versioning Strategy
**Decision**: Local folder structure with Semantic Versioning (SemVer) for locally trained models. Remote HuggingFace tags for pre-trained models.
**Reason**: Keeps the project lightweight without needing MLflow or DVC for a hackathon MVP.
**Alternatives**: MLflow, DVC, Weights & Biases.
**Why Rejected**: Overkill for a single fine-tuned model and downloaded GGUF files.
**Cost**: ₹0.
**Hardware**: Minimal local storage (~2GB for intent model + quantized LLMs).
**License**: N/A.
**Risks**: Manual error in versioning.
**Fallback**: Just use latest timestamped folder.

## 2. Naming Convention
Format: `v{MAJOR}.{MINOR}.{PATCH}`
- **MAJOR**: Architecture change (e.g., switching from IndicBERT to another base).
- **MINOR**: Retrained with new data, significant metric improvement.
- **PATCH**: Minor config tweaks (e.g., ONNX export settings).

## 3. Storage Location
Models are stored locally in the following registry structure:
```text
/models/
  /intent-classifier/
    /v1.0.0/
      config.json
      model.onnx
      tokenizer.json
    /v1.1.0/
  /llm/
    qwen3-4b-instruct-q4_k_m.gguf
  /asr/
    faster-whisper-large-v3-turbo-int8/
```

## 4. Changelog
Stored in `/models/CHANGELOG.md`.
Example:
- `v1.1.0`: Added 200 Tanglish examples to training set. F1 improved from 0.82 to 0.88.
- `v1.0.0`: Initial IndicBERT fine-tune on 500 synthetic intent queries.

## 5. Rollback Procedure
If `v1.1.0` fails in production:
1. Update `.env` or `config.yaml` to point `INTENT_MODEL_DIR` back to `models/intent-classifier/v1.0.0/`.
2. Restart FastAPI backend.
