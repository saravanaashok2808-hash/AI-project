# Tamil Language Guidelines

This document standardizes how the system handles Tamil text, colloquialisms, and terminology to ensure respectful and accurate communication with citizens.

## 1. Tamil Terminology for Government Concepts

To maintain consistency and professionalism, the assistant must use standardized official terminology.

| English Concept | Standard Tamil Translation | Avoid |
| :--- | :--- | :--- |
| Scheme / Plan | திட்டம் (Thittam) | ஸ்கீம் (Scheme) |
| Government | அரசாங்கம் / அரசு (Arasu) | கவர்மெண்ட் (Government) |
| Eligibility | தகுதி (Thaguthi) | எலிஜிபிலிட்டி (Eligibility) |
| Application | விண்ணப்பம் (Vinnappam) | அப்ளிகேஷன் (Application) |
| Subsidy | மானியம் (Maaniyam) | சப்சிடி (Subsidy) |
| Loan | கடன் (Kadan) | லோன் (Loan) |
| Certificate | சான்றிதழ் (Saandridhazh) | சர்டிபிகேட் (Certificate) |

## 2. Tanglish Normalization Rules

Users will frequently type in Tanglish (Tamil in Latin script).
*   **Rule:** The system must normalize Tanglish to proper Tamil script *before* performing vector search.
*   **Implementation:** We rely on the multilingual capabilities of `intfloat/multilingual-e5-small`, which handles mixed scripts reasonably well. If performance drops, we will use a lightweight transliteration library (e.g., AI4Bharat indic-trans).
*   **Response:** Regardless of whether the user types in Tamil script or Tanglish, the LLM must respond in **proper Tamil script** or English, avoiding responding in Tanglish.

## 3. Colloquial vs. Formal Tamil

*   **Input (ASR):** The ASR model (faster-whisper) handles colloquial Tamil well. We accept spoken slang (e.g., "vendum" vs "venum").
*   **Output (LLM & TTS):** Responses must be in **Standard Formal Tamil (எழுத்துத் தமிழ்)** to sound official and clear, but not overly archaic. 
*   **Style:** Polite and respectful. Always use the plural/respectful suffix (e.g., செய்யுங்கள் instead of செய்).

## 4. Avoiding Machine Translation Artifacts

Direct translations from English scheme docs often sound unnatural in Tamil.
*   **Guideline:** Prompt the LLM to generate responses naturally in Tamil, rather than translating an English thought process.
*   **Prompt enforcement:** "Write the response naturally in Tamil. Do not translate literally from English."

## 5. Tamil Unicode Handling

*   All internal processing, database storage, and API JSON payloads MUST use UTF-8 encoding.
*   Python code must explicitly specify `encoding='utf-8'` when reading/writing files.
*   No ASCII-escaping in JSON responses (`ensure_ascii=False` in FastAPI/Pydantic).
