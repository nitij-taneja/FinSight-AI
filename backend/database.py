"""
Database initialization and schema setup for the Financial News Intelligence System.
"""

import sqlite3
from pathlib import Path
from typing import Optional

# Database path
DB_PATH = Path(__file__).parent / "news_intelligence.db"


def get_db_connection():
    """Get a database connection."""
    conn = sqlite3.connect(str(DB_PATH))
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    """Initialize the database with required tables."""
    conn = get_db_connection()
    cursor = conn.cursor()

    # Create articles table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS articles (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            content TEXT NOT NULL,
            source TEXT,
            url TEXT UNIQUE,
            published_date TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            embedding BLOB,
            is_duplicate BOOLEAN DEFAULT 0,
            canonical_id INTEGER,
            FOREIGN KEY (canonical_id) REFERENCES articles(id)
        )
    """)

    # Create entities table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS entities (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            article_id INTEGER NOT NULL,
            entity_text TEXT NOT NULL,
            entity_type TEXT NOT NULL,
            confidence REAL DEFAULT 1.0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (article_id) REFERENCES articles(id) ON DELETE CASCADE
        )
    """)

    # Create stock impacts table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS stock_impacts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            article_id INTEGER NOT NULL,
            stock_symbol TEXT NOT NULL,
            impact_type TEXT,
            confidence REAL DEFAULT 0.5,
            sentiment TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (article_id) REFERENCES articles(id) ON DELETE CASCADE
        )
    """)

    # Create deduplication records table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS deduplication_records (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            article_id_1 INTEGER NOT NULL,
            article_id_2 INTEGER NOT NULL,
            similarity_score REAL,
            is_duplicate BOOLEAN DEFAULT 1,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (article_id_1) REFERENCES articles(id) ON DELETE CASCADE,
            FOREIGN KEY (article_id_2) REFERENCES articles(id) ON DELETE CASCADE
        )
    """)

    # Create query cache table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS query_cache (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            query_text TEXT NOT NULL,
            results TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # Create indices for better query performance
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_articles_canonical ON articles(canonical_id)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_entities_article ON entities(article_id)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_entities_type ON entities(entity_type)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_stock_impacts_article ON stock_impacts(article_id)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_stock_impacts_symbol ON stock_impacts(stock_symbol)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_dedup_articles ON deduplication_records(article_id_1, article_id_2)")

    conn.commit()
    conn.close()


if __name__ == "__main__":
    init_db()
    print(f"Database initialized at {DB_PATH}")
