"""Debug script to investigate query search results."""
import requests
import json

BASE = "http://127.0.0.1:8000"

# Test what "schemes for women" returns
r = requests.post(f"{BASE}/api/query/", json={"query": "schemes for women"})
q = r.json()
print(f"Query: 'schemes for women'")
print(f"  Language: {q['detected_language']}")
print(f"  Intent: {q['detected_intent']}")
print(f"  Schemes count: {len(q['schemes'])}")
for s in q["schemes"]:
    print(f"    {s['scheme_id']}: {s['scheme_name_english']} [{s.get('eligibility_status', 'N/A')}]")

print()

# Test farmer
r2 = requests.post(f"{BASE}/api/query/", json={"query": "farmer scheme"})
q2 = r2.json()
print(f"Query: 'farmer scheme'")
print(f"  Schemes count: {len(q2['schemes'])}")
for s in q2["schemes"]:
    print(f"    {s['scheme_id']}: {s['scheme_name_english']}")

print()

# Test with profile
r3 = requests.post(f"{BASE}/api/query/", json={
    "query": "government help for women",
    "profile_updates": {"age": 24, "gender": "Female", "annual_income": 100000}
})
q3 = r3.json()
print(f"Query: 'government help for women' + profile")
print(f"  Schemes count: {len(q3['schemes'])}")
for s in q3["schemes"]:
    print(f"    {s['scheme_id']}: {s['scheme_name_english']} [{s.get('eligibility_status', 'N/A')}]")
