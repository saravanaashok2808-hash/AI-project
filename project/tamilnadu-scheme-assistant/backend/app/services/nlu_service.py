import re

class NLUService:
    def detect_language(self, text: str) -> str:
        # Check if text contains Tamil Unicode characters
        if re.search(r'[\u0B80-\u0BFF]', text):
            return "ta"

        # Check for Romanized Tanglish keywords (spoken Tamil in English script)
        tanglish_markers = [
            "enakku", "eenaku", "enaku", "unaku", "ungalukku", "namakku",
            "irukku", "irukka", "mudinjudhu", "mudichen", "venum", "vendam",
            "thittam", "kedaikkuma", "kedaikuma", "kedakkuma", "kedaikumaa", "kedaikala",
            "kedaikkum", "kedaikum", "kedaikadha", "kedaikadhaa",
            "theriyanum", "theriyala", "puriyala", "aachu", "aagudhu",
            "velai", "vivasayi", "magalir", "kaapidu", "kadan", "padippu", "pasanga",
            "kulandhai", "nanban", "nanba", "nanbaa", "thozha", "machan", "thambi", "anna",
            "enna", "edhu", "ethu", "ithu", "idhu", "ithula", "idhula", "elam", "ellam",
            "epdi", "eppadi", "edhavadhu", "evlo", "evalavu", "romba",
            "solunga", "sollunga", "solren", "paththi", "paaru", "vayasu",
            "varuma", "mudiyuma", "varumaa", "mudiyumaa", "seri", "apdiya"
        ]
        text_lower = text.lower()
        if any(re.search(rf"\b{re.escape(word)}\b", text_lower) for word in tanglish_markers):
            return "ta"

        return "en"

    def classify_intent(self, text: str) -> str:
        text = text.lower()
        # 1. Documents Required
        if any(word in text for word in [
            "documents", "document", "proof", "proofs", "certificate", "certificates",
            "ஆவணங்கள்", "ஆவணம்", "சான்றிதழ்", "சான்றிதழ்கள்", "theva aavanangal",
            "டாக்குமெண்ட்", "சர்டிபிகேட்", "aavanangal", "aavanam"
        ]):
            return "documents_required"

        # 2. Benefits / Financial / Subsidy Amount Inquiry
        if any(word in text for word in [
            "how much", "how much money", "subsidy", "amount", "stipend", "evlo", "evalavu",
            "panam", "kadan evlo", "subsidy evlo", "எவ்வளவு", "தொகை", "மானியம்", "ரூபாய்",
            "நிதி உதவி", "coverage", "insurance amount"
        ]):
            return "benefits_inquiry"

        # 3. Application Process
        if any(word in text for word in [
            "how to apply", "steps to apply", "application process", "where to apply",
            "விண்ணப்பிக்க", "விண்ணப்பிப்பது எப்படி", "epdi apply", "eppadi apply",
            "vinnappikka", "அப்ளை செய்வது எப்படி", "வழிமுறை", "அப்ளிகேஷன் முறை",
            "apply online", "apply panrathu"
        ]):
            return "application_process"

        # 4. Helpline / Support
        if any(word in text for word in [
            "helpline", "toll free", "tollfree", "phone number", "contact number",
            "ஹெல்ப்லைன்", "தொலைபேசி எண்", "உதவி எண்"
        ]):
            return "helpline_inquiry"

        # 5. Check Eligibility
        if any(word in text for word in [
            "best", "nalladhu", "ethu best", "edhu best", "which is best", "recommend",
            "eligibility", "eligible", "can i get", "am i eligible", "will i get", "qualify",
            "income limit", "age limit", "qualification", "rules", "நிபந்தனை", "வருமான வரம்பு",
            "தகுதி", "தகுதிகள்", "thaghudhi", "thakudhi", "எலிஜிபிள்",
            "kedaikuma", "kedaikkuma", "kedakkuma", "kedaikumaa", "kedaikum",
            "varuma", "varumaa", "kedaikadha", "kedaikadhaa", "mudiyuma", "mudiyumaa"
        ]):
            return "check_eligibility"

        # 6. Scheme Details / What is X
        if any(word in text for word in [
            "details", "about", "what is", "விவரம்", "vivaram", "paththi", "பற்றி",
            "டீடைல்ஸ்", "explain", "சொல்லுங்க"
        ]):
            return "scheme_details"

        # 7. Help / Support
        if any(word in text for word in ["help", "support", "உதவி", "udhavi", "ஹெல்ப்"]):
            return "help"

        # Default for scheme queries (find/search/what schemes)
        return "find_scheme"

    def extract_entities(self, text: str) -> dict:
        entities = {}
        text_lower = text.lower()
        
        # Age extraction (handles 23 years, age 23, 23 age, 23 வயது, 23 வயசு, 23 vayasu, 23 aachu)
        age_match = re.search(r'(\d{1,2})\s*(?:years?|yrs?|வயது|வயசு|vayasu|age|aachu|aagudhu)(?:[^\w]|$)', text_lower)
        if not age_match:
            age_match = re.search(r'(?:age|வயது|வயசு|vayasu)\s*[:=]?\s*(\d{1,2})(?:[^\w]|$)', text_lower)
        if age_match:
            entities['age'] = int(age_match.group(1))

        # Gender
        if any(word in text_lower for word in ["female", "woman", "girl", "பெண்", "மகள்", "தாய்", "ladies", "lady"]):
            entities['gender'] = "Female"
        elif any(word in text_lower for word in ["male", "man", "boy", "ஆண்", "மகன்", "gents"]):
            entities['gender'] = "Male"

        # Employment / Unemployment status (Pure Tamil, English, and Spoken Tamil loanwords)
        if any(word in text_lower for word in [
            "unemployed", "jobless", "no job", "looking for job",
            "வேலை இல்லாம", "வேலையில்லை", "வேலை இல்லை", "வேலை தேடும்", "வேலை தேடுறேன்",
            "velai illa", "velai kedaikala", "job illa", "velai theduren", "velai thedum",
            "ஜாப் இல்ல", "ஜாப் இல்லாம", "வேலை கெடைக்கல"
        ]):
            entities['employment_status'] = "Unemployed"

        # Education
        if any(word in text_lower for word in [
            "degree", "graduate", "college", "கல்லூரி", "பட்டதாரி", "படிச்சு முடிச்சு",
            "college mudichen", "degree mudichen", "patadhari", "engineering", "b.e", "b.tech", "arts",
            "காலேஜ்", "டிகிரி", "இன்ஜினியரிங்"
        ]):
            entities['education_level'] = "Graduate"
        elif any(word in text_lower for word in ["school", "பள்ளி", "10th", "12th", "பிளஸ் டூ", "school mudichen", "ஸ்கூல்"]):
            entities['education_level'] = "School"

        # Disability / Differently Abled (Tamil, English, and Tanglish)
        if any(word in text_lower for word in [
            "differently abled", "disabled", "disability", "handicapped", "physically challenged",
            "மாற்றுத்திறனாளி", "ஊனம்", "மாற்றுத் திறனாளி", "maatru thirunaali", "handicap"
        ]):
            entities['disability'] = "Yes"

        # Marital Status & Marriage Assistance
        if any(word in text_lower for word in ["widow", "விதவை", "vithavai"]):
            entities['marital_status'] = "Widow"
        elif any(word in text_lower for word in ["deserted", "கைவிடப்பட்ட", "kaividapatta"]):
            entities['marital_status'] = "Deserted"
        elif any(word in text_lower for word in ["marriage", "திருமணம்", "கல்யாணம்", "kalyanam", "wedding"]):
            entities['seeking_marriage_assistance'] = True

        # Common Tamil districts
        districts = [
            "chennai", "coimbatore", "madurai", "tiruchirappalli", "salem", "tirunelveli", "thanjavur",
            "தஞ்சாவூர்", "சென்னை", "மதுரை", "கோயம்புத்தூர்", "திருச்சி", "சேலம்", "ஈரோடு", "திண்டுக்கல்",
            "erode", "dindigul", "vellore", "வேலூர்", "tiruppur", "திருப்பூர்"
        ]
        for district in districts:
            if district in text_lower:
                entities['district'] = district.title()

        # Occupation & Entrepreneurship (English, Tamil, and spoken loanwords)
        occupations = [
            ("farmer", ["farmer", "agriculturist", "விவசாயி", "உழவர்", "vivasayi", "vivasayam", "agri"]),
            ("student", ["student", "மாணவர்", "மாணவி", "படிக்கும்", "padikkum", "studying", "ஸ்டூடண்ட்"]),
            ("entrepreneur", ["entrepreneur", "business", "தொழில்", "தொழில்முனைவோர்", "suya thozhil", "startup", "kada", "பிசினஸ்", "ஸ்டார்ட்அப்", "லோன்"]),
            ("weaver", ["weaver", "நெசவாளர்", "கைத்தறி", "nesavalar"]),
            ("fisherman", ["fisherman", "மீனவர்", "மீன்பிடி", "meenavar"]),
            ("construction", ["construction", "கட்டுமான", "கொத்தனார்", "kattumanam"]),
            ("driver", ["driver", "ஆட்டோ", "ஓட்டுநர்", "டாக்சி", "auto driver"]),
            ("tailor", ["tailor", "தையல்", "thayal"])
        ]
        for occ_name, keywords in occupations:
            if any(kw in text_lower for kw in keywords):
                entities['occupation'] = occ_name.title()
                break

        return entities

nlu_service = NLUService()
