# Cost Analysis (₹0 Verification)

This document verifies that every component of the Tamil Nadu Government Scheme Assistant MVP incurs exactly ₹0 in costs, adhering to the project constraint.

## ₹0 Cost Verification Table

| Category | Component | Selected Solution | Cost | License / Plan | Why it's ₹0 |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Software OS** | Operating System | Windows 10/11, Ubuntu Linux | ₹0 | Commercial/Open Source | Standard student laptop OS. |
| **Development** | IDE | VS Code | ₹0 | MIT | Free open-source editor. |
| **Development** | Language | Python, Node.js | ₹0 | PSF, MIT | Open-source runtimes. |
| **AI Model: ASR** | Speech-to-Text | `faster-whisper` (large-v3-turbo) | ₹0 | MIT | Runs locally on CPU. Model weights are free on HuggingFace. |
| **AI Model: LLM** | Language Model | `Qwen3-4B-Instruct` via Ollama | ₹0 | Apache 2.0 | Runs locally. Weights available for free. |
| **AI Model: Embed** | Text Embeddings | `intfloat/multilingual-e5-small` | ₹0 | MIT | Runs locally via HuggingFace transformers. |
| **AI Model: TTS** | Text-to-Speech | `ai4bharat/indic-parler-tts` | ₹0 | MIT | Runs locally. Open-source model. |
| **Datasets** | Base Data | tn.gov.in, open data portals | ₹0 | Public Domain | Government information is freely accessible. |
| **Datasets** | Eval Data | AI4Bharat datasets, Common Voice | ₹0 | CC0 / CC-BY | Open-source research datasets. |
| **Database** | Relational DB | SQLite | ₹0 | Public Domain | Serverless, file-based database included with Python. |
| **Database** | Vector DB | ChromaDB | ₹0 | Apache 2.0 | Runs locally in-memory/file-system mode. No cloud tier used. |
| **Training** | Fine-tuning | None required for MVP | ₹0 | N/A | Using RAG and pre-trained models exclusively. |
| **Inference** | Compute | Student Laptop (Local CPU) | ₹0 | N/A | Utilizing existing hardware (8-16GB RAM). |
| **Hosting (Opt)** | Frontend Hosting | Vercel | ₹0 | Free Tier | Hobby tier is 100% free for static/React apps. |
| **Hosting (Opt)** | Backend Hosting | HuggingFace Spaces | ₹0 | Free CPU Tier | Provides free 16GB RAM CPU instances. |
| **Domain** | Domain Name | None / `.vercel.app` / `.hf.space` | ₹0 | Subdomain | Using default provided subdomains if hosted. |
| **Monitoring** | Analytics | Local JSON Logging | ₹0 | N/A | No paid third-party services used. |
| **Architecture** | RAG Framework | Custom pipeline | ₹0 | N/A | Built using standard Python; no paid LangChain integrations. |

## Alternative Hosting (If scaling beyond free tiers)
If the project needs to be hosted for a larger audience and free tiers are exhausted, the cheapest alternative is a basic VPS (e.g., Hetzner ARM64 instance for ~$5/month), but this is strictly out-of-scope for the ₹0 MVP.
