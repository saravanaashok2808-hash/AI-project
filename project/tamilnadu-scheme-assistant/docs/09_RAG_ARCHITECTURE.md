# 09 RAG Architecture

This document details the Retrieval-Augmented Generation (RAG) pipeline for extracting and querying Tamil Nadu government scheme data.

## 1. Document Ingestion Pipeline
- **Sources:** TN government portals, PDFs, HTML pages.
- **Extraction:**
  - PDFs: `pdfminer.six` (text), `Surya OCR` (scanned images).
  - Web: BeautifulSoup for HTML parsing.
- **Cleaning:** Remove headers/footers, standardize whitespace.

## 2. Chunking Strategy
- **Method:** Semantic / Section-based chunking.
- **Logic:** Government schemes have distinct sections (Eligibility, Benefits, Documents Required). Chunks are split at these headers.
- **Size:** ~250-500 words per chunk with 50-word overlap to maintain context.

## 3. Embedding Generation
- **Model:** `intfloat/multilingual-e5-small`.
- **Process:** Text chunks (Tamil and English) are embedded into dense vectors.
- **Prefixing:** E5 requires prefixing (e.g., `passage: ` for indexing, `query: ` for searching).

## 4. Storage and Indexing
- **Vector DB:** ChromaDB (local persistence).
- **Relational DB:** SQLite with FTS5.
- **Process:** Vectors are stored in ChromaDB; exact text and metadata are stored in SQLite for keyword searches.

## 5. Query Understanding and Expansion
- **Translation/Alignment:** User query (Tamil/English/Tanglish) is embedded directly (multilingual models handle this).
- **Intent Extraction:** IndicBERT extracts intent (e.g., "Check Eligibility", "Find Documents").

## 6. Hybrid Retrieval
- **Vector Search:** ChromaDB returns top-K semantically similar chunks.
- **Keyword Search:** SQLite FTS5 returns exact keyword matches (vital for specific scheme names like "Kalaignar Magalir Urimai Thogai").

## 7. Result Merging and Scoring
- **Method:** Reciprocal Rank Fusion (RRF) combines vector and keyword ranks.
- **Reranker:** **NOT REQUIRED FOR MVP** (saves RAM/latency; RRF provides sufficient accuracy for <10,000 documents).

## 8. Metadata Filtering
- **Fields:** Department, Category, District, Status, Target Audience.
- **Usage:** Pre-filtering vector search if the LLM or UI explicitly identifies a category (e.g., "Schemes for Farmers").

## 9. Evidence Pack Assembly
- **Process:** Top 3-5 ranked chunks are concatenated into a prompt context window.
- **Limit:** Kept under 2000 tokens to ensure fast LLM processing on 4B models.

## 10. Citation Generation & Source Verification
- **Traceability:** Every chunk maintains its source URL and document title.
- **Output:** The LLM is instructed to append `[Source: Title]` to its claims.

## 11. Confidence Scoring
- **Heuristic:** Distance metric from ChromaDB + keyword overlap score. If confidence is low, the LLM is prompted to state "I cannot find specific information on this."
