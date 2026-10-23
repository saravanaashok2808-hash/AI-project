# Data Quality Assurance Pipeline

## 1. Decision: Automated and Manual Quality Checks
**Decision**: Implement a mixed pipeline for data validation.
**Reason**: RAG systems heavily depend on the accuracy of the underlying scheme documents. Government schemes have strict eligibility rules that cannot be hallucinated.
**Alternatives**: Fully manual review.
**Why Rejected**: Too slow for continuous updates.
**Cost**: ₹0.
**Hardware**: N/A.
**License**: N/A.

## 2. Pipeline Components

### 2.1 Tamil Linguistic Correctness Checks
- Run spell checks and basic grammar checks on parsed OCR output using open-source tools to ensure Surya OCR/EasyOCR didn't produce garbage text.
- Fallback to English documents if Tamil OCR confidence is < 70%.

### 2.2 Scheme Factual Accuracy Verification
- **Process**: Extracted numerical values (Age limits, Income limits, Subsidy amounts) are extracted via Regex/NER during ingestion and stored as metadata in SQLite.
- **Verification**: Ensure metadata matches the embedded text chunk.

### 2.3 Duplicate Detection
- **Process**: Hash the text content of every ingested document (SHA-256).
- **Action**: Reject ingestion if hash already exists in SQLite document registry to prevent duplicate vector embeddings in ChromaDB.

### 2.4 Source Freshness Monitoring
- **Metadata**: Store `date_issued` and `date_scraped`.
- **Threshold**: Flag documents older than 2 years for manual review to check if the scheme is still active.

### 2.5 Human Review Workflow
- Any document with OCR confidence < 80% or missing critical metadata (e.g., no department found) is placed in a `pending_review` queue in the SQLite DB.
- A simple admin API endpoint allows a human to approve or edit the text before it enters the ChromaDB vector store.

### 2.6 Quality Metrics and Thresholds
- **Vector DB Quality**: Max 1500 documents for MVP.
- **Chunk Size**: Strict adherence to 512 tokens.
- **Metadata Completeness**: 100% of schemes must have `department` and `scheme_name`.
