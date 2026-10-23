# 10 Eligibility Engine

This document outlines the deterministic eligibility engine designed to prevent AI hallucinations regarding scheme qualifications.

## 1. Rule Schema (JSON)
All schemes have eligibility criteria codified in a strict JSON format.

```json
{
  "scheme_id": "tn_kmut_01",
  "scheme_name": "Kalaignar Magalir Urimai Thogai",
  "rules": {
    "operator": "AND",
    "conditions": [
      { "field": "gender", "operator": "EQUALS", "value": "female" },
      { "field": "age", "operator": "GTE", "value": 21 },
      { "field": "family_income", "operator": "LTE", "value": 250000 },
      { "field": "land_wet", "operator": "LTE", "value": 5, "unit": "acres" }
    ]
  }
}
```

## 2. Rule Types
- **Demographic:** Age, Gender, Social Category (Community), Marital Status.
- **Economic:** Annual Income, Land Ownership, Ration Card Type (PHH, AAY).
- **Geographic:** District, Residency Status (Resident of TN).
- **Educational/Occupational:** Highest Education, Occupation (e.g., Farmer, Weaver).

## 3. Rule Evaluation Logic
- Standard Boolean evaluation: `AND`, `OR`, `NOT`.
- Engine compares user profile data (gathered via chat) against the JSON schema.

## 4. Result Categories
- `ELIGIBLE`: All required criteria are definitively met.
- `POTENTIALLY_ELIGIBLE`: Some criteria met, but some non-blocking criteria are unknown.
- `NOT_APPEARING_ELIGIBLE`: At least one hard blocking criterion failed (e.g., male applying for a female-only scheme).
- `INSUFFICIENT_INFORMATION`: Key criteria (like income or age) are entirely missing.

## 5. Missing Information Detection & Progressive Profiling
- If result is `INSUFFICIENT_INFORMATION` or `POTENTIALLY_ELIGIBLE`, the engine identifies the missing fields.
- The LLM is prompted to ask the user *only* for the missing fields (e.g., "To confirm your eligibility, could you please tell me your annual family income?").

## 6. Tracking Criteria
- The backend maintains session state mapping:
  - `matched`: [Gender, Age]
  - `failed`: []
  - `unknown`: [Income, Land Ownership]

## 7. Example Rules for TN Schemes
1. **Kalaignar Magalir Urimai Thogai:** Female, Age >= 21, Income <= 2.5L.
2. **Moovalur Ramamirtham Ammaiyar Higher Education Assurance (Pudhumai Penn):** Female, Studied 6th to 12th in Government School, Pursuing Higher Ed.
3. **Dr. Muthulakshmi Reddy Maternity Benefit:** Pregnant Women, Age >= 19, Max 2 deliveries.
4. **Chief Minister's Comprehensive Health Insurance:** TN Resident, Family Income < 1.2L.
5. **Uzhavar Pathukappu Thittam:** Farmer/Tenant, Age 18-65.

## 8. Integration with RAG Evidence
- The deterministic engine evaluates JSON rules.
- RAG fetches unstructured qualitative data (e.g., exact procedures, required documents).
- Both outputs are injected into the LLM prompt.

## 9. LLM Explanation Generation
- The LLM translates the raw JSON evaluation into natural language (Tamil/English).
- **Prompt Instruction:** "Based on the rule engine, the user meets X and Y but missing Z. Ask for Z nicely."

## 10. Principle: Never Overclaim Eligibility
- **Core Rule:** The AI must NEVER guarantee eligibility or funds.
- It must always use phrasing like "Based on the details provided, you *appear to qualify*" and add a disclaimer: "Final approval is subject to official verification by the respective department."
