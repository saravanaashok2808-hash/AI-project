# ASR Fine-Tuning Analysis

## 1. Decision
**DO NOT FINE-TUNE FOR MVP.**

## 2. Rationale and Benchmark Evidence
The target hardware is an 8-16GB RAM laptop running CPU inference.

- **Pretrained Performance:** 
  `faster-whisper large-v3-turbo` achieves highly competitive Word Error Rates (WER) on the Common Voice Tamil test set and FLEURS Tamil test set (typically ~10-15% WER).
- **Domain Adaptation Context:** 
  While Tamil Nadu government schemes contain specific nomenclature (e.g., "Kalaignar Magalir Urimai Thogai"), the base vocabulary of `large-v3-turbo` is extensive enough to transcribe them phonetically.
- **Resource Constraints:** 
  Fine-tuning a Whisper Large model requires at least a 24GB VRAM GPU. While achievable via free cloud tiers (Colab), maintaining and deploying a custom LoRA adapter adds unnecessary complexity for the MVP.

## 3. Implementation Plan (Zero-Shot)
- **Model:** `faster-whisper large-v3-turbo`
- **Quantization:** INT8 (via CTranslate2)
- **Inference:** Fast CPU transcription using prompt conditioning if necessary (passing "Kalaignar Magalir Urimai Thogai" as a prefix prompt to bias the decoder).

## 4. Alternatives Considered
- **Alternative:** Fine-tune `whisper-small` using LoRA.
- **Why rejected:** Base `whisper-small` has a high baseline WER for Tamil (~30%+). Even with fine-tuning on government data, it struggles to surpass the zero-shot capabilities of the `large-v3-turbo` architecture.
- **Cost:** ₹0.
- **Hardware:** CPU only.
- **License:** MIT.

## 5. Risks and Fallback
- **Risks:** High error rate on heavy regional dialects or very fast speech.
- **Fallback:** Implement fuzzy string matching in the backend (e.g., `FuzzWrap` or FTS5 trm matching) to catch misspelled scheme names (e.g., "urimai togai" -> "Urimai Thogai").

## 6. Future Path (Post-MVP)
If WER on domain specific acronyms proves problematic in production:
1. Collect 10-20 hours of user queries.
2. Fine-tune `whisper-small` using PEFT/LoRA on a cloud GPU.
3. Deploy customized GGUF model.
