import asyncio
import json
import logging
import sys
from pathlib import Path
import aiosqlite

# Add backend directory to sys.path
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(BASE_DIR / "backend"))

from app.core.config import settings
from app.core.database import init_db

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger("ingest")

async def ingest_schemes():
    await init_db()
    data_file = BASE_DIR / "data" / "schemes" / "tn_schemes_verified.json"
    if not data_file.exists():
        logger.error(f"Verified schemes file not found at {data_file}")
        return

    with open(data_file, "r", encoding="utf-8") as f:
        schemes = json.load(f)

    logger.info(f"Loaded {len(schemes)} schemes from {data_file.name}")

    async with aiosqlite.connect(settings.DATABASE_PATH) as db:
        for s in schemes:
            await db.execute("""
            INSERT INTO schemes (
                scheme_id, scheme_name_tamil, scheme_name_english, department,
                department_tamil, category, sub_category, description_tamil,
                description_english, benefits, eligibility_rules, required_documents,
                application_method, application_steps, official_urls, contact_helpline,
                dates, source_metadata, content_hash, version, status
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(scheme_id) DO UPDATE SET
                scheme_name_tamil = excluded.scheme_name_tamil,
                scheme_name_english = excluded.scheme_name_english,
                department = excluded.department,
                department_tamil = excluded.department_tamil,
                category = excluded.category,
                sub_category = excluded.sub_category,
                description_tamil = excluded.description_tamil,
                description_english = excluded.description_english,
                benefits = excluded.benefits,
                eligibility_rules = excluded.eligibility_rules,
                required_documents = excluded.required_documents,
                application_method = excluded.application_method,
                application_steps = excluded.application_steps,
                official_urls = excluded.official_urls,
                contact_helpline = excluded.contact_helpline,
                dates = excluded.dates,
                source_metadata = excluded.source_metadata,
                content_hash = excluded.content_hash,
                version = excluded.version,
                status = excluded.status,
                updated_at = CURRENT_TIMESTAMP;
            """, (
                s["scheme_id"],
                s["scheme_name_tamil"],
                s["scheme_name_english"],
                s["department"],
                s.get("department_tamil"),
                s["category"],
                s.get("sub_category"),
                s["description_tamil"],
                s["description_english"],
                json.dumps(s.get("benefits", {}), ensure_ascii=False),
                json.dumps(s.get("eligibility_rules", {}), ensure_ascii=False),
                json.dumps(s.get("required_documents", []), ensure_ascii=False),
                s.get("application_method", "Offline"),
                json.dumps(s.get("application_steps", []), ensure_ascii=False),
                json.dumps(s.get("official_urls", []), ensure_ascii=False),
                s.get("contact_helpline"),
                json.dumps(s.get("dates", {}), ensure_ascii=False),
                json.dumps(s.get("source_metadata", {}), ensure_ascii=False),
                s.get("content_hash"),
                s.get("version", 1),
                s.get("status", "Active")
            ))

        # Rebuild FTS5 external content index
        await db.execute("INSERT INTO schemes_fts(schemes_fts) VALUES('rebuild');")
        await db.commit()

        cursor = await db.execute("SELECT count(*) FROM schemes;")
        row = await cursor.fetchone()
        logger.info(f"Ingestion successful! Total active schemes in database: {row[0]}")

if __name__ == "__main__":
    asyncio.run(ingest_schemes())
