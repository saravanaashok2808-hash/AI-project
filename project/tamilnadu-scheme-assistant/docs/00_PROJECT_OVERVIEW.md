# 00 — Project Overview

## Tamil Nadu Multilingual Voice-Based Government Scheme Assistant

### Project Title
**Multilingual Voice-Based Government Scheme Assistant**

### Version
1.0.0-MVP

### Status
Active Development — Phase 0 (Research Complete)

---

## Executive Summary

This project builds a **web-based AI assistant** that helps people in Tamil Nadu discover and understand government welfare schemes through **Tamil voice, English voice, Tanglish, and text input**. The system uses a verified government knowledge base, structured eligibility rules, Retrieval-Augmented Generation (RAG), and open-source AI models — all at **₹0 core cost**.

The assistant is NOT a generic chatbot. It is a **grounded, explainable information system** where:
- Government sources are the **source of truth**
- Structured rules determine **eligibility**
- RAG provides **evidence**
- The LLM explains **verified evidence** to the user

---

## Scope

| Attribute | Value |
|-----------|-------|
| **Geography** | Tamil Nadu, India (with applicable Central Government schemes) |
| **Languages** | Tamil, English, Tanglish (Tamil-English code-switching) |
| **Input** | Voice (Tamil/English/Tanglish) + Text |
| **Output** | Text + Tamil/English voice |
| **Schemes** | TN State schemes, TN department schemes, applicable Central schemes |
| **Cost** | ₹0 core cost — all open-source, local inference |
| **Deployment** | Student laptop (8-16GB RAM, no GPU required) |

---

## What This System Does

1. **Understands** user queries in Tamil, English, or Tanglish (voice or text)
2. **Detects** language and normalizes the query
3. **Extracts** relevant user information (age, district, occupation, etc.)
4. **Searches** a verified government scheme knowledge base using hybrid retrieval
5. **Evaluates** potential eligibility using structured deterministic rules
6. **Explains** why a scheme may or may not be relevant
7. **Identifies** missing information needed for eligibility assessment
8. **Shows** benefits, required documents, and application process
9. **Provides** official application/source links with verification dates
10. **Responds** naturally in Tamil or English with optional voice output
11. **Never** invents scheme facts, eligibility criteria, or government links

---

## What This System Does NOT Do

- ❌ Does NOT approve or reject applications
- ❌ Does NOT claim to be a government authority
- ❌ Does NOT invent schemes, benefits, documents, or links
- ❌ Does NOT permanently store personal data (session-only)
- ❌ Does NOT require paid APIs, services, or GPU
- ❌ Does NOT depend on internet for core functionality (after initial model download)

---

## Architecture Overview

```
                    USER
                      |
          +-----------+-----------+
          |                       |
       VOICE                    TEXT
          |                       |
     ASR (Whisper)                |
          |                       |
          +-----------+-----------+
                      |
              Language Detection (lingua)
                      |
          Tamil / English / Tanglish
                      |
          Query Normalization
                      |
        Intent Detection (IndicBERT)
           +
        Entity Extraction (IndicNER)
                      |
          User Profile Manager
                      |
          +-----------+-----------+
          |                       |
   Eligibility Facts        Scheme Search
          |                       |
          |              Hybrid Retrieval
          |              (E5 + ChromaDB)
          |                       |
          +-----------> Evidence Pack
                              |
                   Eligibility Engine
                     (Deterministic Rules)
                              |
                   LLM Explanation
                   (Qwen3-4B via Ollama)
                              |
                  Source/Citation Check
                              |
                   Response Generator
                     /            \
                  TEXT            TTS
                  (Web)    (MMS-TTS/Parler)
                     \            /
                          USER
```

---

## Key Design Principles

1. **Government Sources = Truth** — The LLM never becomes the database
2. **Structured Rules = Eligibility** — Deterministic engine, not LLM guessing
3. **RAG = Evidence** — Every claim backed by retrieved documents
4. **LLM = Explanation Layer** — Explains verified evidence naturally
5. **Tamil First** — Tamil is a first-class language, not translated English
6. **Voice First** — Designed for voice interaction with text fallback
7. **₹0 Core Cost** — Fully functional without any payment
8. **Student Laptop** — Runs on 8-16GB RAM without GPU
9. **Privacy by Default** — No permanent storage of personal data
10. **Explainable** — Every recommendation has a traceable reason

---

## Target Users

- Tamil-speaking citizens seeking government scheme information
- Rural users unfamiliar with government portals
- Elderly users who prefer voice interaction
- Youth seeking education/employment schemes
- Women seeking welfare schemes
- Farmers, fishermen, workers seeking occupational schemes
- Users comfortable with Tanglish (Tamil-English mix)
- Anyone in Tamil Nadu needing scheme guidance

---

## Innovation

| Feature | Differentiation |
|---------|----------------|
| Tamil-first voice interface | Most assistants are English-first |
| Tanglish understanding | Rare in government tools |
| Government-source-grounded RAG | Not generic LLM answers |
| Structured eligibility reasoning | Deterministic, not probabilistic |
| Explainable eligibility | Shows matched/failed/missing criteria |
| Missing-information detection | Asks only necessary follow-ups |
| Official-link verification | Domain allowlist, not blind URLs |
| Source freshness tracking | Last verified date on every scheme |
| ₹0 core cost | Truly free, not freemium |
