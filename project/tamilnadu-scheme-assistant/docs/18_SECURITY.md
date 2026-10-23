# Security Architecture

## 1. Prompt Injection Prevention
* **System Prompt Framing:** Hardcode rigid system instructions.
* **Input Delimiting:** Wrap user queries in `<user_input>` XML tags.
* **Output Validation:** Use Pydantic strict schemas for LLM structured output.
* **RAG Treatment:** Retrieved documents are explicitly labeled as `[DATA]` and not instructions.

## 2. Input/Output Security
* **XSS Prevention:** Handled by React's default escaping. Markdown rendering uses DOMPurify.
* **Input Sanitization:** Handled by Pydantic v2 strict validation on the FastAPI backend.
* **File Uploads:** Voice payloads are size-limited (e.g., max 5MB), validated for MIME type (`audio/wav`, `audio/webm`).

## 3. Network & Infrastructure
* **Rate Limiting:** `slowapi` applied to LLM/ASR endpoints to prevent DoS.
* **CORS:** FastAPI `CORSMiddleware` restricted to frontend origin (`localhost:5173` for MVP).
* **Security Headers:** HSTS, X-Content-Type-Options via middleware.
* **Allowlist:** Official scheme URLs are strictly validated against an allowlist (e.g., `*.tn.gov.in`).

## 4. Data Security
* **No Raw SQL:** SQLAlchemy Core/ORM with parameterized queries.
* **Dependency Scanning:** Use `pip-audit` or `safety` in CI.
* **Admin Access:** Disabled in MVP. If added, requires robust AuthN/AuthZ.
* **RAG Poisoning Prevention:** Strict source verification. Only TN Govt verified URLs parsed.
