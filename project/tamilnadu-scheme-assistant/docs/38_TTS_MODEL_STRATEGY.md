# TTS Model Strategy

## 1. Primary Model Decision
**Decision:** `ai4bharat/indic-parler-tts`
- **Reason:** Provides the highest quality, most natural-sounding Tamil speech synthesis available in open source.
- **Fine-Tuning:** DO NOT FINE-TUNE. Pretrained weights are excellent.
- **Hardware:** CPU inference (moderate latency).
- **License:** Apache 2.0
- **Cost:** ₹0

## 2. Fallback Model Decision
**Decision:** `facebook/mms-tts-tam`
- **Reason:** VITS-based architecture that is exceptionally fast on CPU. Useful if the primary model causes latency bottlenecks on an 8GB RAM machine while ASR and LLM are also loaded in memory.
- **License:** CC-BY-NC 4.0
- **Hardware:** Very lightweight on CPU.

## 3. Ultra-Low Latency Option
**Decision:** `espeak-ng`
- **Reason:** For ultra-constrained environments or instantaneous feedback requirements. Highly robotic but guarantees 0ms load time and near-zero memory footprint.
- **License:** GPL-3.0

## 4. Implementation details
- The Python FastAPI backend will dynamically select the TTS engine based on system load or user configuration.
- Audio will be streamed back to the React frontend in chunks (if supported) or as a completed `.wav`/`.mp3` payload.

## 5. Risks
- TTS inference blocks the CPU, potentially causing stuttering if the LLM is concurrently generating tokens.
- **Mitigation:** Implement strict sequential processing (wait for full LLM sentence completion before triggering TTS).
