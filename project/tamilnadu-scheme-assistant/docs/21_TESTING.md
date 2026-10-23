# Testing Strategy

## 1. Test Levels
* **Unit Tests (`pytest`):** 
  * Eligibility rule logic.
  * Markdown parsers.
  * API endpoints (mocking AI models).
  * Data validation logic & profile extraction.
* **Integration Tests:**
  * ASR -> NLU pipeline.
  * NLU -> RAG.
  * RAG -> Eligibility engine.
  * Eligibility -> LLM generation -> TTS.
* **E2E Tests:** Full user journeys in Tamil, English, and Tanglish.
* **Security Tests:** Inject prompt engineering attacks (prompt injection, XSS, SQL injection, fake URLs) in tests to verify system boundaries.

## 2. Test Configuration
* Framework: `pytest` with `pytest-asyncio`.
* Fixtures: Pre-configured user profiles, mock audio files, mock DB schemas in `conftest.py`.
* Coverage Target: >80% for backend business logic.

## 3. CI/CD Integration
* GitHub Actions workflow to run `pytest`, `eslint`, and type checking on every PR.
