# Dataset License and Ethics

## 1. Decision: Dataset Usage and Verification
**Decision**: Use explicitly verified open-source and open-government datasets.
**Reason**: To ensure compliance with copyright laws and ethical standards for building government-related software.
**Alternatives**: Web scraping private forums.
**Why Rejected**: Legal ambiguity and risk of PII violation.
**Cost**: ₹0.
**Hardware**: N/A.
**License**: Varied (see table).
**Risks**: License changes or withdrawal by dataset owners.
**Fallback**: Synthesize replacement datasets internally.

## 2. License Verification

| Dataset | Source | License | Commercial Use | Training | Redistribution | Ethical Concerns |
| --- | --- | --- | --- | --- | --- | --- |
| Mozilla Common Voice Tamil | Mozilla | CC0 (Public Domain) | Yes | Yes | Yes | None |
| OpenSLR SLR127 | OpenSLR | CC BY 2.0 | Yes | Yes | Yes | None |
| Kathbath | AI4Bharat | CC0 | Yes | Yes | Yes | None |
| FLEURS | Google | CC-BY-4.0 | Yes | Yes | Yes | None |
| Naamapadam | AI4Bharat | CC BY-NC 4.0 | No (Research Only) | Yes | No | Cannot be used directly in commercialised product; fine for hackathon MVP. |
| gov_myscheme | shrijayan (HF) | Open Government Data | Yes | Yes | Yes | May contain outdated scheme details. |
| colloquial_tamil | HF | MIT (Assumed) | Yes | Yes | Yes | Slang bias. |
| MIRACL | University of Waterloo | Apache 2.0 | Yes | Yes | Yes | None |

## 3. Ethical Considerations

### 3.1 Personal Identifiable Information (PII)
- **Policy**: No real PII is permitted in any synthetic data or training sets.
- **Implementation**: We strictly use generic names (e.g., "Kannan", "Lakshmi") and standard test numbers. Synthetic generation prompts explicitly forbid realistic phone numbers or Aadhar numbers.

### 3.2 Tamil Linguistic Respect
- **Policy**: Maintain respectful and grammatically correct Tamil, avoiding derogatory slang while supporting colloquial (Tanglish) queries for accessibility.
- **Implementation**: The LLM prompt and prompt templates for synthetic generation enforce standard formal Tamil for system responses.

### 3.3 Bias Awareness
- **Policy**: Avoid demographic bias in scheme eligibility simulation.
- **Implementation**: Evaluation dataset includes 50 diverse synthetic user profiles covering varying districts, genders, castes (where relevant to schemes), and income levels to ensure fair retrieval performance.
