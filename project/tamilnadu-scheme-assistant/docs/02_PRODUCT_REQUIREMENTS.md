# Product Requirements Document

## 1. Functional Requirements

### 1.1 Input Processing
*   **Voice Input:** Accept voice input in Tamil, English, and Tanglish via microphone recording.
*   **Text Input:** Accept text input in Tamil, English, and Tanglish.
*   **Language Detection:** Automatically detect the user's input language and script (Tamil vs Latin).
*   **Intent Recognition:** Classify the user's intent (e.g., scheme discovery, eligibility check, general inquiry) using an IndicBERT classifier.

### 1.2 Core Capabilities
*   **Scheme Search:** Retrieve relevant government schemes using semantic search and full-text search based on user queries.
*   **Eligibility Assessment:** Compare user-provided profile data (age, gender, income, caste, occupation) against parsed scheme rules to determine eligibility.
*   **Missing Information Detection:** Identify mandatory criteria missing from the user's profile and prompt the user to provide them before finalizing eligibility.
*   **Detailed Explanations:** Provide comprehensive answers covering:
    *   Scheme benefits
    *   Required documents
    *   Application process
    *   Official department links
    *   Source citations (URLs to tn.gov.in, myscheme.gov.in, etc.)
*   **Follow-up Questions:** Support multi-turn conversational follow-ups contextually linked to the current scheme or query.

### 1.3 Output Processing
*   **Voice Output:** Provide text-to-speech (TTS) playback in Tamil (and English) for the assistant's responses.
*   **Session Management:** Maintain context of the current conversation and user profile temporarily during the active session.

## 2. Non-Functional Requirements

### 2.1 Performance
*   **Response Time (Text):** Under 10 seconds for text-based Q&A.
*   **Response Time (Voice):** Under 15 seconds for end-to-end voice interactions (Speech -> Text -> RAG -> Text -> Speech).

### 2.2 Cost & Infrastructure
*   **Cost:** Strictly ₹0 for core functionality (no paid APIs, no cloud LLMs).
*   **Target Hardware:** Standard student laptop with 8-16GB RAM, CPU-only (no GPU required).
*   **Offline Capability:** Fully functional completely offline after the initial download of models and scheme database.

### 2.3 Security & Privacy
*   **Data Privacy:** No persistent storage of Personally Identifiable Information (PII). Profile data is kept strictly in-memory or in ephemeral session state.
*   **Security:** Implement prompt injection protection to prevent jailbreaking or malicious instructions via user text/audio.

### 2.4 Accessibility & UI
*   **Accessibility:** Support large text, high contrast modes, and screen reader compatibility.
*   **Design:** Mobile-first responsive UI, ensuring easy usage on smartphones and tablets.

## 3. Input/Output Specifications

*   **ASR Input:** `.wav` or `.webm` audio streams (16kHz, mono preferred).
*   **ASR Output:** Transcribed text string.
*   **LLM Input:** Structured prompt containing system instructions, conversation history, retrieved RAG context, and current query.
*   **LLM Output:** Markdown-formatted response containing answering text, source citations, and optional TTS markers.
*   **TTS Output:** `.wav` audio stream delivered to the frontend.

## 4. API Requirements

*   **REST API:** Provided by Python FastAPI.
*   **Endpoints:**
    *   `POST /api/chat`: Handles text-in, text-out.
    *   `POST /api/transcribe`: Handles audio-in, text-out.
    *   `POST /api/synthesize`: Handles text-in, audio-out.
    *   `GET /api/schemes`: Retrieve scheme master data.
    *   `POST /api/session/update`: Update transient user profile context.

## 5. Data Requirements

*   **Scheme Database:** Pre-processed SQLite database (with FTS5) containing structured scheme data (name, description, eligibility criteria, benefits, application process, URLs).
*   **Vector Database:** Local ChromaDB containing embeddings of scheme chunks for semantic similarity search.
*   **Supported Sources:** tn.gov.in, tnesevai.tn.gov.in, cmhelpline.tn.gov.in, tahdco.com, tncwwb.com, myscheme.gov.in (TN filter).
