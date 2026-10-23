import logging
import asyncio
import json
import re
from typing import Optional, List, Dict, Any, Union
import httpx
from app.core.config import settings

logger = logging.getLogger(__name__)

class GeminiService:
    def __init__(self):
        self.active_model: Optional[str] = None
        self.api_version: str = "v1beta"

    def get_api_key(self, custom_key: Optional[str] = None) -> Optional[str]:
        if custom_key and custom_key.strip():
            return custom_key.strip()
        if settings.GEMINI_API_KEY and settings.GEMINI_API_KEY.strip():
            return settings.GEMINI_API_KEY.strip()
        return None

    def is_configured(self, custom_key: Optional[str] = None) -> bool:
        return bool(self.get_api_key(custom_key))

    async def discover_best_model(self, api_key: str) -> str:
        """
        Dynamically calls ModelService.ListModels on the user's API key
        to determine exactly which model Google AI Studio has enabled.
        """
        preferred = [
            "gemini-2.0-flash",
            "gemini-2.5-flash",
            "gemini-1.5-flash",
            "gemini-1.5-flash-latest",
            "gemini-1.5-flash-002",
            "gemini-1.5-flash-001",
            "gemini-2.0-flash-lite",
            "gemini-1.5-pro",
            "gemini-pro"
        ]

        for ver in ["v1beta", "v1"]:
            try:
                url = f"https://generativelanguage.googleapis.com/{ver}/models?key={api_key}"
                async with httpx.AsyncClient(timeout=7.0) as client:
                    res = await client.get(url)
                    if res.status_code == 200:
                        data = res.json()
                        available = []
                        for m in data.get("models", []):
                            methods = m.get("supportedGenerationMethods", [])
                            if "generateContent" in methods:
                                name = m.get("name", "").replace("models/", "")
                                available.append(name)
                        
                        for pref in preferred:
                            if pref in available:
                                self.active_model = pref
                                self.api_version = ver
                                logger.info(f"Auto-selected working Gemini model: {pref} on API {ver}")
                                return pref
                        
                        flash_models = [m for m in available if "flash" in m]
                        if flash_models:
                            self.active_model = flash_models[0]
                            self.api_version = ver
                            return flash_models[0]

                        gemini_models = [m for m in available if "gemini" in m]
                        if gemini_models:
                            self.active_model = gemini_models[0]
                            self.api_version = ver
                            return gemini_models[0]
            except Exception as e:
                logger.warning(f"Error querying {ver}/models: {e}")
                continue

        # Default fallback
        self.active_model = "gemini-2.0-flash"
        self.api_version = "v1beta"
        return "gemini-2.0-flash"

    async def generate_response(
        self,
        query: str,
        user_profile: Dict[str, Any],
        schemes: List[Dict[str, Any]],
        eligibility_summaries: List[Dict[str, Any]],
        detected_language: str,
        detected_intent: str,
        custom_api_key: Optional[str] = None,
        conversation_history: Optional[List[Dict[str, Any]]] = None
    ) -> Optional[str]:
        api_key = self.get_api_key(custom_api_key)
        if not api_key:
            logger.info("Gemini API key not configured. Using contextual helper engine.")
            return None

        # Build comprehensive schemes context for Gemini
        schemes_info = []
        for s, e in zip(schemes, eligibility_summaries):
            name_en = s.get("scheme_name_english", "")
            name_ta = s.get("scheme_name_tamil", "")
            dept = s.get("department", "")
            desc = s.get("description_english", "") or s.get("description_tamil", "")
            status = e.get("status", "POTENTIALLY_ELIGIBLE")
            benefits = s.get("benefits", {})
            rules = s.get("eligibility_rules", {})
            docs = s.get("required_documents", [])
            steps = s.get("application_steps", [])
            urls = s.get("official_urls", [])
            helpline = s.get("contact_helpline", "CM Helpline 1100")
            
            schemes_info.append(
                f"- Scheme: {name_en} ({name_ta})\n"
                f"  Department: {dept}\n"
                f"  Description: {desc}\n"
                f"  Eligibility Status for Citizen: {status}\n"
                f"  Eligibility Rules (Age, Gender, Income Limit, Conditions): {json.dumps(rules, ensure_ascii=False)}\n"
                f"  Official Benefits (Amounts, Subsidies, DBT): {json.dumps(benefits, ensure_ascii=False)}\n"
                f"  Required Documents: {', '.join(docs) if isinstance(docs, list) else str(docs)}\n"
                f"  Application Steps: {' -> '.join(steps) if isinstance(steps, list) else str(steps)}\n"
                f"  Official Portals: {', '.join(urls) if isinstance(urls, list) else str(urls)}\n"
                f"  Helpline: {helpline}"
            )

        schemes_block = "\n\n".join(schemes_info) if schemes_info else "No specific schemes matched yet."
        profile_str = ", ".join([f"{k}: {v}" for k, v in user_profile.items() if v]) or "Citizen details in progress"

        system_instruction = (
            "You are 'Arasu Nanban' (அரசு நண்பன் / Government Friend), the authoritative, warm, caring, and highly accurate AI companion for Tamil Nadu Government welfare schemes. "
            "You speak like an affectionate, encouraging elder sibling or trusted friend sitting right next to the citizen.\n\n"
            "CRITICAL CONVERSATIONAL & FACTUAL RULES:\n"
            "1. STRICT FACTUAL ACCURACY GROUNDED IN OFFICIAL DATA:\n"
            "   - Base all answers on the provided evaluated schemes. Never invent or hallucinate scheme names, eligibility criteria, or benefit amounts.\n"
            "   - When answering about amounts (e.g., Kalaignar Magalir Urimai Thogai = ₹1,000/mo, Pudhumai Penn = ₹1,000/mo, CMCHIS = up to ₹5,00,000, UYEGP = 25% subsidy, NEEDS = 25% subsidy up to ₹75L, Muthulakshmi Reddy = ₹18,000 total across stages), state exact figures clearly.\n"
            "   - When answering about eligibility, state the exact age range, family income ceiling (e.g. ₹2.5 Lakhs for KMUT, ₹1.2 Lakhs for CMCHIS, ₹5 Lakhs for UYEGP), and schooling requirements (e.g. 6th-12th in TN Govt Schools for Pudhumai Penn and Tamizh Pudhalvan).\n"
            "2. DIRECT ANSWERS WITHOUT ROBOTIC CANNED REPETITION:\n"
            "   - Directly answer the citizen's specific question first without repetitive greeting rituals.\n"
            "   - If asking for documents, list the exact required documents clearly.\n"
            "   - If asking how to apply, give the step-by-step procedure and official web link.\n"
            "   - If asking 'which is best', compare the top options with clear justification.\n"
            "3. LANGUAGE ADAPTABILITY:\n"
            "   - If user asks in Tanglish, reply in warm, friendly conversational Tamil or natural Tanglish.\n"
            "   - If user asks in Tamil script, reply in polite, warm spoken Tamil.\n"
            "   - If user asks in English, reply in friendly, helpful English.\n"
        )

        user_content = (
            f"Citizen Profile:\n{profile_str}\n\n"
            f"Evaluated Schemes Ground Truth Facts:\n{schemes_block}\n\n"
            f"Citizen's Query: \"{query}\"\n"
            f"Detected Intent: {detected_intent}\n"
            f"Detected Language: {detected_language}\n\n"
            "Please respond warmly to the citizen, directly answering their query with empathy, accuracy, and encouragement."
        )

        if not self.active_model:
            await self.discover_best_model(api_key)

        model = self.active_model or "gemini-2.0-flash"
        ver = self.api_version or "v1beta"
        endpoint = f"https://generativelanguage.googleapis.com/{ver}/models/{model}:generateContent?key={api_key}"

        contents = []
        if conversation_history:
            last_role = None
            for item in conversation_history[-6:]:
                raw_role = item.get("role", "user")
                role = "user" if raw_role in ["user", "citizen"] else "model"
                text = item.get("content") or item.get("text", "")
                if not text or not str(text).strip():
                    continue
                clean_text = str(text).strip()
                if role == last_role and contents:
                    contents[-1]["parts"].append({"text": clean_text})
                else:
                    contents.append({"role": role, "parts": [{"text": clean_text}]})
                    last_role = role

        if contents and contents[-1]["role"] == "user":
            contents.append({"role": "model", "parts": [{"text": "Understood. Please ask your next question."}]})

        contents.append({"role": "user", "parts": [{"text": user_content}]})

        payload = {
            "system_instruction": {
                "parts": [{"text": system_instruction}]
            },
            "contents": contents,
            "generationConfig": {
                "temperature": 0.5,
                "topP": 0.9,
                "maxOutputTokens": 700
            }
        }

        for attempt in range(2):
            try:
                async with httpx.AsyncClient(timeout=15.0) as client:
                    res = await client.post(endpoint, json=payload)
                    if res.status_code == 200:
                        data = res.json()
                        candidates = data.get("candidates", [])
                        if candidates:
                            parts = candidates[0].get("content", {}).get("parts", [])
                            if parts and "text" in parts[0]:
                                text = parts[0]["text"].strip()
                                logger.info(f"Gemini AI ({model}) generated response successfully ({len(text)} chars).")
                                return text
                    elif res.status_code in [429, 503]:
                        logger.warning(f"Gemini API rate limit/busy ({res.status_code}), waiting 1s...")
                        await asyncio.sleep(1.0)
                        continue
                    elif res.status_code == 404:
                        new_model = await self.discover_best_model(api_key)
                        if new_model != model:
                            model = new_model
                            endpoint = f"https://generativelanguage.googleapis.com/{self.api_version}/models/{new_model}:generateContent?key={api_key}"
                            continue
                    else:
                        logger.warning(f"Gemini API returned status {res.status_code}: {res.text[:200]}")
            except Exception as e:
                logger.warning(f"Error calling Gemini API: {e}")

        return None

    # -------------------------------------------------------------
    # HIGH-ACCURACY SCHEMA-AWARE LOCAL RAG QA GENERATOR
    # -------------------------------------------------------------
    @staticmethod
    def _extract_facts(s: Dict[str, Any]) -> Dict[str, Any]:
        """Safely extract and decode all structured columns from a scheme dictionary."""
        def parse_json(val, default):
            if isinstance(val, (dict, list)):
                return val
            if isinstance(val, str):
                try:
                    return json.loads(val)
                except Exception:
                    return default
            return default

        return {
            "id": s.get("scheme_id", ""),
            "name_en": s.get("scheme_name_english", ""),
            "name_ta": s.get("scheme_name_tamil", ""),
            "dept": s.get("department", "Tamil Nadu Government"),
            "dept_ta": s.get("department_tamil", "தமிழ்நாடு அரசு"),
            "cat": s.get("category", ""),
            "desc_en": s.get("description_english", ""),
            "desc_ta": s.get("description_tamil", ""),
            "benefits": parse_json(s.get("benefits"), {}),
            "rules": parse_json(s.get("eligibility_rules"), {}),
            "docs": parse_json(s.get("required_documents"), []),
            "steps": parse_json(s.get("application_steps"), []),
            "urls": parse_json(s.get("official_urls"), []),
            "helpline": s.get("contact_helpline") or "CM Helpline 1100"
        }

    @staticmethod
    def _format_benefits_str(b: Dict[str, Any], is_ta: bool = False) -> str:
        if not b:
            return "மாதாந்திர நிதி உதவித்தொகை மற்றும் அரசு நலச் சலுகைகள்" if is_ta else "Direct financial assistance and welfare benefits"
        
        labels_ta = {
            "financial_support": "நிதி உதவித்தொகை",
            "financial_assistance": "நிதி உதவி",
            "insurance_coverage": "மருத்துவக் காப்பீடு",
            "capital_subsidy": "அரசு மூலதன மானியம்",
            "interest_subvention": "வட்டி மானியம்",
            "nutrition_kits": "ஊட்டச்சத்து பெட்டகம்",
            "total_value": "மொத்த உதவி மதிப்பு",
            "mode": "வழங்கும் முறை",
            "frequency": "வழங்கும் கால இடைவெளி",
            "stipend": "மாதாந்திர உதவித்தொகை",
            "covered_procedures": "சிகிச்சைகள் வரம்பு",
            "project_size": "திட்ட மதிப்பீடு வரம்பு",
            "sslc_passed": "10-ஆம் வகுப்பு தேர்ச்சி பெற்றோர்",
            "sslc_failed": "10-ஆம் வகுப்பு தேர்ச்சி பெறாதோர்",
            "hsc_passed": "12-ஆம் வகுப்பு தேர்ச்சி பெற்றோர்",
            "graduates_postgraduates": "பட்டதாரிகள் & முதுகலை",
            "payment_cycle": "பரிமாற்ற முறை"
        }
        lines = []
        for k, v in b.items():
            if is_ta:
                lbl = labels_ta.get(k, k.replace("_", " ").title())
                lines.append(f"• **{lbl}**: {v}")
            else:
                lbl = k.replace("_", " ").title()
                lines.append(f"• **{lbl}**: {v}")
        return "\n".join(lines)

    @staticmethod
    def _format_eligibility_str(rules: Dict[str, Any], is_ta: bool = False) -> str:
        if not rules:
            return "தமிழ்நாடு வாழ் அனைத்து குடிமக்களும் விண்ணப்பிக்கலாம்" if is_ta else "Open to all eligible residents of Tamil Nadu"

        lines = []
        # Age
        age = rules.get("age")
        if age and isinstance(age, dict):
            min_a = age.get("min")
            max_a = age.get("max")
            if min_a or max_a:
                if is_ta:
                    lines.append(f"• **வயது வரம்பு**: {min_a or 0} முதல் {max_a or 'வரம்பில்லை'} வயது வரை")
                else:
                    lines.append(f"• **Age Limit**: {min_a or 0} to {max_a or 'No upper limit'} years")

        # Gender
        gender = rules.get("gender")
        if gender and isinstance(gender, list) and "Any" not in gender:
            if "Female" in gender and "Transgender" in gender:
                g_ta = "பெண்கள் மற்றும் திருநங்கைகள்"
            elif "Female" in gender:
                g_ta = "பெண்கள் மட்டும்"
            elif "Male" in gender:
                g_ta = "ஆண்கள் மட்டும்"
            else:
                g_ta = ", ".join(gender)
            lines.append(f"• **பாலினம்**: {g_ta}" if is_ta else f"• **Gender**: {', '.join(gender)}")

        # Income Limit
        income = rules.get("income_limit_annual")
        if income:
            if is_ta:
                lines.append(f"• **வருமான வரம்பு**: குடும்ப ஆண்டு வருமானம் ₹{income:,} -க்கு மிகாமல் இருக்க வேண்டும்")
            else:
                lines.append(f"• **Income Ceiling**: Annual family income must not exceed ₹{income:,}")

        # Schooling requirement
        schooling = rules.get("schooling_requirement")
        if schooling:
            if is_ta:
                lines.append(f"• **பள்ளிப் படிப்பு**: {schooling}")
            else:
                lines.append(f"• **Schooling**: {schooling}")

        # Education
        edu = rules.get("education_level") or rules.get("education")
        if edu:
            edu_str = ", ".join(edu) if isinstance(edu, list) else str(edu)
            lines.append(f"• **கல்வித் தகுதி**: {edu_str}" if is_ta else f"• **Education**: {edu_str}")

        # Special conditions
        conditions = rules.get("special_conditions", [])
        if conditions and isinstance(conditions, list):
            lines.append("• **முக்கிய நிபந்தனைகள்**:" if is_ta else "• **Key Conditions**:")
            for c in conditions[:4]:
                lines.append(f"   - {c}")

        return "\n".join(lines) if lines else ("தமிழ்நாடு வசிப்பிடம்" if is_ta else "Tamil Nadu residence required")

    @staticmethod
    def _format_documents_str(docs: List[str], is_ta: bool = False) -> str:
        if not docs:
            return "• ஆதார் அட்டை\n• குடும்ப அட்டை (Smart Ration Card)\n• வருமானச் சான்றிதழ்" if is_ta else "• Aadhaar Card\n• Smart Ration Card\n• Income Certificate"
        lines = [f"• {doc}" for doc in docs]
        return "\n".join(lines)

    @staticmethod
    def _format_steps_str(steps: List[str], urls: List[str], helpline: str, is_ta: bool = False) -> str:
        lines = []
        if steps:
            for s in steps:
                lines.append(f"{s}" if s.strip().startswith(("1.", "2.", "3.", "4.", "5.")) else f"• {s}")
        else:
            lines.append("1. அதிகாரப்பூர்வ இணையதளம் அல்லது இ-சேவை மையத்தை அணுகவும்" if is_ta else "1. Visit the official portal or your nearest e-Sevai center")
            lines.append("2. தேவையான ஆவணங்களுடன் விண்ணப்பத்தை சமர்ப்பிக்கவும்" if is_ta else "2. Submit application form with required verified documents")
            lines.append("3. சரிபார்ப்புக்குப் பின் வங்கி கணக்கில் உதவித்தொகை வரவு வைக்கப்படும்" if is_ta else "3. Assistance credited directly to bank account after departmental verification")

        portal = urls[0] if urls else "https://www.tn.gov.in"
        lines.append("")
        lines.append(f"🌐 **அதிகாரப்பூர்வ இணையதளம்**: {portal}" if is_ta else f"🌐 **Official Portal**: {portal}")
        if helpline:
            lines.append(f"📞 **உதவி எண் (Helpline)**: {helpline}" if is_ta else f"📞 **Official Helpline**: {helpline}")
        return "\n".join(lines)

    def generate_smart_fallback(
        self,
        query: str,
        user_profile: Dict[str, Any],
        schemes: List[Dict[str, Any]],
        detected_language: str,
        detected_intent: str,
        conversation_history: Optional[List[Dict[str, Any]]] = None
    ) -> Dict[str, str]:
        """
        Generates authoritative, fact-grounded responses in both Tamil and English
        using exact structured facts from the matched schemes.
        """
        q_lower = query.lower().strip()
        q_tokens = set(re.findall(r"[\w\u0B80-\u0BFF]+", q_lower))
        citizen_name = user_profile.get("name") or "நண்பா"
        citizen_name_en = user_profile.get("name") or "Friend"
        age = user_profile.get("age") or 24
        edu = user_profile.get("education_level") or "Graduate"

        # 1. Standalone Greeting Detection (strictly word boundaries)
        greeting_words = {"hi", "hello", "hey", "vanakkam", "வணக்கம்", "வணக்கம்!", "ஹாய்", "namaste"}
        if (q_tokens & greeting_words) and len(q_tokens) <= 3:
            ta = (
                f"வணக்கம் {citizen_name}! நான் தமிழ்நாடு அரசு நலத்திட்டங்களுக்கான உங்கள் AI வழிகாட்டி 'அரசு நண்பன்'. "
                f"உங்களுக்கான உதவித்தொகை, கல்விச் சலுகைகள், மருத்துவக் காப்பீடு, மகளிர் திட்டங்கள் மற்றும் தொழில் மானியக் கடன்கள் "
                f"பற்றிய துல்லியமான தகவல்களை வழங்க நான் காத்திருக்கிறேன். உங்களுக்கு எந்த திட்டம் குறித்து அறிய வேண்டும்?"
            )
            en = (
                f"Hello {citizen_name_en}! I am 'Arasu Nanban', your official AI guide for Tamil Nadu Government welfare schemes. "
                f"I can provide accurate details on monthly assistance, student scholarships, healthcare insurance, women welfare, "
                f"and subsidized business loans. How may I assist you today?"
            )
            return {"tamil": ta, "english": en}

        # Check if schemes were retrieved
        if not schemes:
            ta = (
                f"நண்பா, '{query}' தொடர்பான துல்லியமான தகவல்களைத் தேடுகிறேன். "
                f"கீழே உள்ள தேடல் பகுதியில் உங்கள் வயது, படிப்பு அல்லது தேவைப்படும் உதவியைக் குறிப்பிட்டால், "
                f"பொருத்தமான தமிழ்நாடு அரசு நலத்திட்டங்களை உடனடியாகப் பார்க்கலாம்!"
            )
            en = (
                f"I am searching for schemes matching '{query}'. "
                f"Please refine your query with your age, education, or specific requirement to view matching official Tamil Nadu Government schemes."
            )
            return {"tamil": ta, "english": en}

        top_s = self._extract_facts(schemes[0])
        top_name_ta = top_s["name_ta"] or top_s["name_en"]
        top_name_en = top_s["name_en"] or top_s["name_ta"]

        second_s = self._extract_facts(schemes[1]) if len(schemes) > 1 else None

        # 2. Comparison: "ithula ethu best?" / "which is best" / "recommend"
        if any(w in q_lower for w in ["best", "ethu best", "edhu best", "which is best", "nalladhu", "mukkiyam", "first ethu", "recommend", "பரிந்துரை"]):
            if second_s:
                sec_name_ta = second_s["name_ta"] or second_s["name_en"]
                sec_name_en = second_s["name_en"] or second_s["name_ta"]
                ta = (
                    f"நண்பா, உங்கள் நிலைக்கு மேலே உள்ளவற்றில் **{top_name_ta}** மற்றும் **{sec_name_ta}** ஆகிய இரண்டும் மிகச் சிறந்த திட்டங்கள்!\n\n"
                    f"📌 **முதல் முன்னுரிமை**: **{top_name_ta}**\n"
                    f"{self._format_benefits_str(top_s['benefits'], is_ta=True)}\n\n"
                    f"📌 **அடுத்த வாய்ப்பு**: **{sec_name_ta}**\n"
                    f"{self._format_benefits_str(second_s['benefits'], is_ta=True)}\n\n"
                    f"முதலில் **{top_name_ta}** திட்டத்திற்கு விண்ணப்பிக்கப் பரிந்துரைக்கிறேன். தேவையான ஆவணங்களை கீழே உள்ள கார்டில் சரிபார்த்து உடனே பயன்பெறுங்கள்!"
                )
                en = (
                    f"Based on your profile, the two top recommendations are **{top_name_en}** and **{sec_name_en}**.\n\n"
                    f"📌 **Top Priority**: **{top_name_en}**\n"
                    f"{self._format_benefits_str(top_s['benefits'], is_ta=False)}\n\n"
                    f"📌 **Alternative Option**: **{sec_name_en}**\n"
                    f"{self._format_benefits_str(second_s['benefits'], is_ta=False)}\n\n"
                    f"We recommend applying for **{top_name_en}** first for immediate benefits. Review the required documents on the card below to proceed."
                )
            else:
                ta = (
                    f"நண்பா, உங்கள் விவரங்களுக்கு **{top_name_ta}** திட்டம் தான் மிகச் சிறந்தது!\n\n"
                    f"📌 **வழங்கப்படும் பலன்**:\n"
                    f"{self._format_benefits_str(top_s['benefits'], is_ta=True)}\n\n"
                    f"கீழே உள்ள கார்டில் ஆவணங்களைச் சரிபார்த்து உடனடியாக விண்ணப்பிக்கலாம்!"
                )
                en = (
                    f"**{top_name_en}** is the most optimal scheme for your current profile.\n\n"
                    f"📌 **Key Benefits**:\n"
                    f"{self._format_benefits_str(top_s['benefits'], is_ta=False)}\n\n"
                    f"Check the required documents in the card below to initiate your application."
                )
            return {"tamil": ta, "english": en}

        # 3. Helpline / Contact Inquiry
        if detected_intent == "helpline_inquiry" or any(w in q_lower for w in ["helpline", "toll free", "tollfree", "phone", "contact", "call", "ஹெல்ப்லைன்", "தொலைபேசி", "எண்"]):
            ta = (
                f"நண்பா, **{top_name_ta}** ({top_name_en}) திட்டத்திற்கான அதிகாரப்பூர்வ தொடர்பு விவரங்கள்:\n\n"
                f"📞 **உதவி எண் (Helpline)**: {top_s['helpline']}\n"
                f"🌐 **அதிகாரப்பூர்வ தளம்**: {top_s['urls'][0] if top_s['urls'] else 'https://www.tn.gov.in'}\n"
                f"🏛️ **நிர்வாகத் துறை**: {top_s['dept_ta'] or top_s['dept']}\n\n"
                f"விண்ணப்ப நிலை மற்றும் சந்தேகங்களுக்கு இந்த உதவி எண்ணை அலுவலக வேலை நாட்களில் தொடர்பு கொள்ளலாம்."
            )
            en = (
                f"Official contact and helpline details for **{top_name_en}** ({top_name_ta}):\n\n"
                f"📞 **Official Helpline**: {top_s['helpline']}\n"
                f"🌐 **Official Portal**: {top_s['urls'][0] if top_s['urls'] else 'https://www.tn.gov.in'}\n"
                f"🏛️ **Department**: {top_s['dept']}\n\n"
                f"You can reach out to this helpline during working hours for application status and grievance redressal."
            )
            return {"tamil": ta, "english": en}

        # 4. Required Documents Inquiry
        if detected_intent == "documents_required" or any(w in q_lower for w in [
            "documents", "document", "proof", "proofs", "certificate", "certificates",
            "ஆவணங்கள்", "ஆவணம்", "சான்றிதழ்", "சான்றிதழ்கள்", "theva", "aavanangal", "டாக்குமெண்ட்", "சர்டிபிகேட்"
        ]):
            ta = (
                f"நண்பா, **{top_name_ta}** ({top_name_en}) திட்டத்திற்கு விண்ணப்பிக்கத் தேவையான அதிகாரப்பூர்வ ஆவணங்கள்:\n\n"
                f"{self._format_documents_str(top_s['docs'], is_ta=True)}\n\n"
                f"🌐 **விண்ணப்பிக்கும் இணையதளம்**: {top_s['urls'][0] if top_s['urls'] else 'https://www.tn.gov.in'}\n"
                f"📞 **உதவி எண்**: {top_s['helpline']}\n\n"
                f"இந்த ஆவணங்களை தயார் செய்து கொண்டு அருகிலுள்ள இ-சேவை மையம் அல்லது அதிகாரப்பூர்வ தளம் வழியாக விண்ணப்பிக்கலாம்!"
            )
            en = (
                f"Required official documents to apply for **{top_name_en}** ({top_name_ta}):\n\n"
                f"{self._format_documents_str(top_s['docs'], is_ta=False)}\n\n"
                f"🌐 **Official Portal**: {top_s['urls'][0] if top_s['urls'] else 'https://www.tn.gov.in'}\n"
                f"📞 **Helpline**: {top_s['helpline']}\n\n"
                f"Ensure you have original and scanned copies ready when applying via your nearest e-Sevai centre or online."
            )
            return {"tamil": ta, "english": en}

        # 5. Benefits / Financial / Subsidy Amount Inquiry
        if detected_intent == "benefits_inquiry" or any(w in q_lower for w in [
            "how much", "amount", "money", "panam", "stipend", "subsidy", "evalavu", "evlo",
            "kadan evlo", "panam evlo", "ரூபாய்", "தொகை", "மானியம்", "எவ்வளவு", "நிதி உதவி",
            "coverage", "assistance amount", "benefit", "பலன்", "சலுகை"
        ]):
            ta = (
                f"நண்பா, **{top_name_ta}** ({top_name_en}) திட்டத்தின் கீழ் தமிழ்நாடு அரசு வழங்கும் அதிகாரப்பூர்வ சலுகைகள்:\n\n"
                f"{self._format_benefits_str(top_s['benefits'], is_ta=True)}\n\n"
                f"🌐 **அதிகாரப்பூர்வ தளம்**: {top_s['urls'][0] if top_s['urls'] else 'https://www.tn.gov.in'}\n"
                f"📞 **உதவி எண்**: {top_s['helpline']}\n\n"
                f"அனைத்து நிதி உதவிகளும் பயனாளியின் ஆதார் இணைக்கப்பட்ட வங்கிக் கணக்கில் நேரடியாக (DBT) செலுத்தப்படும்."
            )
            en = (
                f"Official benefits provided under **{top_name_en}** ({top_name_ta}) by the Tamil Nadu Government:\n\n"
                f"{self._format_benefits_str(top_s['benefits'], is_ta=False)}\n\n"
                f"🌐 **Official Portal**: {top_s['urls'][0] if top_s['urls'] else 'https://www.tn.gov.in'}\n"
                f"📞 **Helpline**: {top_s['helpline']}\n\n"
                f"Financial support is disbursed directly to the beneficiary's Aadhaar-linked bank account via DBT."
            )
            return {"tamil": ta, "english": en}

        # 6. Eligibility / Rules / Income Limit / Age Inquiry
        if detected_intent == "check_eligibility" or any(w in q_lower for w in [
            "who is eligible", "eligibility", "eligible", "income limit", "age limit", "qualification",
            "தகுதி", "விதிகள்", "யாருக்கு கிடைக்கும்", "kedaikuma", "kedaikkuma", "kedakkuma", "rules",
            "varuma", "mudiyuma", "can i get", "am i eligible", "eligibility enna"
        ]):
            ta = (
                f"நண்பா, **{top_name_ta}** ({top_name_en}) திட்டத்திற்கான அதிகாரப்பூர்வ தகுதி வரம்புகள்:\n\n"
                f"{self._format_eligibility_str(top_s['rules'], is_ta=True)}\n\n"
                f"📌 **தேவையான முக்கிய ஆவணங்கள்**:\n"
                f"{self._format_documents_str(top_s['docs'][:3], is_ta=True)}\n\n"
                f"கீழே உள்ள கார்டில் உங்கள் தகுதிப் பொருத்தத்தை (Matched Criteria) பார்த்து உடனடியாக விண்ணப்பிக்கலாம்!"
            )
            en = (
                f"Official eligibility criteria for **{top_name_en}** ({top_name_ta}):\n\n"
                f"{self._format_eligibility_str(top_s['rules'], is_ta=False)}\n\n"
                f"📌 **Essential Documents**:\n"
                f"{self._format_documents_str(top_s['docs'][:3], is_ta=False)}\n\n"
                f"Review your evaluated eligibility status in the card below to initiate your application."
            )
            return {"tamil": ta, "english": en}

        # 7. Application Process / How to Apply
        if detected_intent == "application_process" or any(w in q_lower for w in [
            "how to apply", "steps to apply", "application process", "where to apply",
            "விண்ணப்பிக்க", "விண்ணப்பிப்பது எப்படி", "epdi apply", "eppadi apply",
            "vinnappikka", "வழிமுறை", "அப்ளிகேஷன் முறை", "apply online", "apply panrathu"
        ]):
            ta = (
                f"நண்பா, **{top_name_ta}** ({top_name_en}) திட்டத்திற்கு விண்ணப்பிக்கும் நேரடி வழிமுறைகள்:\n\n"
                f"{self._format_steps_str(top_s['steps'], top_s['urls'], top_s['helpline'], is_ta=True)}\n\n"
                f"அருகிலுள்ள அரசு இ-சேவை மையம் மூலமாகவும் அல்லது கார்டில் உள்ள இணைப்பை கிளிக் செய்தும் விண்ணப்பிக்கலாம்!"
            )
            en = (
                f"Step-by-step instructions to apply for **{top_name_en}** ({top_name_ta}):\n\n"
                f"{self._format_steps_str(top_s['steps'], top_s['urls'], top_s['helpline'], is_ta=False)}\n\n"
                f"You can submit your application via your nearest e-Sevai centre or directly through the official portal link above."
            )
            return {"tamil": ta, "english": en}

        # 8. Category / Domain Broad Inquiries (when asking about a sector without a single specific scheme)
        category_queries = [
            ("student", ["college", "student", "மாணவர்", "கல்லூரி", "படிப்பு", "பட்டதாரி", "degree", "school", "scholarship", "ஸ்காலர்ஷிப்"]),
            ("jobs", ["velai", "job", "unemployed", "வேலை", "வேலையில்லா", "வேலைவாய்ப்பு"]),
            ("loan", ["loan", "business", "தொழில்", "கடன்", "subsidy", "மானியம்", "லோன்", "சுயதொழில்", "வியாபாரம்", "முனைவோர்"]),
            ("women", ["magalir", "women", "மகளிர்", "பெண்", "பெண்கள்", "urimai thogai"]),
            ("farmer", ["farmer", "விவசாயி", "வேளாண்", "பயிர்", "உழவர்", "agriculture", "payir"]),
            ("medical", ["health", "medical", "மருத்துவம்", "காப்பீடு", "சிகிச்சை", "hospital"]),
            ("pension", ["pension", "முதியோர்", "ஓய்வூதியம்", "பென்ஷன்"])
        ]
        is_broad_category = False
        matched_cat_label = None
        for cat_key, cat_words in category_queries:
            if any(w in q_lower for w in cat_words) and len(q_tokens) <= 4:
                is_broad_category = True
                matched_cat_label = cat_key
                break

        if is_broad_category:
            scheme_bullets_ta = []
            scheme_bullets_en = []
            for idx, s_raw in enumerate(schemes[:3], 1):
                sf = self._extract_facts(s_raw)
                b_preview_ta = next(iter(sf["benefits"].values()), "அரசு நல உதவி") if sf["benefits"] else "அரசு நல உதவி"
                b_preview_en = next(iter(sf["benefits"].values()), "Government assistance") if sf["benefits"] else "Government assistance"
                scheme_bullets_ta.append(f"{idx}. **{sf['name_ta']}** - {b_preview_ta}")
                scheme_bullets_en.append(f"{idx}. **{sf['name_en']}** - {b_preview_en}")

            ta = (
                f"நண்பா, உங்கள் தேவைக்கு தமிழ்நாடு அரசின் மிகச் சிறந்த திட்டங்கள்:\n\n"
                + "\n\n".join(scheme_bullets_ta) + "\n\n"
                f"கீழே உள்ள திட்ட அட்டைகளில் முழு தகுதிகள், தேவையான ஆவணங்கள் மற்றும் விண்ணப்பிக்கும் வழிமுறைகளைப் பார்த்து உடனடியாகப் பயன்பெறுங்கள்!"
            )
            en = (
                f"Here are the top Tamil Nadu Government welfare schemes matching your inquiry:\n\n"
                + "\n\n".join(scheme_bullets_en) + "\n\n"
                f"Review each scheme card below for detailed eligibility criteria, required documents, and the official application portal."
            )
            return {"tamil": ta, "english": en}

        # 9. Scheme Overview / Specific Details / What is X
        ta = (
            f"நண்பா, **{top_name_ta}** ({top_name_en}) திட்டத்தின் முக்கிய விவரங்கள்:\n\n"
            f"🏛️ **துறை**: {top_s['dept_ta'] or top_s['dept']}\n"
            f"📝 **விவரம்**: {top_s['desc_ta'] or top_s['desc_en']}\n\n"
            f"💰 **வழங்கப்படும் அதிகாரப்பூர்வ சலுகைகள்**:\n"
            f"{self._format_benefits_str(top_s['benefits'], is_ta=True)}\n\n"
            f"📋 **முக்கிய தகுதி வரம்புகள்**:\n"
            f"{self._format_eligibility_str(top_s['rules'], is_ta=True)}\n\n"
            f"🌐 **அதிகாரப்பூர்வ தளம்**: {top_s['urls'][0] if top_s['urls'] else 'https://www.tn.gov.in'} | 📞 **உதவி எண்**: {top_s['helpline']}"
        )
        en = (
            f"Official details for **{top_name_en}** ({top_name_ta}):\n\n"
            f"🏛️ **Department**: {top_s['dept']}\n"
            f"📝 **Overview**: {top_s['desc_en'] or top_s['desc_ta']}\n\n"
            f"💰 **Official Benefits**:\n"
            f"{self._format_benefits_str(top_s['benefits'], is_ta=False)}\n\n"
            f"📋 **Eligibility Criteria**:\n"
            f"{self._format_eligibility_str(top_s['rules'], is_ta=False)}\n\n"
            f"🌐 **Official Portal**: {top_s['urls'][0] if top_s['urls'] else 'https://www.tn.gov.in'} | 📞 **Helpline**: {top_s['helpline']}"
        )
        return {"tamil": ta, "english": en}

gemini_service = GeminiService()