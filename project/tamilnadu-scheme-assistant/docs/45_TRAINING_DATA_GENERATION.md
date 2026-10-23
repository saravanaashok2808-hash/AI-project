# Training Data Generation

## 1. Decision: Synthetic Data for NLP Tasks
**Decision**: Use LLMs (offline or free API) to generate synthetic training data for intents and NER.
**Reason**: No readymade dataset exists for Tamil Nadu government scheme intents in Tanglish/Tamil.
**Alternatives**: Manual annotation.
**Why Rejected**: Too slow for a hackathon timeframe.
**Cost**: ₹0.
**Hardware**: Laptop for generation scripts.
**License**: Generated data belongs to the project (MIT).
**Risks**: LLM bias in generated queries.
**Fallback**: Manually write 100 examples instead of 500.

## 2. Generation Specifications

### 2.1 Intent Classification Examples (500+)
- **Target**: 17 Intents (e.g., `Find_Scheme`, `Check_Eligibility`, `Track_Status`, `Required_Documents`).
- **Distribution**: 40% Tamil, 30% Tanglish, 30% English.
- **Template Example**:
  - Tamil: "எனக்கு உழவர் அட்டை வாங்க என்ன தகுதி வேண்டும்?" (`Check_Eligibility`)
  - Tanglish: "Uzhavar attai vanga enna documents venum?" (`Required_Documents`)
  - English: "How to apply for farmer certificate?" (`Find_Scheme`)

### 2.2 Entity Extraction Examples (200+)
- **Target Entities**: `Age`, `District`, `Occupation`, `Income`, `Gender`, `Caste`.
- **Template Example**:
  - "I am a **25 year old** [Age] **farmer** [Occupation] from **Madurai** [District]."

### 2.3 Government Scheme QA Pairs (100+)
- Extracted manually or via script from:
  - tn.gov.in
  - kmut.tn.gov.in
- Used for RAG retrieval testing, not model training.

### 2.4 Tanglish Variation Generation Rules
- Substitute Tamil script with phonetic English (e.g., 'விவசாயி' -> 'vivasayi').
- Mix English nouns with Tamil verbs (e.g., 'Application status eppadi check pandrathu?').

### 2.5 Quality Validation Checklist
- [ ] No real user PII used.
- [ ] Balanced distribution across all 17 intents.
- [ ] Tanglish phonetics represent realistic typing habits.
- [ ] Labels strictly map to the defined intent taxonomy.
