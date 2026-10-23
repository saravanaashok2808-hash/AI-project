"""Script to pre-download and verify AI models locally for zero-cost execution."""
import sys
import torch
from pathlib import Path

print("=" * 60)
print("  Tamil Nadu Scheme Assistant — Local Model Setup")
print("=" * 60)

# Check hardware
device = "cuda" if torch.cuda.is_available() else "cpu"
print(f"[*] Compute Device: {device.upper()}")
if device == "cuda":
    print(f"[*] GPU Name: {torch.cuda.get_device_name(0)}")
    print(f"[*] Total VRAM: {torch.cuda.get_device_properties(0).total_memory / (1024**3):.2f} GB")
print()

# 1. Embedding Model
embedding_model_id = "sentence-transformers/all-MiniLM-L6-v2"
print(f"[1/2] Verifying Embedding Model ({embedding_model_id})...")
try:
    from sentence_transformers import SentenceTransformer
    emb_model = SentenceTransformer(embedding_model_id, device=device)
    test_vec = emb_model.encode("Tamil Nadu Government Scheme")
    print(f"  [+] Embedding model loaded successfully! Dim: {len(test_vec)}")
except Exception as e:
    print(f"  [-] Failed to load embedding model: {e}")

print()

# 2. Main LLM
llm_model_id = "Qwen/Qwen2.5-3B-Instruct"
print(f"[2/2] Checking Main LLM ({llm_model_id})...")
print("Note: If not already downloaded, this will download ~5.8 GB from HuggingFace.")
choice = input("Would you like to download/load the LLM now? (y/n) [default: y]: ").strip().lower()
if choice in ["", "y", "yes"]:
    try:
        from transformers import AutoModelForCausalLM, AutoTokenizer
        print(f"  Downloading/Loading tokenizer for {llm_model_id}...")
        tokenizer = AutoTokenizer.from_pretrained(llm_model_id, trust_remote_code=True)
        print("  Tokenizer ready.")
        
        print(f"  Downloading/Loading model weights on {device} (float16)...")
        dtype = torch.float16 if device == "cuda" else torch.float32
        model = AutoModelForCausalLM.from_pretrained(
            llm_model_id,
            torch_dtype=dtype,
            device_map="auto" if device == "cuda" else None,
            low_cpu_mem_usage=True,
            trust_remote_code=True
        )
        print("  [+] LLM weights loaded successfully!")
    except Exception as e:
        print(f"  [-] Could not complete LLM download: {e}")
else:
    print("  Skipped LLM download. The backend will use the rule-based grounded explanation fallback.")

print("\n[+] Verification complete!")
