from news_gathering_system.storage.database_manager import DatabaseManager
from news_gathering_system.config import DATABASE_PATH
import os
import json

def get_sample_data(limit=5):
    db_manager = DatabaseManager(DATABASE_PATH)
    articles = db_manager.fetch_data("articles")
    db_manager.close_connection()
    
    sample_articles = []
    for article in articles[:limit]:
        # Assuming the order of columns: id, source_type, source_url, title, content, author, published_date, collected_at, tags, extra_metadata
        sample_articles.append({
            "title": article[3], # title
            "url": article[2]    # source_url
        })
    return json.dumps(sample_articles, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    print(get_sample_data())
