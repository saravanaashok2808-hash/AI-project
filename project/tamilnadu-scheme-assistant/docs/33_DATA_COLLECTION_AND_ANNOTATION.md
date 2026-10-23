# Data Collection and Annotation

## 1. Overview
For the MVP, data collection is focused on establishing a high-quality, ground-truth database of Tamil Nadu government schemes for the RAG pipeline.

## 2. Target Sources
- `tn.gov.in` (Main portal)
- `tnesevai.tn.gov.in` (E-Sevai services)
- `kmut.tn.gov.in` (Kalaignar Magalir Urimai Thogai)
- `cmchistn.com` (Chief Minister's Comprehensive Health Insurance Scheme)
- `myscheme.gov.in` (Filtered for Tamil Nadu)

## 3. Manual Process for MVP
Given the short timeframe of the hackathon and the requirement for absolute accuracy, automated scraping will be limited. A manual/semi-manual collection pipeline is adopted.

### Step 1: Document Acquisition
- Download PDF guidelines, G.O.s (Government Orders), and FAQ pages.
- Use `pdfminer.six` for native PDFs and `Surya OCR` for scanned documents.

### Step 2: Chunking and Structuring
- Convert raw text into structured Markdown formats.
- **Fields required per scheme:**
  - Scheme Name (Tamil & English)
  - Department
  - Objective
  - Target Audience
  - Eligibility Criteria (Age, Income, Caste, Gender, Location)
  - Benefits / Allowances
  - Required Documents
  - Application Process (Online/Offline URL)
  - Deadlines (if any)

### Step 3: Annotation and Metadata
- Store the structured markdown in a local directory `data/schemes/`.
- Maintain a `metadata.json` or SQLite table mapping the scheme file to its specific metadata tags (e.g., `category: agriculture`, `income_limit: 200000`).
- This structured metadata fuels the SQLite FTS5 index and ChromaDB metadata filters.

### Step 4: Intent Data Annotation
- Manually create ~500 query variations mapping to 17 distinct intents.
- **Example Intent Annotation:**
  - `"How do I apply for farmer subsidy?"` -> `intent: APPLY_SCHEME`
  - `"Kalaignar urimai thogai status check"` -> `intent: CHECK_STATUS`
  - `"எப்படி விண்ணப்பிப்பது?"` -> `intent: APPLY_SCHEME`
- Saved in CSV format for IndicBERT fine-tuning.

## 4. Hardware and Cost
- **Decision:** Local manual curation + Open Source OCR.
- **Cost:** ₹0.
- **Hardware:** Local laptop (8GB RAM).

## 5. Risks & Fallbacks
- **Risks:** Data becomes outdated; OCR errors in Tamil text.
- **Fallback:** Maintain hardcoded fallback text for the top 5 most critical schemes.
