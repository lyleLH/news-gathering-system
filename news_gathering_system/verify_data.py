from news_gathering_system.storage.database_manager import DatabaseManager
import os
from news_gathering_system.config import DATABASE_PATH

def verify_data():
    db_manager = DatabaseManager(DATABASE_PATH)
    
    articles = db_manager.fetch_data("articles")
    
    print(f"Found {len(articles)} articles in the database:")
    for article in articles:
        print(article)
        
    db_manager.close_connection()

if __name__ == "__main__":
    verify_data()