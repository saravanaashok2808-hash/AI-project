# Model Training Pipeline

## 1. Decision: Model Fine-Tuning Strategy
**Decision**: Fine-tune ONLY the IndicBERT intent classifier. No LLM or ASR fine-tuning for MVP.
**Reason**: LLM fine-tuning is too hardware-intensive for student laptops. Intent classification requires high accuracy on Tanglish/Tamil queries which zero-shot LLM might struggle with quickly.
**Alternatives**: Zero-shot prompting Qwen3-4B-Instruct for intent.
**Why Rejected**: Slower inference time compared to a small, fast encoder model.
**Cost**: ₹0.
**Hardware**: CPU-only training is feasible for IndicBERT (albert-base size), takes < 2 hours on modern CPU.
**License**: MIT (training code), Model (MIT).
**Risks**: Overfitting on small dataset.
**Fallback**: Fallback to LLM zero-shot classification if IndicBERT fails.

## 2. Training Pipeline

### 2.1 Data Preparation Script (`prepare_intent_data.py`)
- Reads synthetic intent JSON lines.
- Tokenizes using `AutoTokenizer.from_pretrained("ai4bharat/indic-bert")`.
- Maps 17 intents to integer IDs.
- Splits into 80% train, 20% validation.

### 2.2 Training Script (`train_intent.py`)
```python
# Pseudo-code implementation using PyTorch + Transformers
from transformers import AutoModelForSequenceClassification, Trainer, TrainingArguments

model = AutoModelForSequenceClassification.from_pretrained(
    "ai4bharat/indic-bert", num_labels=17
)

training_args = TrainingArguments(
    output_dir="./models/intent_classifier_v1",
    num_train_epochs=3,
    per_device_train_batch_size=16,
    evaluation_strategy="epoch",
    use_cpu=True # Hardware constraint
)

trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=train_dataset,
    eval_dataset=val_dataset,
)

trainer.train()
```

### 2.3 Evaluation Script (`eval_intent.py`)
- Calculates Accuracy, Precision, Recall, F1-Score.
- Generates confusion matrix for the 17 intents to identify overlaps (e.g., confusing "Scheme Search" with "Eligibility Check").

### 2.4 Model Export & Versioning
- Exports model to `ONNX` format for faster CPU inference in production.
- Model weights saved to `models/intent-classifier/v1.0.0/`.
