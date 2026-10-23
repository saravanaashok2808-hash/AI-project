from typing import Any, Optional
from app.models.session import UserProfile

class RuleEvaluationResult:
    def __init__(self, scheme_id: str):
        self.scheme_id = scheme_id
        self.status = "INSUFFICIENT_INFORMATION"  # ELIGIBLE, POTENTIALLY_ELIGIBLE, NOT_APPEARING_ELIGIBLE, INSUFFICIENT_INFORMATION
        self.matched_criteria: list[str] = []
        self.unmet_criteria: list[str] = []
        self.missing_criteria: list[str] = []
        self.reasoning_tamil: str = ""
        self.reasoning_english: str = ""
        self.confidence: str = "HIGH"

    def to_dict(self) -> dict[str, Any]:
        return {
            "scheme_id": self.scheme_id,
            "status": self.status,
            "matched_criteria": self.matched_criteria,
            "unmet_criteria": self.unmet_criteria,
            "missing_criteria": self.missing_criteria,
            "reasoning_tamil": self.reasoning_tamil,
            "reasoning_english": self.reasoning_english,
            "confidence": self.confidence
        }

class EligibilityEngine:
    @staticmethod
    def evaluate(profile: UserProfile, scheme_dict: dict[str, Any]) -> RuleEvaluationResult:
        scheme_id = scheme_dict.get("scheme_id", "UNKNOWN")
        rules = scheme_dict.get("eligibility_rules", {})
        if isinstance(rules, str):
            import json
            rules = json.loads(rules)

        result = RuleEvaluationResult(scheme_id)

        # 1. Evaluate Age
        age_rules = rules.get("age")
        if age_rules:
            min_age = age_rules.get("min")
            max_age = age_rules.get("max")
            is_unrestricted = (min_age in (None, 0)) and (max_age is None or max_age >= 100)
            if not is_unrestricted:
                if profile.age is None:
                    result.missing_criteria.append("Age / வயது")
                else:
                    age_ok = True
                    if min_age is not None and profile.age < min_age:
                        age_ok = False
                    if max_age is not None and profile.age > max_age:
                        age_ok = False
                    
                    if age_ok:
                        result.matched_criteria.append(f"வயது வரம்பு ({profile.age} வயது) பொருந்துகிறது")
                    else:
                        result.unmet_criteria.append(
                            f"வயது {profile.age} தேவையை பூர்த்தி செய்யவில்லை (தேவை: {min_age or 0} முதல் {max_age or 'வரம்பில்லை'} வரை)"
                        )
            else:
                if profile.age is not None:
                    result.matched_criteria.append(f"வயது வரம்பு ({profile.age} வயது) பொருந்துகிறது")

        # 2. Evaluate Gender
        gender_rules = rules.get("gender", ["Any"])
        if "Any" not in gender_rules and len(gender_rules) > 0:
            if not profile.gender:
                result.missing_criteria.append("Gender / பாலினம்")
            else:
                user_gender = profile.gender.strip().capitalize()
                allowed_genders = [g.strip().capitalize() for g in gender_rules]
                
                is_matched = user_gender in allowed_genders
                if not is_matched and user_gender in ["Other", "Others", "Transgender"]:
                    if any(g in ["Transgender", "Other", "Others"] for g in allowed_genders):
                        is_matched = True

                if is_matched:
                    display_gender = "மற்றவை/Others" if user_gender in ["Other", "Others"] else user_gender
                    result.matched_criteria.append(f"பாலினம் ({display_gender}) பொருந்துகிறது")
                else:
                    result.unmet_criteria.append(
                        f"இத்திட்டம் {', '.join(gender_rules)} பயனாளிகளுக்கானது. நீங்கள் குறிப்பிட்ட பாலினம்: {profile.gender}"
                    )

        # 3. Evaluate Residence
        residence_rule = rules.get("residence")
        if residence_rule and residence_rule != "Any":
            if profile.residence:
                if "tamil nadu" in profile.residence.lower() or "தமிழ்நாடு" in profile.residence:
                    result.matched_criteria.append("தமிழ்நாடு வசிப்பிட தகுதி பொருந்துகிறது")
                else:
                    result.unmet_criteria.append("இத்திட்டம் தமிழ்நாடு வாழ் மக்களுக்கு மட்டுமே பொருந்தும்")
            else:
                # Default assume resident if asking about TN schemes, but flag if uncertain
                result.matched_criteria.append("தமிழ்நாடு வசிப்பிடம் (இயல்புநிலை)")

        # 4. Evaluate Annual Income Limit
        income_limit = rules.get("income_limit_annual")
        if income_limit is not None:
            if profile.annual_income is None:
                result.missing_criteria.append(f"ஆண்டு வருமானம் (வரம்பு: ₹{int(income_limit):,})")
            else:
                if profile.annual_income <= income_limit:
                    result.matched_criteria.append(
                        f"குடும்ப ஆண்டு வருமானம் (₹{int(profile.annual_income):,}) அனுமதிக்கப்பட்ட வரம்பிற்குள் (₹{int(income_limit):,}) உள்ளது"
                    )
                else:
                    result.unmet_criteria.append(
                        f"வருமானம் ₹{int(profile.annual_income):,} அனுமதிக்கப்பட்ட உச்சவரம்பை (₹{int(income_limit):,}) தாண்டியுள்ளது"
                    )

        # 5. Evaluate Student Status / Schooling
        student_req = rules.get("student_status")
        if student_req is not None:
            if profile.student_status is None:
                result.missing_criteria.append("மாணவர் நிலை (படித்து வருகிறீர்களா இல்லையா?)")
            elif profile.student_status == student_req:
                result.matched_criteria.append("மாணவர் நிலை பொருந்துகிறது")
            else:
                result.unmet_criteria.append("இத்திட்டம் தற்போது பயிலும் மாணவர்களுக்கானது மட்டுமே")

        schooling_req = rules.get("schooling_requirement")
        if schooling_req:
            if not profile.schooling_type:
                result.missing_criteria.append("பள்ளி கல்வி விவரம் (அரசுப் பள்ளி 6-12 ஆம் வகுப்பு)")
            else:
                if "govt" in profile.schooling_type.lower() or "அரசு" in profile.schooling_type.lower():
                    result.matched_criteria.append("அரசுப் பள்ளி கல்வி தகுதி பொருந்துகிறது")
                else:
                    result.unmet_criteria.append("அரசுப் பள்ளியில் 6 முதல் 12 வரை படித்திருக்க வேண்டும்")

        # 6. Evaluate Occupation / Farmer / Laborer / Weaver / Artisan
        occupation_req = rules.get("occupation")
        if occupation_req:
            allowed_occs = [o.lower() for o in (occupation_req if isinstance(occupation_req, list) else [occupation_req])]
            if not profile.occupation:
                result.missing_criteria.append(f"தொழில் நிலை ({', '.join(allowed_occs)})")
            else:
                occ_lower = profile.occupation.lower()
                if any(k in occ_lower or occ_lower in k for k in allowed_occs):
                    result.matched_criteria.append(f"தொழில் ({profile.occupation}) பொருந்துகிறது")
                else:
                    result.unmet_criteria.append(f"இத்திட்டம் {', '.join(allowed_occs)} மட்டுமே பொருந்தும்")

        # 7. Evaluate Employment Status
        emp_req = rules.get("employment_status")
        if emp_req:
            user_unemployed = False
            emp_status = getattr(profile, "employment_status", None)
            if emp_status and "unemployed" in str(emp_status).lower():
                user_unemployed = True
            elif profile.occupation and any(k in profile.occupation.lower() for k in ["unemployed", "வேலையில்லை", "வேலை இல்லை", "வேலை தேடுபவர்"]):
                user_unemployed = True
                
            if user_unemployed:
                result.matched_criteria.append("வேலையில்லாத இளைஞர் தகுதி பொருந்துகிறது")
            elif emp_status or profile.occupation:
                result.unmet_criteria.append("இத்திட்டம் வேலைவாய்ப்பற்ற இளைஞர்களுக்கானது")
            else:
                result.missing_criteria.append("வேலைவாய்ப்பு நிலை (வேலையின்மை விவரம்)")

        # 8. Evaluate Marital Status (Widow, etc.)
        marital_req = rules.get("marital_status")
        if marital_req:
            allowed_maritals = [m.lower() for m in (marital_req if isinstance(marital_req, list) else [marital_req])]
            if not profile.marital_status:
                result.missing_criteria.append(f"குடும்ப நிலை ({', '.join(allowed_maritals)})")
            else:
                user_mar = profile.marital_status.lower()
                if any(m in user_mar or user_mar in m for m in allowed_maritals):
                    result.matched_criteria.append(f"குடும்ப நிலை ({profile.marital_status}) பொருந்துகிறது")
                else:
                    result.unmet_criteria.append(f"இத்திட்டம் {', '.join(allowed_maritals)} பயனாளிகளுக்கானது")

        # 9. Evaluate Disability
        disability_rule = rules.get("disability_percentage") or rules.get("disability")
        if disability_rule:
            min_dis = disability_rule.get("min", 40) if isinstance(disability_rule, dict) else 40
            if profile.is_differently_abled is None:
                result.missing_criteria.append("மாற்றுத்திறனாளி விவரம்")
            elif not profile.is_differently_abled:
                result.unmet_criteria.append("இத்திட்டம் மாற்றுத்திறனாளிகளுக்கான பிரத்யேக உதவித்தொகை ஆகும்")
            else:
                if profile.disability_percentage is not None and profile.disability_percentage >= min_dis:
                    result.matched_criteria.append(f"மாற்றுத்திறன் அளவு ({profile.disability_percentage}%) பொருந்துகிறது")
                elif profile.disability_percentage is None:
                    result.missing_criteria.append(f"மாற்றுத்திறன் சதவீதம் (குறைந்தபட்சம் {min_dis}%)")
                else:
                    result.unmet_criteria.append(f"மாற்றுத்திறன் அளவு குறைந்தபட்சம் {min_dis}% தேவைப்படுகிறது")

        # 10. Evaluate Community (SC/ST/BC/MBC)
        community_rules = rules.get("community", ["Any"])
        if "Any" not in community_rules and len(community_rules) > 0:
            if not profile.community:
                result.missing_criteria.append(f"சமூகப் பிரிவு ({', '.join(community_rules)})")
            else:
                comm_user = profile.community.upper()
                allowed_comms = [c.upper() for c in community_rules]
                if any(c in comm_user for c in allowed_comms):
                    result.matched_criteria.append(f"சமூகப் பிரிவு ({profile.community}) பொருந்துகிறது")
                else:
                    result.unmet_criteria.append(f"இத்திட்டம் {', '.join(community_rules)} பிரிவினருக்கு மட்டுமே")

        # Determine Final Status
        if len(result.unmet_criteria) > 0:
            result.status = "NOT_APPEARING_ELIGIBLE"
            result.confidence = "HIGH"
            result.reasoning_tamil = (
                f"வழங்கப்பட்ட தகவலின்படி, நீங்கள் இத்திட்டத்தின் சில முக்கிய நிபந்தனைகளை பூர்த்தி செய்யவில்லை: "
                f"{'; '.join(result.unmet_criteria)}."
            )
            result.reasoning_english = (
                f"Based on the provided details, you do not appear eligible due to: "
                f"{'; '.join(result.unmet_criteria)}."
            )
        elif len(result.missing_criteria) > 0:
            if len(result.matched_criteria) > 0:
                result.status = "POTENTIALLY_ELIGIBLE"
                result.confidence = "MEDIUM"
                result.reasoning_tamil = (
                    f"நீங்கள் சில தகுதிகளை பூர்த்தி செய்துள்ளீர்கள் ({'; '.join(result.matched_criteria)}), "
                    f"ஆனால் இறுதி தகுதியை உறுதி செய்ய மேலும் சில விவரங்கள் தேவை: {', '.join(result.missing_criteria)}."
                )
                result.reasoning_english = (
                    f"You meet several criteria ({'; '.join(result.matched_criteria)}), "
                    f"but additional information is needed to confirm eligibility: {', '.join(result.missing_criteria)}."
                )
            else:
                result.status = "INSUFFICIENT_INFORMATION"
                result.confidence = "LOW"
                result.reasoning_tamil = (
                    f"இத்திட்டத்திற்கான உங்கள் தகுதியை கணிக்க போதிய தகவல்கள் இல்லை. "
                    f"தயவுசெய்து இந்த தகவல்களை பகிருங்கள்: {', '.join(result.missing_criteria)}."
                )
                result.reasoning_english = (
                    f"Insufficient information to evaluate this scheme. "
                    f"Please provide: {', '.join(result.missing_criteria)}."
                )
        else:
            result.status = "ELIGIBLE"
            result.confidence = "HIGH"
            result.reasoning_tamil = (
                f"அரசாணை மற்றும் வெளியிடப்பட்ட விதிகளின்படி, நீங்கள் இத்திட்டத்திற்கு முழு தகுதியுடையவராக தெரிகிறீர்கள். "
                f"(குறிப்பு: இறுதி ஒப்புதலை சம்பந்தப்பட்ட அரசுத் துறை மட்டுமே தீர்மானிக்கும்)."
            )
            result.reasoning_english = (
                f"Based on the published rules, you appear potentially eligible for this scheme. "
                f"(Note: Final approval is determined by the respective government authority)."
            )

        return result
