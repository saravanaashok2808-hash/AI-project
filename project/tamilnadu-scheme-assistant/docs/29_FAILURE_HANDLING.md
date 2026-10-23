# Failure Handling & Graceful Degradation

This document defines the system's behavior across various failure modes to ensure a robust user experience, even on constrained hardware.

## 1. Information Failures

| Scenario | System Behavior | User-Facing Message (Tamil / English) |
| :--- | :--- | :--- |
| **Unknown Question** (Out of scope) | Intent classifier rejects query. LLM is not called. | "I can only assist with TN Govt schemes." / "நான் தமிழ்நாடு அரசு திட்டங்கள் குறித்து மட்டுமே உதவ முடியும்." |
| **No Scheme Found** (RAG returns low similarity) | LLM instructed to refuse guessing. | "No specific scheme found for this request. Please contact e-Sevai." / "இந்தக் கோரிக்கைக்கு ஏற்ற திட்டம் எதுவும் கிடைக்கவில்லை." |
| **Insufficient Info** (Vague query) | LLM asks 1-2 clarifying questions. | "Could you specify your age and occupation?" / "உங்கள் வயது மற்றும் தொழிலைக் குறிப்பிட முடியுமா?" |
| **Conflicting Sources** | LLM highlights the conflict or provides the most recent. | "There are different criteria listed. Please verify at tn.gov.in." |

## 2. Component Failures

| Failure Mode | Detection | Graceful Degradation Strategy |
| :--- | :--- | :--- |
| **ASR Failure** (Unclear audio/Noise) | Whisper confidence score < threshold. | Prompt user to speak again or use text input. "Please speak clearly or type your question." |
| **TTS Failure** (Model crash/OOM) | Backend exception during audio generation. | Fallback to displaying Text-Only response on the UI. |
| **LLM Failure** (Ollama timeout/crash) | HTTP timeout (>15s) or connection refused. | Return direct RAG text snippets without summarization. "Summary unavailable. Here are relevant documents:" |
| **RAG/Vector DB Failure** | ChromaDB connection error. | Fallback to SQLite Full Text Search (FTS5) keyword matching. |
| **Database Failure** (SQLite locked) | SQL exception. | Return generic error. "System maintenance. Please try again." |

## 3. System & Network Failures

*   **Model Loading Failure (Startup):** If a model (e.g., ASR) fails to load into RAM (due to 8GB limit), the backend starts anyway but disables voice features, operating in **Text-Only Mode**.
*   **Network Failure:** Since the system is designed to be 100% local, it is immune to internet outages once models are downloaded.

## 4. Hardware Degradation Strategy (RAM Constraints)

If running on exactly 8GB RAM, the system orchestrator will aggressively manage memory:
1.  **Unload TTS:** TTS model is evicted from memory immediately after generating audio.
2.  **Sequential Processing:** ASR model is unloaded before the LLM generates text to prevent OOM errors, though this increases latency. (Controlled via environment variable `LOW_MEM_MODE=true`).
