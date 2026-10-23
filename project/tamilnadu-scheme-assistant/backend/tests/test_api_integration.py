"""End-to-end API integration tests for the Tamil Nadu Scheme Assistant using FastAPI TestClient."""
import sys
from pathlib import Path

# Ensure backend directory is in sys.path
backend_dir = Path(__file__).resolve().parent.parent
if str(backend_dir) not in sys.path:
    sys.path.insert(0, str(backend_dir))

from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health():
    r = client.get("/api/health")
    assert r.status_code == 200
    data = r.json()
    assert data["status"] == "ok"

def test_list_schemes():
    r = client.get("/api/schemes/")
    assert r.status_code == 200
    schemes = r.json()
    assert len(schemes) >= 10, f"Expected 10+ schemes, got {len(schemes)}"
    for s in schemes:
        assert "scheme_id" in s
        assert "scheme_name_tamil" in s
        assert "scheme_name_english" in s
        assert "official_urls" in s

def test_get_single_scheme():
    r = client.get("/api/schemes/TN-KMUT-001")
    assert r.status_code == 200
    s = r.json()
    assert s["scheme_name_english"] == "Kalaignar Magalir Urimai Thogai (KMUT)"
    assert s["status"] == "Active"
    assert "kmut.tn.gov.in" in str(s["official_urls"])

def test_scheme_not_found():
    r = client.get("/api/schemes/NONEXISTENT")
    assert r.status_code == 404

def test_query_english_women():
    r = client.post("/api/query/", json={"query": "schemes for women"})
    assert r.status_code == 200
    q = r.json()
    assert q["detected_language"] == "en"
    assert q["detected_intent"] == "find_scheme"
    assert len(q["schemes"]) > 0
    scheme_ids = [s["scheme_id"] for s in q["schemes"]]
    assert "TN-KMUT-001" in scheme_ids, f"KMUT not in results: {scheme_ids}"

def test_query_farmer():
    r = client.post("/api/query/", json={"query": "farmer scheme"})
    assert r.status_code == 200
    q = r.json()
    assert len(q["schemes"]) > 0
    scheme_ids = [s["scheme_id"] for s in q["schemes"]]
    assert "TN-UZHAVAR-009" in scheme_ids, f"Uzhavar not in results: {scheme_ids}"

def test_query_with_profile():
    r = client.post("/api/query/", json={
        "query": "government help for women",
        "profile_updates": {"age": 24, "gender": "Female", "annual_income": 100000}
    })
    assert r.status_code == 200
    q = r.json()
    assert len(q["schemes"]) > 0
    for s in q["schemes"]:
        if s["scheme_id"] == "TN-KMUT-001":
            assert s["eligibility_status"] == "ELIGIBLE", f"KMUT status: {s['eligibility_status']}"
            break

def test_query_eligibility_check():
    r = client.post("/api/query/", json={
        "query": "Am I eligible?",
        "profile_updates": {"age": 65, "annual_income": 50000}
    })
    assert r.status_code == 200
    q = r.json()
    assert q["detected_intent"] == "check_eligibility"

def test_query_health_insurance():
    r = client.post("/api/query/", json={"query": "health insurance"})
    assert r.status_code == 200
    q = r.json()
    assert len(q["schemes"]) > 0

def test_official_sources_present():
    r = client.post("/api/query/", json={"query": "pension scheme"})
    assert r.status_code == 200
    q = r.json()
    if q["schemes"]:
        for s in q["schemes"]:
            assert len(s["official_urls"]) > 0, f"{s['scheme_id']} has no official URLs"

def test_empty_query_returns_all():
    r = client.post("/api/query/", json={"query": ""})
    assert r.status_code == 200
    q = r.json()
    assert len(q["schemes"]) >= 5

def test_voice_tts():
    r = client.post("/api/voice/tts", json={"text": "வணக்கம்! நான் அரசு நண்பன்.", "voice": "ta-IN-PallaviNeural"})
    assert r.status_code == 200
    assert r.headers["content-type"] == "audio/mpeg"
    assert len(r.content) > 1000
