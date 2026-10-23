# Tamil Nadu Multilingual Voice-Based Government Scheme Assistant

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Cost: ₹0](https://img.shields.io/badge/Cost-₹0-green.svg)](#)
[![Tamil](https://img.shields.io/badge/Language-Tamil-blue.svg)](#)
[![Tests: 28/28 Passed](https://img.shields.io/badge/Tests-28%2F28%20Passed-brightgreen.svg)](#)

A voice-enabled, Tamil-first AI assistant that helps citizens discover Tamil Nadu government welfare schemes through natural Tamil, English, or mixed colloquial conversation. Built entirely with open-source tools at **₹0 core cost**.

---

## 🎯 What It Does

- **Natural Human Neural Voice** — Clear, expressive Tamil & Indian-English voices (👩 பல்லவி & 👨 வள்ளுவர் via Edge-TTS & gTTS fallback).
- **Citizen Onboarding & Profile Matching** — 3-step structured citizen questionnaire (Age, Gender, District, Education, Employment, Annual Income, Community, Disability) for personalized scheme filtering.
- **Empathetic Companion Persona ("அரசு நண்பன்")** — Warm, conversational guidance that explains schemes, benefits, documents, and application steps like a helpful friend.
- **59 Verified Government Schemes** — Authoritative scheme database compiled from verified TN government sources (`kmut.tn.gov.in`, `tndistrict.tn.gov.in`, `tnstc.gov.in`, `pudhumaimaippan.tn.gov.in`, etc.).
- **Deterministic Eligibility Engine** — Strict Python rule evaluation (zero LLM hallucinations) that computes `ELIGIBLE`, `INELIGIBLE`, or `POTENTIALLY_ELIGIBLE`.
- **Offline / Local Acceleration** — GPU acceleration on RTX 3050 (or automatic CPU fallback) with raw PyTorch & HuggingFace Transformers (NO Ollama dependency).
- **₹0 Cost** — Completely free, open-source, no paid API keys or credit cards needed.

---

## 🏗️ Architecture

```
Citizen (Voice / Text)
      ↓
Web Speech API / faster-whisper ASR
      ↓
FastAPI Router (Language Detection & Intent Extraction)
      ↓
Citizen Profile Engine ──► Deterministic Rule Engine (Zero Hallucination)
      ↓                                    ▲
SQLite FTS5 Scheme Search ─────────────────┘
      ↓
Empathetic Voice Generator (Qwen2.5 Raw PyTorch CUDA/CPU)
      ↓
Neural TTS Audio Stream (Edge-TTS / gTTS fallback)
      ↓
Citizen Browser (Audio Playback + Scheme Cards + Official Application URLs)
```

---

## 🛠️ Tech Stack

| Component | Technology | Mode | License |
|-----------|-----------|------|---------|
| **Backend** | Python FastAPI + Uvicorn | Local Async Server | MIT |
| **Frontend** | React 19 + Vite + Tailwind CSS | Responsive Web Client | MIT |
| **Database** | SQLite + FTS5 Full-Text Search | Local Embedded DB | Public Domain |
| **Speech Recognition** | Web Speech API (`ta-IN`, `en-IN`) | Local Browser Engine | W3C Standard |
| **Speech Synthesis (TTS)** | `edge-tts` (`ta-IN-PallaviNeural`, `ta-IN-ValluvarNeural`) + `gTTS` | High-Clarity Neural Audio | MIT / Apache |
| **Main LLM** | `Qwen/Qwen2.5-1.5B-Instruct` | Raw PyTorch CUDA/CPU (NO Ollama) | Apache 2.0 |
| **Eligibility Engine** | Deterministic Python Rule Evaluator | Zero Hallucination Logic | MIT |
| **Voice Persona** | Arasu Nanban ("அரசு நண்பன்") | Natural Colloquial Tamil & English | MIT |
| **Total Cost** | ₹0 Core Cost | 100% Free & Open-Source | Free |

---

## 📋 Prerequisites

- **Python 3.10 or 3.11** (Ensure "Add Python to PATH" is ticked)
- **Node.js 18+ or 20+**
- Windows 10/11 (CUDA GPU supported & auto-detected; CPU also fully supported)

---

## 🚀 1-Click Launch

Simply double-click or run:

```bat
run_app.bat
```
*(or `scripts\start_local.bat`)*

This script is self-healing:
1. Detects or creates the isolated virtual environment (`backend/venv`).
2. Installs required Python and Node.js dependencies automatically.
3. Indexes and validates all 59 verified schemes into SQLite (`data/schemes.db`).
4. Boots the FastAPI backend on `http://127.0.0.1:8000`.
5. Boots the Vite frontend on `http://127.0.0.1:5173`.
6. Launches your default web browser directly to the application!

---

## 📦 How to Share with a Colleague

To package the project into a lightweight zip file (~320 KB) that can be sent over email, WhatsApp, or Google Drive:

```cmd
backend\venv\Scripts\python.exe scripts\package_for_sharing.py
```

This creates `tamilnadu-scheme-assistant.zip` excluding the heavy `venv` and `node_modules` folders. When your colleague unzips it and runs `run_app.bat`, everything will configure and boot automatically!

See [HOW_TO_SHARE_WITH_COLLEAGUE.md](file:///h:/PROJECTS/tamilnadu-scheme-assistant/tamilnadu-scheme-assistant/HOW_TO_SHARE_WITH_COLLEAGUE.md) for complete sharing instructions.

---

## 🧪 Automated Test Suite

Run all automated unit and integration tests:

```cmd
backend\venv\Scripts\python.exe -m pytest backend/tests/ -v
```

**Results: 28/28 tests passing (100% pass rate)**:
- 12 End-to-end API integration tests (health, scheme retrieval, search, profile matching, voice TTS)
- 12 Deterministic rule engine tests (age, gender, income, community, disability, edge cases)
- 4 Native Tamil query resolution tests

---

## 📜 License

MIT License — see [LICENSE](LICENSE) file.
