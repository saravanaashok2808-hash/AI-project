# 📦 How to Share This Project with Your Colleague

This guide explains how to package and send the **Tamil Nadu Multilingual Voice-Based Government Scheme Assistant** to your colleague, and how they can run it on their computer with zero hassle.

---

## ⚡ Summary for You (The Sender)

### Step 1: Create the Clean Lightweight Zip
Do **NOT** manually zip the folder from Windows Explorer, because `backend/venv` and `frontend/node_modules` are huge (5+ GB) and machine-specific.

Instead, run this command in terminal (or double-click it):
```cmd
backend\venv\Scripts\python.exe scripts\package_for_sharing.py
```
This automatically creates:
> **`tamilnadu-scheme-assistant.zip`** (only **~320 KB**!)

### Step 2: Send the Zip to Your Colleague
Because the zip is only **320 KB**, you can easily send it via:
- 📧 **Email Attachment** (Gmail / Outlook)
- 💬 **WhatsApp / Telegram / Slack / Discord**
- ☁️ **Google Drive / OneDrive**
- 💾 **USB Pen Drive**

---

## 💻 Instructions for Your Colleague (The Receiver)

Copy and paste the instructions below and send them to your colleague along with the zip file:

```markdown
### 🚀 How to Run Tamil Nadu Scheme Assistant

#### Prerequisites (one-time setup if not already installed):
1. **Python 3.10 or 3.11** (Download from https://www.python.org/downloads/)
   * ⚠️ IMPORTANT: Tick the box **"Add python.exe to PATH"** during installation!
2. **Node.js** (Download LTS version from https://nodejs.org/)

#### Steps to Run:
1. **Unzip** `tamilnadu-scheme-assistant.zip` to any folder (e.g. `C:\tamilnadu-scheme-assistant` or Desktop).
2. **Double-click `run_app.bat`** (or `scripts\start_local.bat`).

That's it! The launcher script will automatically:
- Create the Python virtual environment (`backend/venv`)
- Install all required backend packages (`FastAPI`, `edge-tts`, `torch`, `transformers`, etc.)
- Install frontend packages (`npm install`)
- Ingest and index all 59 verified Tamil Nadu government schemes into SQLite
- Start the FastAPI backend server on `http://127.0.0.1:8000`
- Start the React/Vite frontend on `http://127.0.0.1:5173`
- Automatically open your default web browser to the application!

#### How to Use the App:
1. **Sign In / Sign Up**: Enter your name or choose "Continue as Guest".
2. **Citizen Profile**: Fill in your basic details (Age, Gender, District, Income, Education, Community).
   * Pick your preferred human voice persona: **👩 பல்லவி (Pallavi)** or **👨 வள்ளுவர் (Valluvar)**.
3. **Personalized Assistant**:
   * Instantly see schemes matched to your profile.
   * Speak or type your questions in **Tamil**, **English**, or **Mixed Tamil-English**.
   * Listen to natural, empathetic voice guidance with full scheme breakdown, benefits, and official government application links!

#### Running Tests:
To verify that everything works:
```cmd
backend\venv\Scripts\python.exe -m pytest backend/tests/
```
All 28 automated tests will run and pass!
```
