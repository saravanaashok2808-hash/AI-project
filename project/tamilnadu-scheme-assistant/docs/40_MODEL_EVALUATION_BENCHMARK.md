# Model Evaluation and Benchmark Plan

## 1. Objective
Ensure every ML component of the Tamil Nadu Scheme Assistant meets baseline production standards through reproducible metrics.

## 2. Component Benchmarks

### 2.1 ASR (Speech-to-Text)
- **Metric:** Word Error Rate (WER) and Character Error Rate (CER).
- **Test Sets:** 
  - Mozilla Common Voice Tamil Test Split
  - Google FLEURS Tamil
- **Target:** WER < 15%.
- **Script:** Standard `jiwer` library evaluation script processing a folder of audio files against ground truth transcripts.

### 2.2 NLU: Intent Classification
- **Metric:** F1-Score, Precision, Recall, Accuracy.
- **Test Set:** 20% holdout split from the custom 500-example intent dataset.
- **Target:** F1 > 0.85 across all 17 classes.
- **Script:** `scikit-learn` classification report generated post-training.

### 2.3 NLU: Named Entity Recognition
- **Metric:** Entity-level F1-Score.
- **Test Set:** Annotated examples from user queries (Locations, Dates, Scheme Names).
- **Target:** F1 > 0.80.

### 2.4 Retrieval (RAG / Embeddings)
- **Metric:** Recall@5, Recall@10, Mean Reciprocal Rank (MRR).
- **Test Set:** 50 curated queries mapping to specific schemes.
- **Target:** Recall@5 > 0.90 (The correct scheme must be in the top 5 results 90% of the time).
- **Script:** Automated querying of ChromaDB comparing retrieved document IDs against ground truth.

### 2.5 Eligibility Engine (Logic)
- **Metric:** Precision and Recall on Test Scenarios.
- **Test Set:** 20 synthetic user profiles (Age, Income, Caste) mapped to expected scheme eligibility.
- **Target:** 100% Accuracy (Deterministic rule engine).

### 2.6 LLM Generation
- **Metric:** Factuality, Hallucination Rate, Citation Correctness.
- **Test Set:** 50 QA pairs.
- **Evaluation Method:** LLM-as-a-judge (using a larger model like GPT-4o-mini or Claude 3.5 Sonnet to score the 4B model's outputs), plus manual spot checks.
- **Target:** 0% numerical hallucination.

### 2.7 TTS (Text-to-Speech)
- **Metric:** Human Intelligibility Evaluation / Mean Opinion Score (MOS).
- **Evaluation Method:** Blind A/B testing of synthesized audio samples by native Tamil speakers rating naturalness and clarity on a scale of 1-5.
- **Target:** MOS > 3.5.

## 3. Reproducibility
All evaluation scripts will be stored in `scripts/eval/` and can be executed via a unified `make benchmark` command, outputting results to a central `benchmarks.json` file.
