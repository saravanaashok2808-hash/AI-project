# Evaluation Framework

## 1. Metrics & Targets
* **ASR:** Word Error Rate (WER), Character Error Rate (CER) evaluated on Mozilla Common Voice Tamil test split. Target: WER < 15%.
* **NLU (Intent & Entity):** Precision, Recall, F1 on custom annotated government queries.
* **Retrieval (RAG):** Recall@5, Recall@10, MRR, Precision@K on scheme matching queries.
* **Eligibility Rule Engine:** Precision/Recall for False Positives (showing ineligible scheme) and False Negatives.
* **LLM Generation:** Factuality/Groundedness (no hallucinated benefits), Citation correctness, structured output validity.
* **TTS:** Human evaluation for intelligibility and natural Tamil pronunciation.

## 2. End-to-End Evaluation
* Success rate of full user journeys (from voice query -> profile extraction -> scheme recommendation).
* Evaluated across Tamil, English, and Tanglish.

## 3. Dataset Creation Methodology
* Scrape 50+ real TN government scheme documents.
* Synthetically generate 500 query-profile-scheme triplets using a larger LLM for the golden dataset.
* Manual annotation for edge cases.

## 4. Benchmarking Scripts
* Python scripts in `/eval` directory to automate metrics collection using custom automated testing scripts.
