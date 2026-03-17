from news_gathering_system.storage.database_manager import DatabaseManager
from news_gathering_system.acquisition.data_acquirer import DataAcquirer
import logging
import os

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def run_collector():
    logging.info("Starting data collection...")
    
    # Initialize DatabaseManager
    db_path = os.path.join(os.path.dirname(__file__), '..', 'news_data.db')
    db_manager = DatabaseManager(db_path)
    
    # Initialize DataAcquirer
    data_acquirer = DataAcquirer(db_manager)
    
    # Define example sources to scrape
    # These are placeholder URLs and selectors. In a real scenario, these would be dynamic.
    sources = {
        "news_site": [
            {"url": "https://news.ycombinator.com/", "selectors": None} # Using Hacker News for a news-like site
        ],
        "trending": [
            {"url": "https://www.reddit.com/r/popular/", "selectors": None} # Using Reddit popular for trending topics
        ],
        "competitor_blog": [
            {"url": "https://blog.cloudflare.com/", "competitor_name": "Cloudflare", "selectors": None}
        ],
        "ugc_forum_listing": [
            {"url": "https://www.example.com/forum", "selectors": None} # Still a placeholder, as real forums are complex
        ]
    }
    
    # Collect data from all defined sources
    collected_data = data_acquirer.collect_all(sources)
    
    logging.info(f"Finished data collection. Collected {len(collected_data)} items.")
    
    # Close database connection
    db_manager.close_connection()

if __name__ == "__main__":
    run_collector()