# 15 API Specification

## Technology
- **Framework**: FastAPI (Python)
- **Deployment**: Local Uvicorn / Docker Compose
- **Cost**: ₹0

## Endpoints

### 1. `POST /api/query`
Processes text queries.
- **Request**: `{ "session_id": "str", "query": "str" }`
- **Response**: `{ "reply": "str", "schemes_referenced": ["TN-KMUT-001"] }`

### 2. `POST /api/voice`
Accepts audio file, runs ASR (`faster-whisper`), then processes via `/api/query`.
- **Request**: `multipart/form-data` with `file` (audio/wav or webm), `session_id`.
- **Response**: `{ "transcribed_text": "str", "reply": "str", "audio_response_url": "str" }`

### 3. `GET /api/schemes`
List/Search schemes.
- **Params**: `?q=women&category=empowerment`
- **Response**: `[ { "scheme_id": "...", "name": "..." } ]`

### 4. `GET /api/schemes/{id}`
Get full details.
- **Response**: Full scheme JSON object.

### 5. `POST /api/eligibility`
Check eligibility against known rules.
- **Request**: `{ "scheme_id": "...", "user_profile": { "age": 25, "gender": "Female" } }`
- **Response**: `{ "eligible": true, "missing_info": ["income"] }`

### 6. `GET /api/session`
- **Params**: `?session_id=...`
- **Response**: `{ "session_id": "...", "context_data": {} }`

### 7. `PATCH /api/session`
Update known user traits.
- **Request**: `{ "session_id": "...", "context_data": { "income": 100000 } }`
- **Response**: `200 OK`

### 8. `DELETE /api/session`
Clear conversation context.
- **Request**: `{ "session_id": "..." }`
- **Response**: `200 OK`

### 9. `POST /api/tts`
Generate TTS for given text (`ai4bharat/indic-parler-tts`).
- **Request**: `{ "text": "str", "lang": "ta" }`
- **Response**: Audio stream (e.g. `audio/wav`).

### 10. `WebSocket /ws/conversation`
Streaming conversation for low-latency web interfaces.
- **Event**: `{"type": "user_msg", "content": "..."}`
- **Response Stream**: `{"type": "bot_token", "content": "..."}`

## Error Responses
- `400 Bad Request`: Validation errors.
- `404 Not Found`: Scheme or Session missing.
- `500 Internal Error`: Model inference failed.

## Rate Limiting & CORS
- **CORS**: Allowed origins configured via env vars (e.g., `http://localhost:5173` for Vite).
- **Rate Limiting**: 10 req/min for inference endpoints to protect local resources.
