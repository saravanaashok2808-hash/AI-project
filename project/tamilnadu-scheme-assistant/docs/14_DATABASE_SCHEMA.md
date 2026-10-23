# 14 Database Schema

## Design Decisions
- **Database**: SQLite
- **Vector DB**: ChromaDB (local)
- **Search**: FTS5 for SQLite
- **Costs**: ₹0

## SQLite Schema

### `schemes` Table
(See `11_KNOWLEDGE_BASE_SCHEMA.md` for full definition)

### `sessions` Table
Stores conversation contexts for the RAG pipeline.

```sql
CREATE TABLE sessions (
    session_id TEXT PRIMARY KEY,
    user_id TEXT,
    start_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_active TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    context_data JSON -- Current identified state (e.g., {"age": 25, "gender": "Female"})
);
```

### `user_profiles` Table (Temporary)
Caches identified user traits across sessions.

```sql
CREATE TABLE user_profiles (
    user_id TEXT PRIMARY KEY,
    demographics JSON,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### FTS5 Virtual Table
For fast keyword search (fallback/augmentation to Vector search).

```sql
CREATE VIRTUAL TABLE schemes_fts USING fts5(
    scheme_id UNINDEXED,
    scheme_name_tamil,
    scheme_name_english,
    description_tamil,
    description_english,
    category
);
```

## ChromaDB Design

### Collections
- **Collection Name**: `tn_schemes`
- **Embedding Model**: `intfloat/multilingual-e5-small`

### Metadata Structure
When inserting a document into ChromaDB, the following metadata is attached:
```json
{
  "scheme_id": "TN-KMUT-001",
  "category": "Women Empowerment",
  "language": "tamil"
}
```

## Migration & Backup
- SQLite: Weekly file copy (`sqlite3 database.db ".backup database_backup.db"`).
- ChromaDB: Backup the persist directory.

## Query Examples
```sql
-- Keyword Search Example
SELECT scheme_id FROM schemes_fts WHERE schemes_fts MATCH 'women empowerment' ORDER BY rank;

-- Profile update example
UPDATE sessions SET context_data = '{"age": 30}' WHERE session_id = 'sess_123';
```
