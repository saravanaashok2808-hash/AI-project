"""Test queries in native Tamil script against the Assistant API using FastAPI TestClient."""
import sys
from pathlib import Path
import pytest

# Ensure backend directory is in sys.path
backend_dir = Path(__file__).resolve().parent.parent
if str(backend_dir) not in sys.path:
    sys.path.insert(0, str(backend_dir))

from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

QUERIES = [
    {
        "query": "மகளிர் திட்டம்",
        "expected_lang": "ta",
        "expected_scheme": "TN-KMUT-001"
    },
    {
        "query": "விவசாயிகளுக்கான உதவி என்ன?",
        "expected_lang": "ta",
        "expected_scheme": "TN-UZHAVAR-009"
    },
    {
        "query": "மருத்துவக் காப்பீடு விவரம்",
        "expected_lang": "ta",
        "expected_scheme": "TN-CMCHIS-004"
    },
    {
        "query": "முதியோர் ஓய்வூதியம் பெறுவது எப்படி?",
        "expected_lang": "ta",
        "expected_scheme": "TN-OAP-006"
    }
]

@pytest.mark.parametrize("case", QUERIES)
def test_tamil_query_resolution(case):
    r = client.post("/api/query/", json={"query": case["query"]})
    assert r.status_code == 200, f"Query {case['query']} failed with {r.status_code}"
    res = r.json()
    assert res["detected_language"] == case["expected_lang"], f"Lang {res['detected_language']} != {case['expected_lang']}"
    found_ids = [s["scheme_id"] for s in res["schemes"]]
    assert case["expected_scheme"] in found_ids, f"Scheme {case['expected_scheme']} not in {found_ids} for {case['query']}"
