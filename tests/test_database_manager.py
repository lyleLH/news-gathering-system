import os
import sqlite3
import pytest
from news_gathering_system.storage.database_manager import DatabaseManager

@pytest.fixture
def db_manager():
    db_path = "test_news_data.db"
    if os.path.exists(db_path):
        os.remove(db_path)
    manager = DatabaseManager(db_path)
    yield manager
    manager.close_connection()
    if os.path.exists(db_path):
        os.remove(db_path)

def test_create_table(db_manager):
    db_manager.create_table("articles", {
        "id": "INTEGER PRIMARY KEY",
        "title": "TEXT NOT NULL",
        "url": "TEXT UNIQUE NOT NULL",
        "content": "TEXT",
        "source": "TEXT",
        "published_date": "TEXT"
    })
    conn = sqlite3.connect(db_manager.db_path)
    cursor = conn.cursor()
    cursor.execute("PRAGMA table_info(articles)")
    columns = [col[1] for col in cursor.fetchall()]
    assert "title" in columns
    assert "url" in columns
    conn.close()

def test_insert_article(db_manager):
    db_manager.create_table("articles", {
        "id": "INTEGER PRIMARY KEY",
        "title": "TEXT NOT NULL",
        "url": "TEXT UNIQUE NOT NULL",
        "content": "TEXT",
        "source": "TEXT",
        "published_date": "TEXT"
    })
    article_data = {
        "title": "Test Article",
        "url": "http://test.com/article1",
        "content": "This is a test content.",
        "source": "Test Source",
        "published_date": "2026-03-17"
    }
    db_manager.insert_data("articles", article_data)
    conn = sqlite3.connect(db_manager.db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT title, url FROM articles WHERE title = 'Test Article'")
    result = cursor.fetchone()
    assert result == ("Test Article", "http://test.com/article1")
    conn.close()
