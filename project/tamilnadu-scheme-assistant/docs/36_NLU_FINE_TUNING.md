# NLU Fine-Tuning Plan

## 1. Objective
Train a lightweight intent classifier to map user inputs (Tamil, English, Tanglish) to system actions.

## 2. Decision
**FINE-TUNE `ai4bharat/IndicBERT`** on a custom intent dataset.

## 3. Dataset Configuration
- **Size:** ~500 annotated examples.
- **Categories:** 17 distinct intents (e.g., `GREETING`, `APPLY_SCHEME`, `CHECK_STATUS`, `ELIGIBILITY_CHECK`, `DOCUMENT_QUERY`, `ESCALATE_COMPLAINT`).
- **Format:** 
  ```csv
  text,intent
  "How to apply for farm loan?",APPLY_SCHEME
  "விவசாய கடனுக்கு எப்படி விண்ணப்பிப்பது?",APPLY_SCHEME
  "loan apply panradhu eppadi",APPLY_SCHEME
  ```

## 4. Training Strategy
- **Method:** Full fine-tuning (Sequence Classification Head).
- **Reason:** IndicBERT is small enough (~130M parameters) that full fine-tuning is extremely fast even on a CPU (or a free T4 GPU in Google Colab), taking only minutes. LoRA/PEFT is unnecessary overhead.
- **Hyperparameters:**
  - Learning Rate: `2e-5`
  - Epochs: `10`
  - Batch Size: `16`
- **Evaluation Split:** 80% train / 20% validation.
- **Target Metric:** F1-score > 0.85 on validation set.

## 5. Alternatives
- **Alternative:** LLM Zero-shot classification (prompting Qwen3-4B).
- **Why rejected:** Adds 1-2 seconds of latency to every single interaction. A dedicated BERT model runs in <50ms on CPU.

## 6. Risks and Fallback
- **Risks:** The model might overfit to the 500 examples and fail on unseen phrasing.
- **Fallback:** If classification confidence is below 0.60, default to a fallback intent (`GENERAL_INQUIRY`) which passes the query to the RAG pipeline.

## 7. NER Strategy
- **Decision:** DO NOT FINE-TUNE NER.
- **Reason:** `ai4bharat/IndicNER` will be used zero-shot for standard entities.
