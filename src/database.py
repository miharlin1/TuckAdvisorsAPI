import sqlite3
from pathlib import Path
from contextlib import contextmanager

DB_PATH = Path(__file__).parent / "data" / "analyses.db"


@contextmanager
def get_db_connection():
    """Context manager for database connections."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()


def init_database():
    """Initialize the database schema."""
    with get_db_connection() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS analyses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                markdown_content TEXT NOT NULL,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
    print(f"Database initialized at {DB_PATH}")


def insert_analysis(markdown_content):
    """
    Insert a new analysis into the database.
    
    Args:
        markdown_content: The GPT output markdown
        
    Returns:
        The ID of the inserted row
    """
    with get_db_connection() as conn:
        cursor = conn.execute(
            "INSERT INTO analyses (markdown_content) VALUES (?)",
            (markdown_content,)
        )
        return cursor.lastrowid


def get_latest_markdown():
    """
    Get the most recent markdown content.
    
    Returns:
        Markdown string or None if no data exists
    """
    with get_db_connection() as conn:
        row = conn.execute(
            "SELECT markdown_content FROM analyses ORDER BY updated_at DESC LIMIT 1"
        ).fetchone()
        
        return row["markdown_content"] if row else None


def append_to_markdown(additional_text):
    """
    Append text to the existing markdown content.
    
    Args:
        additional_text: Text to append
        
    Returns:
        Updated markdown content or None if no data exists
    """
    current_markdown = get_latest_markdown()
    if not current_markdown:
        return None
    
    updated_content = current_markdown + " " + additional_text
    
    with get_db_connection() as conn:
        conn.execute(
            """
            UPDATE analyses 
            SET markdown_content = ?, updated_at = CURRENT_TIMESTAMP
            WHERE id = (SELECT id FROM analyses ORDER BY updated_at DESC LIMIT 1)
            """,
            (updated_content,)
        )
    
    return updated_content

