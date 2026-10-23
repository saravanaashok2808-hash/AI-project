import json
import logging
from pathlib import Path
import aiosqlite
from app.core.config import settings

logger = logging.getLogger("db")

async def get_db():
    settings.DATABASE_PATH.parent.mkdir(parents=True, exist_ok=True)
    async with aiosqlite.connect(settings.DATABASE_PATH) as db:
        db.row_factory = aiosqlite.Row
        yield db

async def init_db():
    settings.DATABASE_PATH.parent.mkdir(parents=True, exist_ok=True)
    logger.info(f"Initializing database at {settings.DATABASE_PATH}")
    async with aiosqlite.connect(settings.DATABASE_PATH) as db:
        await db.execute("PRAGMA foreign_keys = ON;")
        await db.execute("PRAGMA journal_mode = WAL;")

        # 1. Main schemes table
        await db.execute("""
        CREATE TABLE IF NOT EXISTS schemes (
            scheme_id TEXT PRIMARY KEY,
            scheme_name_tamil TEXT NOT NULL,
            scheme_name_english TEXT NOT NULL,
            department TEXT NOT NULL,
            department_tamil TEXT,
            category TEXT NOT NULL,
            sub_category TEXT,
            description_tamil TEXT,
            description_english TEXT,
            benefits TEXT,            -- JSON string
            eligibility_rules TEXT,   -- JSON string
            required_documents TEXT,  -- JSON string
            application_method TEXT,
            application_steps TEXT,   -- JSON string
            official_urls TEXT,       -- JSON string
            contact_helpline TEXT,
            dates TEXT,               -- JSON string
            source_metadata TEXT,     -- JSON string
            content_hash TEXT,
            version INTEGER DEFAULT 1,
            status TEXT DEFAULT 'Active',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """)

        # 2. FTS5 Virtual Table for high-speed bilingual full-text search
        await db.execute("""
        CREATE VIRTUAL TABLE IF NOT EXISTS schemes_fts USING fts5(
            scheme_id UNINDEXED,
            scheme_name_tamil,
            scheme_name_english,
            department,
            category,
            description_tamil,
            description_english,
            content='schemes',
            content_rowid='rowid'
        );
        """)

        # 3. Ephemeral sessions table
        await db.execute("""
        CREATE TABLE IF NOT EXISTS sessions (
            session_id TEXT PRIMARY KEY,
            profile_data TEXT,        -- JSON string
            conversation_history TEXT,-- JSON string
            last_activity TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """)

        # 4. Registered users table with credentials and profiles
        await db.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            phone TEXT,
            email TEXT,
            password_hash TEXT NOT NULL,
            salt TEXT NOT NULL,
            profile_data TEXT,        -- JSON string of UserProfile
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """)
        await db.execute("CREATE INDEX IF NOT EXISTS idx_users_name ON users(name);")
        await db.execute("CREATE INDEX IF NOT EXISTS idx_users_phone ON users(phone);")

        await db.commit()
    logger.info("Database initialized successfully.")
