# 13 Data Ingestion

## Pipeline Overview
The pipeline converts unstructured government texts/PDFs into structured SQLite data and ChromaDB embeddings.

## Technical Decisions
- **PDF Extraction**: `pdfminer.six` for native text, `Surya OCR` (local) for scanned documents. Fallback: `EasyOCR`.
- **Reason**: Free, runs locally, no external API calls.
- **Cost**: ₹0.

## Process Flow

1. **Manual Collection (MVP)**
   - Initial 20-30 schemes collected manually into structured JSON format to bootstrap.

2. **Automated Extraction**
   - Download PDF/HTML.
   - For HTML: Use `BeautifulSoup` to extract main content.
   - For PDF: Check if native. If yes, `pdfminer.six`. If scanned, `Surya OCR`.

3. **Text Cleaning (Tamil & English)**
   - Remove artifacts, fix whitespace.
   - Unicode normalization.
   - Discard boilerplate header/footer.

4. **Structured Extraction**
   - Pass cleaned text to local LLM (`Qwen3-4B-Instruct`) with a strict prompt to output JSON matching the Knowledge Base Schema.

5. **Deduplication**
   - Check against SQLite using `content_hash` (SHA-256 of extracted text). If hash exists, skip.

6. **Quality Checks & Human Verification**
   - Initial state is "Draft".
   - Schema validation using Pydantic.
   - Human reviews Draft -> Active.

7. **Vector Embedding Generation**
   - Combine Name + Category + Description + Eligibility into a text chunk.
   - Model: `intfloat/multilingual-e5-small`.
   - Index into ChromaDB local persistent instance.

8. **Data Freshness**
   - Weekly cron job checks source URLs for `Last-Modified` headers or hash changes.
