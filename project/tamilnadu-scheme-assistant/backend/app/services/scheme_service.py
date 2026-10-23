import json
import re
import aiosqlite
from app.core.config import settings

STOP_WORDS = {
    # English
    "a", "an", "the", "in", "on", "at", "for", "of", "to", "and", "or", "is", "am",
    "are", "was", "were", "i", "me", "my", "we", "our", "you", "your", "he", "she",
    "it", "they", "what", "which", "who", "whom", "how", "can", "could", "would",
    "should", "do", "does", "did", "have", "has", "had", "looking", "look", "want",
    "need", "get", "avail", "available", "apply", "give", "help", "about", "any",
    "some", "details", "information", "info", "please", "tell", "show", "scheme",
    "schemes", "thittam", "thittangal",
    # Tamil
    "ஒரு", "மற்றும்", "அல்லது", "எனக்கு", "என்ன", "எந்த", "எப்படி", "இருக்கும்",
    "உள்ள", "வேண்டும்", "உதவி", "பற்றி", "விவரம்", "திட்டம்", "திட்டங்கள்",
    "ஹாய்", "ப்ரோ", "சார்", "வணக்கம்", "அண்ணா", "தம்பி", "ஏதாவது", "இல்லாம",
    "இருக்கேன்", "இருக்கிறேன்", "கிடைக்குமா", "பண்ணலாம்", "சொல்லுங்க", "சொல்ல",
    "தெரியுமா", "hello", "hi", "bro", "sir",
    # Tanglish conversational words
    "ithu", "idhu", "ithula", "idhula", "ethu", "edhu", "best", "nalladhu", "first", "mukkiyam",
    "elam", "ellam", "ella",
    "kedaikuma", "kedaikkuma", "kedakkuma", "kedaikumaa", "kedaikum", "kedaikadha", "kedaikala",
    "nanba", "nanbaa", "nanban", "thozha", "machan", "thambi", "anna",
    "eenaku", "enakku", "enaku", "unaku", "ungalukku", "namakku",
    "solunga", "sollunga", "solren", "puriyala", "theriyala",
    "varuma", "varumaa", "varum", "mudiyuma", "mudiyumaa", "panna", "pannalama",
    "seri", "apdiya", "aachu", "aagudhu"
}

SYNONYMS = {
    "women": ["women", "woman", "girl", "girls", "female", "ladies", "மகளிர்", "பெண்", "பெண்கள்"],
    "woman": ["women", "woman", "girl", "girls", "female", "ladies", "மகளிர்", "பெண்", "பெண்கள்"],
    "girl": ["women", "woman", "girl", "girls", "female", "ladies", "மகளிர்", "பெண்", "பெண்கள்"],
    "girls": ["women", "woman", "girl", "girls", "female", "ladies", "மகளிர்", "பெண்", "பெண்கள்"],
    "female": ["women", "woman", "girl", "girls", "female", "ladies", "மகளிர்", "பெண்", "பெண்கள்"],
    "farmer": ["farmer", "farmers", "agriculture", "agricultural", "விவசாயி", "விவசாயிகள்", "உழவர்"],
    "farmers": ["farmer", "farmers", "agriculture", "agricultural", "விவசாயி", "விவசாயிகள்", "உழவர்"],
    "agriculture": ["farmer", "farmers", "agriculture", "agricultural", "விவசாயி", "விவசாயிகள்", "உழவர்"],
    "health": ["health", "hospital", "medical", "insurance", "மருத்துவம்", "மருத்துவக்", "காப்பீடு"],
    "medical": ["health", "hospital", "medical", "insurance", "மருத்துவம்", "மருத்துவக்", "காப்பீடு"],
    "insurance": ["health", "hospital", "medical", "insurance", "மருத்துவம்", "மருத்துவக்", "காப்பீடு"],
    "student": ["student", "students", "college", "school", "education", "படிப்பு", "மாணவர்", "மாணவர்கள்", "கல்வி"],
    "education": ["student", "students", "college", "school", "education", "படிப்பு", "மாணவர்", "மாணவர்கள்", "கல்வி"],
    "college": ["student", "students", "college", "school", "education", "படிப்பு", "மாணவர்", "மாணவர்கள்", "கல்வி"],
    "படிச்சு": ["student", "college", "degree", "படிப்பு", "மாணவர்", "பட்டதாரி", "கல்வி"],
    "pension": ["pension", "old", "elderly", "aged", "senior", "முதியோர்", "ஓய்வூதியம்"],
    "old": ["pension", "old", "elderly", "aged", "senior", "முதியோர்", "ஓய்வூதியம்"],
    "senior": ["pension", "old", "elderly", "aged", "senior", "முதியோர்", "ஓய்வூதியம்"],
    "unemployed": ["unemployed", "employment", "job", "வேலை", "வேலையில்லா", "வேலைவாய்ப்பு", "வேலையின்மை", "உதவித்தொகை"],
    "job": ["unemployed", "employment", "job", "வேலை", "வேலையில்லா", "வேலைவாய்ப்பு"],
    "வேலை": ["unemployed", "employment", "job", "வேலையில்லா", "வேலைவாய்ப்பு", "வேலையின்மை"],
    "disabled": ["disabled", "disability", "differently", "மாற்றுத்திறனாளி", "மாற்றுத்திறனாளிகள்"],
    "loan": ["loan", "subsidy", "finance", "கடன்", "மானியம்", "நிதி"],
    "கடன்": ["loan", "subsidy", "finance", "கடன்", "மானியம்"],
    "லோன்": ["loan", "subsidy", "finance", "கடன்", "மானியம்"],
    "business": ["business", "enterprise", "entrepreneur", "self employment", "தொழில்", "தொழில்முனைவோர்", "சுயவேலை"],
    "தொழில்": ["business", "enterprise", "entrepreneur", "self employment", "தொழில்", "தொழில்முனைவோர்"],
    "பிசினஸ்": ["business", "enterprise", "entrepreneur", "self employment", "தொழில்", "தொழில்முனைவோர்"],
    "காலேஜ்": ["student", "college", "degree", "கல்லூரி", "கல்வி", "படிப்பு", "பட்டதாரி"],
    "டிகிரி": ["student", "college", "degree", "கல்லூரி", "கல்வி", "படிப்பு", "பட்டதாரி"],
    "ஜாப்": ["unemployed", "employment", "job", "வேலை", "வேலையில்லா", "வேலைவாய்ப்பு"],
    "பென்ஷன்": ["pension", "old", "elderly", "aged", "senior", "முதியோர்", "ஓய்வூதியம்"],
    "scholarship": ["scholarship", "stipend", "கல்வி", "உதவித்தொகை", "படிப்பு"],
    "ஸ்காலர்ஷிப்": ["scholarship", "stipend", "கல்வி", "உதவித்தொகை", "படிப்பு"],
    "marriage": ["marriage", "remarriage", "wedding", "திருமணம்", "மறுமணம்", "கல்யாணம்"],
    "கல்யாணம்": ["marriage", "remarriage", "wedding", "திருமணம்", "மறுமணம்"],
    "muthulakshmi": ["muthulakshmi", "reddy", "maternity", "மகப்பேறு", "முத்துலட்சுமி"],
    "maternity": ["muthulakshmi", "maternity", "pregnant", "மகப்பேறு", "கர்ப்பிணி"],
    "மகப்பேறு": ["muthulakshmi", "maternity", "மகப்பேறு", "முத்துலட்சுமி"],
    "kmut": ["kmut", "magalir", "urimai", "thogai", "மகளிர்", "உரிமைத்தொகை", "கலைஞர்"],
    "pudhumai": ["pudhumai", "penn", "புதுமை", "புதுமைப் பெண்"],
    "penn": ["pudhumai", "penn", "பெண்", "புதுமைப் பெண்"],
    "புதுமை": ["pudhumai", "penn", "புதுமை", "புதுமைப் பெண்"],
    "pudhalvan": ["pudhalvan", "tamizh", "புதல்வன்", "தமிழ்ப் புதல்வன்"],
    "புதல்வன்": ["pudhalvan", "tamizh", "புதல்வன்", "தமிழ்ப் புதல்வன்"],
    "uyegp": ["uyegp", "வேலையில்லா", "வேலைவாய்ப்பு", "மானியம்"],
    "needs": ["needs", "தொழில்முனைவோர்", "நீட்ஸ்", "மானியம்"],
    "cmchis": ["cmchis", "மருத்துவக் காப்பீடு", "காப்பீடு", "insurance"],
    "laptop": ["laptop", "மடிக்கணினி", "மடி கணிணி"],
    "tahdco": ["tahdco", "தாட்கோ", "ஆதிதிராவிடர்", "பழங்குடியினர்"],
    "தாட்கோ": ["tahdco", "தாட்கோ", "ஆதிதிராவிடர்", "பழங்குடியினர்"],
    "crop": ["crop", "insurance", "pmfby", "பயிர்", "காப்பீடு"],
    "pmfby": ["pmfby", "crop", "insurance", "பயிர்", "காப்பீடு"],
    "fishermen": ["fishermen", "fisheries", "மீனவர்", "மீன்பிடி", "நிவாரணம்"],
    "மீனவர்": ["fishermen", "fisheries", "மீனவர்", "மீன்பிடி"],
    "innuyir": ["innuyir", "kaappom", "48", "இன்னுயிர்"],
    "இன்னுயிர்": ["innuyir", "kaappom", "48", "இன்னுயிர்"]
}

class SchemeService:
    async def _row_to_dict(self, row: aiosqlite.Row) -> dict:
        data = dict(row)
        for json_col in [
            "benefits", "eligibility_rules", "required_documents",
            "application_steps", "official_urls", "dates", "source_metadata",
        ]:
            if data.get(json_col):
                try:
                    data[json_col] = json.loads(data[json_col])
                except json.JSONDecodeError:
                    data[json_col] = (
                        {} if json_col in ("benefits", "eligibility_rules", "dates", "source_metadata") else []
                    )
        return data

    def _extract_search_terms(self, query: str) -> list[str]:
        # Clean query, split words
        words = re.findall(r"[\w\u0B80-\u0BFF]+", query.lower())
        filtered = [w for w in words if w not in STOP_WORDS and len(w) > 1]

        tamil_suffixes = [
            "களுக்கான", "ளுக்கான", "களுக்கு", "ளுக்கு", "க்கான", "க்கு",
            "களின்", "ளின்", "யின்", "இன்", "கள்", "ஆக", "இல்", "உடன்", "ஆகிய"
        ]

        terms = set()
        for w in filtered:
            terms.add(w)
            for suff in tamil_suffixes:
                if w.endswith(suff) and len(w) > len(suff) + 2:
                    stem = w[:-len(suff)]
                    terms.add(stem)
                    if stem in SYNONYMS:
                        for syn in SYNONYMS[stem]:
                            terms.add(syn)
                    break

            if w in SYNONYMS:
                for syn in SYNONYMS[w]:
                    terms.add(syn)

        return list(terms)

    async def search_schemes(self, query: str, filters: dict = None, profile = None) -> list[dict]:
        clean_q = query.strip()
        if not clean_q and not profile:
            return await self.get_all_schemes()

        terms = self._extract_search_terms(clean_q)
        
        # Enrich search terms using profile if available
        if profile:
            if getattr(profile, "employment_status", None) == "Unemployed":
                terms.extend(["வேலையில்லா", "வேலைவாய்ப்பு", "unemployed", "நான் முதல்வன்", "உதவித்தொகை"])
            if getattr(profile, "education_level", None) == "Graduate":
                terms.extend(["பட்டதாரி", "முதல் தலைமுறை", "graduate", "கல்லூரி"])
            if profile.occupation:
                terms.append(profile.occupation.lower())
            if profile.marital_status:
                terms.append(profile.marital_status.lower())

        if not terms:
            return await self.get_all_schemes()

        async with aiosqlite.connect(settings.DATABASE_PATH) as db:
            db.row_factory = aiosqlite.Row

            # 1. Try FTS5 prefix search with tokens
            # Safe FTS tokens (alphanumeric + prefix wildcard)
            fts_tokens = []
            for t in terms:
                # Keep ascii words or unicode tamil words
                safe_t = re.sub(r'[^\w\u0B80-\u0BFF]', '', t)
                if safe_t:
                    fts_tokens.append(f'"{safe_t}"*')

            rows = []
            if fts_tokens:
                fts_query = " OR ".join(fts_tokens)
                fts_sql = """
                    SELECT schemes.*, bm25(schemes_fts) AS rank
                    FROM schemes
                    JOIN schemes_fts ON schemes.rowid = schemes_fts.rowid
                    WHERE schemes_fts MATCH ?
                    ORDER BY rank
                """
                try:
                    async with db.execute(fts_sql, (fts_query,)) as cursor:
                        rows = await cursor.fetchall()
                except Exception:
                    rows = []

            # 2. Fallback LIKE search if FTS returned nothing
            if not rows:
                like_clauses = []
                params = []
                for t in terms[:5]:  # limit to top terms
                    like_clauses.append("""
                        (scheme_name_tamil LIKE ?
                         OR scheme_name_english LIKE ?
                         OR description_tamil LIKE ?
                         OR description_english LIKE ?
                         OR category LIKE ?
                         OR department LIKE ?)
                    """)
                    pattern = f"%{t}%"
                    params.extend([pattern] * 6)

                if like_clauses:
                    fallback_sql = f"""
                        SELECT * FROM schemes
                        WHERE {' OR '.join(like_clauses)}
                        LIMIT 10
                    """
                    try:
                        async with db.execute(fallback_sql, params) as cursor:
                            rows = await cursor.fetchall()
                    except Exception:
                        rows = []

            # If still nothing found, return all schemes as safe fallback
            if not rows:
                return await self.get_all_schemes()

            # Deduplicate by scheme_id
            seen = set()
            result = []
            for r in rows:
                d = await self._row_to_dict(r)
                if d["scheme_id"] not in seen:
                    seen.add(d["scheme_id"])
                    result.append(d)

            return result

    async def get_scheme(self, scheme_id: str) -> dict | None:
        async with aiosqlite.connect(settings.DATABASE_PATH) as db:
            db.row_factory = aiosqlite.Row
            async with db.execute("SELECT * FROM schemes WHERE scheme_id = ?", (scheme_id,)) as cursor:
                row = await cursor.fetchone()
                if row:
                    return await self._row_to_dict(row)
                return None

    async def get_all_schemes(self) -> list[dict]:
        async with aiosqlite.connect(settings.DATABASE_PATH) as db:
            db.row_factory = aiosqlite.Row
            async with db.execute("SELECT * FROM schemes ORDER BY scheme_id") as cursor:
                rows = await cursor.fetchall()
                return [await self._row_to_dict(row) for row in rows]


scheme_service = SchemeService()
