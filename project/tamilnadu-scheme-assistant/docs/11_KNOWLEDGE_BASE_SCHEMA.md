# 11 Knowledge Base Schema

## Overview
This document defines the complete schema for the Tamil Nadu Government Scheme Assistant knowledge base.

## Decision Record
- **Database**: SQLite with FTS5 for structured data and keyword search.
- **Reason**: Zero-cost, lightweight, built-in to Python, sufficient for MVP (target hardware: 8-16GB RAM laptop).
- **Alternatives**: PostgreSQL (rejected: overkill, requires extra setup), MongoDB (rejected: no native FTS out-of-the-box in free tier without Atlas).
- **Cost**: ₹0

## Scheme Schema Definition

The primary `schemes` table contains the following fields:

| Field | Type | Description |
|-------|------|-------------|
| `scheme_id` | TEXT | Primary key, unique identifier (e.g., `TN-WCD-001`) |
| `scheme_name_tamil` | TEXT | Name of the scheme in Tamil |
| `scheme_name_english` | TEXT | Name of the scheme in English |
| `department` | TEXT | Responsible department (e.g., "Social Welfare") |
| `category` | TEXT | Broad category (e.g., "Women Empowerment") |
| `sub_category` | TEXT | Specific sub-category (e.g., "Financial Assistance") |
| `description_tamil` | TEXT | Detailed description in Tamil |
| `description_english` | TEXT | Detailed description in English |
| `benefits` | JSON | Structured benefits JSON |
| `eligibility_rules` | JSON | Structured eligibility criteria JSON |
| `required_documents` | JSON | Array of required documents |
| `application_method` | TEXT | "Online", "Offline", "Both" |
| `application_steps` | JSON | Step-by-step application instructions |
| `official_urls` | JSON | Array of official reference URLs |
| `contact_helpline` | TEXT | Contact numbers or emails |
| `dates` | JSON | Start date, deadline, etc. |
| `source_metadata` | JSON | Scraping source, date, reliability score |
| `content_hash` | TEXT | SHA-256 hash of core content for change detection |
| `version` | INTEGER | Version number |
| `status` | TEXT | "Active", "Closed", "Draft" |

### SQLite Table Definition

```sql
CREATE TABLE schemes (
    scheme_id TEXT PRIMARY KEY,
    scheme_name_tamil TEXT NOT NULL,
    scheme_name_english TEXT NOT NULL,
    department TEXT NOT NULL,
    category TEXT NOT NULL,
    sub_category TEXT,
    description_tamil TEXT,
    description_english TEXT,
    benefits JSON,
    eligibility_rules JSON,
    required_documents JSON,
    application_method TEXT,
    application_steps JSON,
    official_urls JSON,
    contact_helpline TEXT,
    dates JSON,
    source_metadata JSON,
    content_hash TEXT,
    version INTEGER DEFAULT 1,
    status TEXT DEFAULT 'Active',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### JSON Schema: `eligibility_rules`

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "type": "object",
  "properties": {
    "age": {
      "type": "object",
      "properties": {
        "min": { "type": "integer" },
        "max": { "type": "integer" }
      }
    },
    "gender": {
      "type": "array",
      "items": { "type": "string", "enum": ["Male", "Female", "Transgender", "Any"] }
    },
    "income_limit_annual": { "type": "number" },
    "residence": { "type": "string", "enum": ["Tamil Nadu", "Any"] },
    "community": { "type": "array", "items": { "type": "string" } },
    "special_conditions": { "type": "array", "items": { "type": "string" } }
  }
}
```

### JSON Schema: `benefits`

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "type": "object",
  "properties": {
    "type": { "type": "string", "enum": ["Financial", "Material", "Service", "Mixed"] },
    "amount": { "type": "number" },
    "frequency": { "type": "string", "enum": ["One-time", "Monthly", "Annual"] },
    "details": { "type": "string" }
  }
}
```

## Example Records

### 1. Kalaignar Magalir Urimai Thogai
```json
{
  "scheme_id": "TN-KMUT-001",
  "scheme_name_english": "Kalaignar Magalir Urimai Thogai",
  "scheme_name_tamil": "கலைஞர் மகளிர் உரிமைத் தொகை",
  "department": "Special Programme Implementation",
  "category": "Women Empowerment",
  "benefits": {
    "type": "Financial",
    "amount": 1000,
    "frequency": "Monthly",
    "details": "Monthly financial assistance of ₹1000 to women heads of family."
  },
  "eligibility_rules": {
    "age": { "min": 21 },
    "gender": ["Female"],
    "income_limit_annual": 250000,
    "residence": "Tamil Nadu"
  }
}
```

### 2. Chief Minister's Comprehensive Health Insurance Scheme (CMCHIS)
```json
{
  "scheme_id": "TN-CMCHIS-001",
  "scheme_name_english": "CMCHIS",
  "scheme_name_tamil": "முதலமைச்சரின் விரிவான மருத்துவக் காப்பீட்டுத் திட்டம்",
  "department": "Health and Family Welfare",
  "category": "Health",
  "benefits": {
    "type": "Service",
    "amount": 500000,
    "frequency": "Annual",
    "details": "Health insurance cover of ₹5,00,000 per family per year."
  },
  "eligibility_rules": {
    "income_limit_annual": 120000,
    "residence": "Tamil Nadu"
  }
}
```

### 3. Indira Gandhi National Old Age Pension Scheme (IGNOAPS) - TN Component
```json
{
  "scheme_id": "TN-OAP-001",
  "scheme_name_english": "Old Age Pension",
  "scheme_name_tamil": "முதியோர் ஓய்வூதியத் திட்டம்",
  "department": "Revenue and Disaster Management",
  "category": "Social Security",
  "benefits": {
    "type": "Financial",
    "amount": 1000,
    "frequency": "Monthly",
    "details": "Monthly pension of ₹1000 for destitute elderly."
  },
  "eligibility_rules": {
    "age": { "min": 60 },
    "residence": "Tamil Nadu",
    "special_conditions": ["Must be destitute"]
  }
}
```

## Validation Rules
- Required fields: `scheme_id`, `scheme_name_tamil`, `scheme_name_english`, `department`, `category`.
- Status must be one of: "Active", "Closed", "Draft".
- `content_hash` must be re-calculated and verified on every update.

## Version Tracking
Updates to a scheme increment the `version` field. Historical records are either archived or replaced, but the `content_hash` changes to trigger re-embedding in Vector DB.
