"""Tests for the Eligibility Engine — deterministic rule-based evaluation."""
import sys
from pathlib import Path

# Add project root to path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))
sys.path.insert(0, str(PROJECT_ROOT / "backend"))

from app.models.session import UserProfile
from app.eligibility.rule_evaluator import EligibilityEngine


# ─── Sample Scheme Data ───────────────────────────────────────────────────────

KMUT_SCHEME = {
    "scheme_id": "TN-KMUT-001",
    "scheme_name_english": "Kalaignar Magalir Urimai Thogai (KMUT)",
    "eligibility_rules": {
        "age": {"min": 21, "max": 100},
        "gender": ["Female", "Transgender"],
        "income_limit_annual": 250000,
        "residence": "Tamil Nadu",
        "community": ["Any"]
    }
}

OAP_SCHEME = {
    "scheme_id": "TN-OAP-006",
    "scheme_name_english": "Old Age Pension Scheme",
    "eligibility_rules": {
        "age": {"min": 60, "max": 120},
        "gender": ["Any"],
        "income_limit_annual": 100000,
        "residence": "Tamil Nadu",
        "community": ["Any"]
    }
}

TAHDCO_SCHEME = {
    "scheme_id": "TN-TAHDCO-011",
    "scheme_name_english": "TAHDCO Self Employment and Business Subsidy Scheme",
    "eligibility_rules": {
        "age": {"min": 18, "max": 45},
        "gender": ["Any"],
        "community": ["SC", "ST", "Scheduled Caste", "Scheduled Tribe"],
        "income_limit_annual": 300000,
        "residence": "Tamil Nadu"
    }
}

DISABILITY_SCHEME = {
    "scheme_id": "TN-DIFFABLE-008",
    "scheme_name_english": "Monthly Maintenance Allowance for Differently Abled Persons",
    "eligibility_rules": {
        "age": {"min": 0, "max": 120},
        "gender": ["Any"],
        "disability_percentage": {"min": 40},
        "residence": "Tamil Nadu",
        "community": ["Any"]
    }
}


# ─── Tests ─────────────────────────────────────────────────────────────────────

def test_eligible_woman_for_kmut():
    """A 30-year-old woman with ₹1.5L income should be ELIGIBLE for KMUT."""
    profile = UserProfile(age=30, gender="Female", annual_income=150000)
    result = EligibilityEngine.evaluate(profile, KMUT_SCHEME)
    assert result.status == "ELIGIBLE", f"Expected ELIGIBLE, got {result.status}: {result.unmet_criteria}"
    assert len(result.unmet_criteria) == 0


def test_male_not_eligible_for_kmut():
    """A male should NOT be eligible for KMUT (women-only scheme)."""
    profile = UserProfile(age=35, gender="Male", annual_income=100000)
    result = EligibilityEngine.evaluate(profile, KMUT_SCHEME)
    assert result.status == "NOT_APPEARING_ELIGIBLE"
    assert any("பாலினம்" in c for c in result.unmet_criteria)


def test_high_income_not_eligible_for_kmut():
    """Income above ₹2.5L should fail KMUT eligibility."""
    profile = UserProfile(age=40, gender="Female", annual_income=500000)
    result = EligibilityEngine.evaluate(profile, KMUT_SCHEME)
    assert result.status == "NOT_APPEARING_ELIGIBLE"
    assert any("வருமானம்" in c for c in result.unmet_criteria)


def test_missing_income_potentially_eligible_kmut():
    """Woman with age but no income info should be POTENTIALLY_ELIGIBLE."""
    profile = UserProfile(age=25, gender="Female")
    result = EligibilityEngine.evaluate(profile, KMUT_SCHEME)
    assert result.status == "POTENTIALLY_ELIGIBLE"
    assert any("வருமானம்" in c for c in result.missing_criteria)


def test_empty_profile_insufficient_info():
    """Empty profile should return INSUFFICIENT_INFORMATION."""
    profile = UserProfile()
    result = EligibilityEngine.evaluate(profile, KMUT_SCHEME)
    assert result.status in ("INSUFFICIENT_INFORMATION", "POTENTIALLY_ELIGIBLE")
    assert len(result.missing_criteria) > 0


def test_senior_eligible_for_oap():
    """65-year-old with low income should be ELIGIBLE for OAP."""
    profile = UserProfile(age=65, annual_income=60000)
    result = EligibilityEngine.evaluate(profile, OAP_SCHEME)
    assert result.status == "ELIGIBLE"


def test_young_not_eligible_for_oap():
    """30-year-old should NOT be eligible for OAP (age 60+ required)."""
    profile = UserProfile(age=30, annual_income=50000)
    result = EligibilityEngine.evaluate(profile, OAP_SCHEME)
    assert result.status == "NOT_APPEARING_ELIGIBLE"
    assert any("வயது" in c for c in result.unmet_criteria)


def test_sc_eligible_for_tahdco():
    """SC community member aged 25 with income ₹2L should be ELIGIBLE for TAHDCO."""
    profile = UserProfile(age=25, community="SC", annual_income=200000)
    result = EligibilityEngine.evaluate(profile, TAHDCO_SCHEME)
    assert result.status == "ELIGIBLE"


def test_general_not_eligible_for_tahdco():
    """General community should NOT be eligible for TAHDCO SC/ST scheme."""
    profile = UserProfile(age=25, community="General", annual_income=200000)
    result = EligibilityEngine.evaluate(profile, TAHDCO_SCHEME)
    assert result.status == "NOT_APPEARING_ELIGIBLE"


def test_disabled_person_eligible():
    """Person with 60% disability should be ELIGIBLE for disability allowance."""
    profile = UserProfile(is_differently_abled=True, disability_percentage=60)
    result = EligibilityEngine.evaluate(profile, DISABILITY_SCHEME)
    assert result.status == "ELIGIBLE"


def test_non_disabled_not_eligible_for_disability_scheme():
    """Non-disabled person should NOT be eligible for disability scheme."""
    profile = UserProfile(is_differently_abled=False)
    result = EligibilityEngine.evaluate(profile, DISABILITY_SCHEME)
    assert result.status == "NOT_APPEARING_ELIGIBLE"


def test_result_to_dict():
    """Test RuleEvaluationResult serialization."""
    profile = UserProfile(age=25, gender="Female", annual_income=100000)
    result = EligibilityEngine.evaluate(profile, KMUT_SCHEME)
    d = result.to_dict()
    assert "scheme_id" in d
    assert "status" in d
    assert "matched_criteria" in d
    assert isinstance(d["matched_criteria"], list)


if __name__ == "__main__":
    tests = [
        test_eligible_woman_for_kmut,
        test_male_not_eligible_for_kmut,
        test_high_income_not_eligible_for_kmut,
        test_missing_income_potentially_eligible_kmut,
        test_empty_profile_insufficient_info,
        test_senior_eligible_for_oap,
        test_young_not_eligible_for_oap,
        test_sc_eligible_for_tahdco,
        test_general_not_eligible_for_tahdco,
        test_disabled_person_eligible,
        test_non_disabled_not_eligible_for_disability_scheme,
        test_result_to_dict,
    ]
    passed = 0
    failed = 0
    for t in tests:
        try:
            t()
            print(f"  ✓ {t.__name__}")
            passed += 1
        except Exception as e:
            print(f"  ✗ {t.__name__}: {e}")
            failed += 1
    print(f"\n{passed} passed, {failed} failed out of {len(tests)} tests")
