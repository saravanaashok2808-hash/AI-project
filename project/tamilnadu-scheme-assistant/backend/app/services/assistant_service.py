import sys
from pathlib import Path
from app.core.config import settings, BASE_DIR

from app.models.query import QueryRequest, QueryResponse, EligibilityCheckResponse
from app.models.scheme import SchemeResponse
from app.models.session import UserProfile
from app.services.scheme_service import scheme_service
from app.services.nlu_service import nlu_service
from app.eligibility.rule_evaluator import EligibilityEngine
from app.ai.llm.raw_model import llm_service
from app.ai.llm.gemini_service import gemini_service

import sys
import re
from pathlib import Path
from app.core.config import settings, BASE_DIR

from app.models.query import QueryRequest, QueryResponse, EligibilityCheckResponse
from app.models.scheme import SchemeResponse
from app.models.session import UserProfile
from app.services.scheme_service import scheme_service
from app.services.nlu_service import nlu_service
from app.eligibility.rule_evaluator import EligibilityEngine
from app.ai.llm.raw_model import llm_service
from app.ai.llm.gemini_service import gemini_service

SCHEME_ALIASES = [
    ("TN-KMUT-001", ["kmut", "magalir urimai", "மகளிர் உரிமை", "kalaignar magalir"]),
    ("TN-PUDHUMAI-002", ["pudhumai penn", "pudhumai", "புதுமைப் பெண்", "புதுமை பெண்", "penkalvi"]),
    ("TN-TAMIZHPUDHALVAN-003", ["tamizh pudhalvan", "tamil pudhalvan", "தமிழ்ப் புதல்வன்", "pudhalvan"]),
    ("TN-CMCHIS-004", ["cmchis", "medical insurance", "மருத்துவக் காப்பீடு", "மருத்துவ காப்பீடு"]),
    ("TN-FREEBUS-005", ["vidiyal payanam", "free bus", "விடியல் பயணம்", "இலவச பேருந்து"]),
    ("TN-OAP-006", ["old age pension", "முதியோர் ஓய்வூதியம்", "oap"]),
    ("TN-WIDOW-007", ["widow pension", "விதவை ஓய்வூதியம்"]),
    ("TN-DIFFABLE-008", ["diffable", "differently abled", "மாற்றுத்திறனாளி"]),
    ("TN-UZHAVAR-009", ["uzhavar", "உழவர் பாதுகாப்பு", "uzhavar pathukappu"]),
    ("TN-UNEMPLOYED-010", ["unemployed assistance", "unemployment assistance", "வேலையில்லா இளைஞர்", "வேலையில்லா உதவித்தொகை"]),
    ("TN-TAHDCO-011", ["tahdco", "தாட்கோ"]),
    ("TN-REMARRIAGE-012", ["dharmambal", "தர்மாம்பாள்", "widow remarriage", "விதவை மறுமணம்"]),
    ("TN-MAKKALAI-THEDI-013", ["makkalai thedi", "மக்களைத் தேடி"]),
    ("TN-INNUYIR-014", ["innuyir", "இன்னுயிர்", "nammai kaakkum 48", "48"]),
    ("TN-KANAVU-ILLAM-015", ["kanavu illam", "கனவு இல்லம்"]),
    ("TN-BREAKFAST-016", ["breakfast", "kaalai unavu", "காலை உணவு"]),
    ("TN-NAAN-MUDHALVAN-017", ["naan mudhalvan", "nan mudhalvan", "நான் முதல்வன்"]),
    ("TN-AABCS-018", ["aabcs", "அம்பேத்கர் தொழில்"]),
    ("TN-NEEDS-019", ["needs", "நீட்ஸ்", "new entrepreneur"]),
    ("TN-UYEGP-020", ["uyegp"]),
    ("TN-MUTHULAKSHMI-021", ["muthulakshmi", "முத்துலட்சுமி", "mrmbs", "maternity", "மகப்பேறு"]),
    ("TN-GIRLCHILD-022", ["girl child protection", "பெண் குழந்தை பாதுகாப்பு"]),
    ("TN-FIRST-GRADUATE-023", ["first graduate", "முதல் தலைமுறை"]),
    ("TN-FREE-LAPTOP-024", ["free laptop", "laptop", "மடிக்கணினி"]),
    ("TN-CROP-INSURANCE-PMFBY-052", ["crop insurance", "pmfby", "பயிர் காப்பீடு"]),
    ("TN-FISHERMEN-LEAN-RELIEF-055", ["fishermen", "மீன்பிடி தடைக்காலம்"]),
    ("TN-ILLAM-THEDI-KALVI-027", ["illam thedi kalvi", "இல்லம் தேடிக் கல்வி"]),
    ("TN-KALLOORI-KANAVU-028", ["kalloori kanavu", "கல்லூரி கனவு"])
]

class AssistantService:
    async def process_query(self, request: QueryRequest) -> QueryResponse:
        language = request.language or nlu_service.detect_language(request.query)
        intent = nlu_service.classify_intent(request.query)
        entities = nlu_service.extract_entities(request.query)

        # Build user profile from entities or request.profile_updates
        profile_data = request.profile_updates or {}
        profile_data.update(entities)
        profile = UserProfile(**profile_data)

        # Search schemes based on query and enriched profile
        filters = {}
        raw_schemes = await scheme_service.search_schemes(request.query, filters, profile=profile)
        
        schemes = []
        eligibility_summaries = []
        official_sources = []
        
        status_priority = {
            "ELIGIBLE": 0,
            "POTENTIALLY_ELIGIBLE": 1,
            "INSUFFICIENT_INFORMATION": 2,
            "NOT_APPEARING_ELIGIBLE": 3
        }

        query_lower = request.query.lower()
        q_words = [w for w in re.findall(r'[\w\u0B80-\u0BFF]+', query_lower) if len(w) > 3]

        evaluated_pairs = []
        for idx, scheme_dict in enumerate(raw_schemes):
            eval_result = EligibilityEngine.evaluate(profile, scheme_dict)
            
            scheme_response = SchemeResponse(**scheme_dict)
            scheme_response.eligibility_status = eval_result.status
            scheme_response.matched_criteria = eval_result.matched_criteria
            scheme_response.unmet_criteria = eval_result.unmet_criteria
            scheme_response.missing_criteria = eval_result.missing_criteria
            
            elig_summary = EligibilityCheckResponse(
                scheme_id=scheme_response.scheme_id,
                status=eval_result.status,
                matched_criteria=eval_result.matched_criteria,
                unmet_criteria=eval_result.unmet_criteria,
                missing_criteria=eval_result.missing_criteria,
                reasoning_tamil=eval_result.reasoning_tamil,
                reasoning_english=eval_result.reasoning_english,
                confidence=eval_result.confidence
            )
            
            sid = scheme_response.scheme_id
            name_en = scheme_response.scheme_name_english.lower()
            name_ta = scheme_response.scheme_name_tamil.lower()
            cat = (scheme_response.category or "").lower()

            # 1. Scheme Name & Alias Matching Bonus
            name_bonus = 0
            for target_sid, aliases in SCHEME_ALIASES:
                if sid == target_sid and any(a in query_lower for a in aliases):
                    name_bonus += 80
                    break

            for w in q_words:
                if w in name_en or w in name_ta:
                    name_bonus += 25

            # 2. Domain relevance bonus for broad category terms
            domain_bonus = 0
            rel_keywords = [
                ("loan", ["loan", "கடன்", "subsidy", "மானியம்", "லோன்", "uyegp", "needs"]),
                ("business", ["business", "தொழில்", "entrepreneur", "enterprise", "சுயதொழில்", "வியாபாரம்"]),
                ("job", ["job", "வேலை", "employment", "unemployed", "முதல்வன்", "வேலைவாய்ப்பு", "வேலையில்லா"]),
                ("pension", ["pension", "ஓய்வூதியம்", "முதியோர்", "பென்ஷன்"]),
                ("college", ["college", "கல்லூரி", "student", "மாணவர்", "படிப்பு", "பட்டதாரி", "கல்வி", "scholarship"]),
                ("women", ["women", "மகள்", "பெண்", "மகளிர்", "தாய்", "விதவை", "உரிமைத்தொகை", "புதுமைப் பெண்"]),
                ("farmer", ["farmer", "விவசாயி", "வேளாண்", "பயிர்", "உழவர்", "agriculture"]),
                ("medical", ["medical", "health", "மருத்துவம்", "காப்பீடு", "சிகிச்சை", "hospital"]),
                ("disabled", ["disabled", "மாற்றுத்திறனாளி", "ஊனம்"]),
            ]
            for kw, related_terms in rel_keywords:
                if any(k in query_lower for k in related_terms):
                    if any(t in name_en or t in name_ta or t in cat for t in related_terms):
                        domain_bonus += 15
            
            # 3. Intent-aware status weighting
            if intent == "check_eligibility":
                status_mult = 10
            else:
                status_mult = 2  # Don't penalize queried schemes on informational questions

            status_weight = status_priority.get(eval_result.status, 2)
            # Final ranking score: lower is better.
            final_score = (status_weight * status_mult) - name_bonus - domain_bonus + (idx * 2)
            evaluated_pairs.append((final_score, scheme_response, elig_summary))

        # Sort so the most query-relevant and eligible schemes always appear at the top
        evaluated_pairs.sort(key=lambda x: x[0])

        for _, scheme_resp, elig_sum in evaluated_pairs[:6]:
            schemes.append(scheme_resp)
            eligibility_summaries.append(elig_sum)
            for url in scheme_resp.official_urls:
                official_sources.append({"name": scheme_resp.scheme_name_english, "url": url})

        is_tamil = language in ["ta", "tamil", "ta-en"]
        lang_name = "Tamil" if is_tamil else "English"

        # 1. First attempt generation with Google Gemini AI API if configured
        gemini_response = None
        custom_key = getattr(request, "gemini_api_key", None)
        conv_history = getattr(request, "history", None)
        if gemini_service.is_configured(custom_key):
            try:
                schemes_data = [s.model_dump() for s in schemes]
                elig_data = [e.model_dump() for e in eligibility_summaries]
                gemini_response = await gemini_service.generate_response(
                    query=request.query,
                    user_profile=profile_data,
                    schemes=schemes_data,
                    eligibility_summaries=elig_data,
                    detected_language=lang_name,
                    detected_intent=intent,
                    custom_api_key=custom_key,
                    conversation_history=conv_history
                )
            except Exception:
                pass

        # 2. Local schema-aware RAG QA Generator (bilingual)
        fallback_data = gemini_service.generate_smart_fallback(
            query=request.query,
            user_profile=profile_data,
            schemes=[s.model_dump() for s in schemes],
            detected_language=language,
            detected_intent=intent,
            conversation_history=conv_history
        )

        if gemini_response:
            if is_tamil:
                response_text_tamil = gemini_response
                response_text_english = fallback_data.get("english", gemini_response)
            else:
                response_text_english = gemini_response
                response_text_tamil = fallback_data.get("tamil", gemini_response)
        else:
            response_text_tamil = fallback_data.get("tamil", "")
            response_text_english = fallback_data.get("english", "")

        # Missing prompts calculation
        missing_prompts = []
        if intent == "check_eligibility" and eligibility_summaries:
            all_missing = set()
            for e in eligibility_summaries:
                if e.status in ["POTENTIALLY_ELIGIBLE", "INSUFFICIENT_INFORMATION"]:
                    for m in e.missing_criteria:
                        all_missing.add(m)
            missing_prompts = list(all_missing)

        return QueryResponse(
            response_text_tamil=response_text_tamil,
            response_text_english=response_text_english,
            detected_language=language,
            detected_intent=intent,
            extracted_entities=entities,
            schemes=schemes,
            eligibility_summaries=eligibility_summaries,
            missing_info_prompts=missing_prompts,
            official_sources=official_sources
        )

assistant_service = AssistantService()
