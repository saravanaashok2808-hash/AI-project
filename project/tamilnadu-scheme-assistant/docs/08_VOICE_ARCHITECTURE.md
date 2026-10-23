# 08 Voice Architecture

This document describes the end-to-end voice pipeline for the Tamil Nadu Government Scheme Assistant.

## 1. Audio Capture
- **Technology:** Browser Web Audio API / MediaRecorder API.
- **Process:** The frontend records user speech in real-time.
- **Mobile Voice Experience:** Responsive UI with a push-to-talk or tap-to-talk button.

## 2. Audio Format and Encoding
- **Frontend Format:** `WebM` (Opus codec) for web, standard for modern browsers.
- **Backend Conversion:** Converted to `WAV` (16kHz, mono) using FFmpeg (or python-ffmpeg) before ASR inference.

## 3. Streaming vs. Batch ASR
- **Decision:** Batch ASR (Chunked).
- **Why:** Streaming ASR on low-end CPUs is computationally expensive and error-prone. The user finishes speaking, and the recorded chunk is sent to the backend for processing.

## 4. ASR Model Loading and Inference
- **Model:** `faster-whisper` (`large-v3-turbo`, INT8).
- **Execution:** Loaded into memory on startup via FastAPI lifecycle events to avoid cold-start latency.
- **Inference:** The WAV file is transcribed.

## 5. Language Detection on ASR Output
- **Pre-filter:** Unicode script detection (checks if output characters are Tamil or English).
- **Primary Detection:** `lingua-py` to classify short text confidently and identify Tanglish (Tamil written in English script or mixed).

## 6. Text Normalization (Tamil / English / Tanglish)
- **Rule-based:** Mapping common Tanglish scheme names to standard Tamil/English names (e.g., "magalir urimai" -> "Magalir Urimai Thogai").
- **LLM assistance:** Prompts given to the LLM explicitly state the user's detected language to ensure the response matches the query language.

## 7. TTS Synthesis Pipeline
- **Model:** `indic-parler-tts` (Tamil) or fallback to `mms-tts-tam`.
- **Process:** LLM response text is chunked by sentence.
- **Streaming:** First sentence is synthesized and streamed to the frontend immediately, hiding the latency of subsequent sentences.

## 8. Audio Playback
- **Technology:** Web Audio API.
- **Handling:** Frontend queues incoming audio chunks and plays them sequentially for a seamless voice experience.

## 9. Fallback Mechanisms
- **ASR Failure:** If audio is too noisy or model fails, fallback to UI text input asking "Could you please type that or say it again clearly?"
- **TTS Failure / Latency:** The text response is *always* displayed on screen instantly. If TTS takes >5 seconds, the user can read the text without waiting for audio.

## 10. Latency Budget Breakdown (Target)
| Step | Time Budget |
| :--- | :--- |
| Network (Audio Upload) | 200ms |
| ASR Inference (10s audio) | 2000ms |
| NLP & RAG Retrieval | 500ms |
| LLM First Token (TTFT) | 1000ms |
| TTS First Sentence | 2000ms |
| Network (Audio Download) | 200ms |
| **Total perceived latency** | **~5.9 seconds** |

## 11. Browser Compatibility Matrix
- **Chrome / Edge / Brave:** Fully supported (WebM Opus).
- **Firefox:** Supported.
- **Safari (iOS/macOS):** Requires MP4/AAC or specific WebM support polyfills. MediaRecorder is supported in iOS 14.3+.
