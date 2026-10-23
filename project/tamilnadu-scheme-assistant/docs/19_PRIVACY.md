# Privacy Architecture

## 1. Data Minimization Principle
* Collect only data essential for scheme eligibility (Age, Gender, Community, Income, Location).
* **What is NOT collected:** Names, Aadhaar numbers, Bank Account details, precise addresses.

## 2. Ephemeral Storage
* **Session-Only Profile Data:** Extracted details exist only for the duration of the conversation.
* **No Raw Voice Storage:** Audio is processed by `faster-whisper` and immediately deleted from RAM/Disk.
* **Session Deletion:** Automatic expiration after 30 minutes of inactivity. Manual "Clear Session" button in UI.

## 3. Consent Mechanism
* Explicit "Accept & Continue" on the Landing Page acknowledging the temporary processing of voice and demographics. Privacy notice content is prominent.

## 4. Data Flow (PII Handling)
```mermaid
flowchart LR
    User[User Audio/Text] --> Frontend
    Frontend -->|HTTPS| Backend
    Backend --> ASR[ASR Model (Local)]
    ASR -.->|Deletes Audio| Trash
    Backend --> NLU[NLU/LLM (Local)]
    NLU --> Profile[Session DB]
    Profile -.->|Auto-Delete on Expiry| Trash
```

## 5. Compliance
* Aligns with Indian DPDP Act principles and GDPR data minimization requirements by treating infrastructure as stateless regarding PII.
