# Evaluation Dataset Specification

## 1. Decision: Static Evaluation Set
**Decision**: Create a hardcoded, static JSON evaluation dataset.
**Reason**: To establish a baseline for RAG retrieval and intent classification performance before and after any changes.
**Alternatives**: Dynamic testing during runtime.
**Why Rejected**: Unrepeatable and not quantifiable.
**Cost**: ₹0.
**Hardware**: N/A.
**License**: Project internal (MIT).

## 2. Evaluation Set Composition

### 2.1 50 Synthetic User Profiles
Profiles to test eligibility logic:
```json
{
  "id": "U001",
  "age": 35,
  "gender": "Female",
  "district": "Chennai",
  "occupation": "Unemployed",
  "income": 90000,
  "marital_status": "Widow"
}
```
*Rule: No real PII. All data is fictional.*

### 2.2 100 Test Queries
Used to evaluate intent classification and NER:
- **Tamil**: 40 queries.
- **English**: 30 queries.
- **Tanglish**: 20 queries.
- **Ambiguous/Incomplete**: 10 queries (e.g., "Tell me about money scheme" -> should prompt for clarification).

### 2.3 30 Eligibility Test Scenarios
Tests the RAG + LLM reasoning:
- **Input**: User Profile `U001` + Query "Am I eligible for Kalaignar Magalir Urimai Thogai?"
- **Expected Outcome**: `Eligible` (with reasoning mapped to income < 2.5L and female head of family).

### 2.4 20 Scheme Retrieval Test Queries
Tests the ChromaDB + embedding performance:
- **Query**: "Subsidy for buying tractor"
- **Expected Top-5**: Must include agricultural machinery subsidy schemes from TAHDCO / Agri Dept.
- **Metric**: Mean Reciprocal Rank (MRR) @ 5.
