# Embedding and Reranking Models

## 1. Embedding Model Strategy
- **Decision:** `intfloat/multilingual-e5-small`
- **Reason:** Requires only ~470MB of memory and outputs 384-dimensional vectors. It boasts excellent Tamil performance on the Massive Text Embedding Benchmark (MTEB). It is highly optimized for CPU inference, which is critical for an 8GB RAM target.
- **Alternatives:** `BAAI/bge-m3`
- **Why rejected:** `bge-m3` is a state-of-the-art model (1024d) but is significantly heavier (~2.2GB). It is reserved as a fallback for systems with 16GB+ RAM.
- **Cost:** ₹0
- **Hardware:** CPU
- **License:** MIT

## 2. Reranking Model Strategy
- **Decision:** NOT REQUIRED FOR MVP
- **Reason:** The anticipated corpus size for the MVP is small (<500 distinct government schemes/documents). With a small corpus and structured ChromaDB metadata filtering (e.g., filtering by department or beneficiary type before vector search), the base recall of `e5-small` is more than sufficient.
- **Alternatives:** Cross-encoder rerankers (e.g., `BAAI/bge-reranker-m3`).
- **Why rejected:** Adding a cross-encoder requires a second forward pass over multiple documents, severely impacting latency on a CPU-only setup.

## 3. Vector Database Architecture
- **Decision:** `ChromaDB`
- **Reason:** Runs locally, persists to SQLite, and requires no external Docker containers or background services.
- **Configuration:** Use `l2` (Euclidean) or `cosine` distance. Embeddings will be normalized prior to insertion.

## 4. Risks and Fallback
- **Risks:** The `small` embedding model might fail to distinguish between highly overlapping queries (e.g., "widow pension scheme" vs "old age pension scheme" if phrased ambiguously).
- **Fallback:** Hybrid search. Combine Vector Search (ChromaDB) with Keyword/FTS5 Search (SQLite) and apply Reciprocal Rank Fusion (RRF) in the application layer.
