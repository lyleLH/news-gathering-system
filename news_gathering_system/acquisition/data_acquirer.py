import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin
import hashlib
import logging
from news_gathering_system.storage.database_manager import DatabaseManager

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class DataAcquirer:
    def __init__(self, db_manager: DatabaseManager, default_selectors=None):
        self.db_manager = db_manager
        self.default_selectors = default_selectors if default_selectors is not None else {
            "news_site": {
                "article_container": "tr.athing",
                "title": "span.titleline a",
                "link": "span.titleline a",
                "summary": None,
                "author": "td.subtext a.hnuser",
                "date": "td.subtext span.age a"
            },
            "trending": {
                "item_container": ".item",
                "title": ".title a",
                "link": ".title a",
                "score": ".score"
            },
            "competitor": {
                "article_container": "div.post",
                "title": "h3 a",
                "link": "h3 a",
                "summary": ".excerpt",
                "author": ".post-author",
                "date": ".post-date"
            },
            "forum_listing": {
                "thread_container": ".thread-item",
                "title": ".thread-title a",
                "link": ".thread-title a",
                "author": ".thread-author",
                "reply_count": ".reply-count"
            },
            "forum_thread": {
                "post_container": ".post-item",
                "author": ".post-author",
                "content": ".post-content",
                "date": ".post-date"
            }
        }
        self._ensure_tables()

    def _ensure_tables(self):
        self.db_manager.create_table("articles", {
            "id": "TEXT PRIMARY KEY", # Using SHA-256 hash as ID for deduplication
            "source_type": "TEXT NOT NULL",
            "source_url": "TEXT NOT NULL",
            "title": "TEXT NOT NULL",
            "content": "TEXT",
            "author": "TEXT",
            "published_date": "TEXT",
            "collected_at": "TEXT DEFAULT CURRENT_TIMESTAMP",
            "tags": "TEXT",
            "extra_metadata": "TEXT"
        })

    def _fetch_page(self, url):
        try:
            headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status() # Raise an exception for HTTP errors
            return BeautifulSoup(response.text, 'html.parser')
        except requests.exceptions.RequestException as e:
            logging.error(f"Error fetching {url}: {e}")
            return None

    def _generate_id(self, url, title):
        return hashlib.sha256(f"{url}-{title}".encode('utf-8')).hexdigest()

    def scrape_news_site(self, url, selectors=None):
        logging.info(f"Scraping news site: {url}")
        soup = self._fetch_page(url)
        if not soup: return [] # Return empty list if page fetch fails

        current_selectors = selectors if selectors else self.default_selectors["news_site"]
        articles_data = []
        for article_container in soup.select(current_selectors["article_container"]):
            title_elem = article_container.select_one(current_selectors["title"]) if current_selectors["title"] else None
            link_elem = article_container.select_one(current_selectors["link"]) if current_selectors["link"] else None
            summary_elem = article_container.select_one(current_selectors["summary"]) if current_selectors["summary"] else None
            author_elem = article_container.select_one(current_selectors["author"]) if current_selectors["author"] else None
            date_elem = article_container.select_one(current_selectors["date"]) if current_selectors["date"] else None

            title = title_elem.get_text(strip=True) if title_elem else ""
            link = urljoin(url, link_elem['href']) if link_elem and 'href' in link_elem.attrs else ""
            summary = summary_elem.get_text(strip=True) if summary_elem else ""
            author = author_elem.get_text(strip=True) if author_elem else ""
            published_date = date_elem.get_text(strip=True) if date_elem else ""

            if title and link:
                article_id = self._generate_id(link, title)
                self.db_manager.insert_data("articles", {
                    "id": article_id,
                    "source_type": "industry_news",
                    "source_url": link,
                    "title": title,
                    "content": summary,
                    "author": author,
                    "published_date": published_date,
                    "tags": "",
                    "extra_metadata": ""
                })
                articles_data.append({"id": article_id, "title": title, "url": link})
        return articles_data

    def scrape_trending_topics(self, url, selectors=None):
        logging.info(f"Scraping trending topics: {url}")
        soup = self._fetch_page(url)
        if not soup: return

        current_selectors = selectors if selectors else self.default_selectors["trending"]
        trending_data = []
        for item_container in soup.select(current_selectors["item_container"]):
            title_elem = item_container.select_one(current_selectors["title"])
            link_elem = item_container.select_one(current_selectors["link"])
            score_elem = item_container.select_one(current_selectors["score"])

            title = title_elem.get_text(strip=True) if title_elem else ""
            link = urljoin(url, link_elem['href']) if link_elem and 'href' in link_elem.attrs else ""
            score = score_elem.get_text(strip=True) if score_elem else ""

            if title and link:
                item_id = self._generate_id(link, title)
                self.db_manager.insert_data("articles", {
                    "id": item_id,
                    "source_type": "trending",
                    "source_url": link,
                    "title": title,
                    "content": f"Score: {score}",
                    "author": "",
                    "published_date": "",
                    "tags": "trending",
                    "extra_metadata": json.dumps({"score": score})
                })
                trending_data.append({"id": item_id, "title": title, "url": link})
        return trending_data

    def scrape_competitor_blog(self, url, competitor_name, selectors=None):
        logging.info(f"Scraping competitor blog: {url}")
        soup = self._fetch_page(url)
        if not soup: return

        current_selectors = selectors if selectors else self.default_selectors["competitor"]
        articles_data = []
        for article_container in soup.select(current_selectors["article_container"]):
            title_elem = article_container.select_one(current_selectors["title"])
            link_elem = article_container.select_one(current_selectors["link"])
            summary_elem = article_container.select_one(current_selectors["summary"])
            author_elem = article_container.select_one(current_selectors["author"])
            date_elem = article_container.select_one(current_selectors["date"])

            title = title_elem.get_text(strip=True) if title_elem else ""
            link = urljoin(url, link_elem['href']) if link_elem and 'href' in link_elem.attrs else ""
            summary = summary_elem.get_text(strip=True) if summary_elem else ""
            author = author_elem.get_text(strip=True) if author_elem else ""
            published_date = date_elem.get_text(strip=True) if date_elem else ""

            if title and link:
                article_id = self._generate_id(link, title)
                self.db_manager.insert_data("articles", {
                    "id": article_id,
                    "source_type": "competitor",
                    "source_url": link,
                    "title": title,
                    "content": summary,
                    "author": author,
                    "published_date": published_date,
                    "tags": f"competitor:{competitor_name}",
                    "extra_metadata": ""
                })
                articles_data.append({"id": article_id, "title": title, "url": link})
        return articles_data

    def scrape_forum_listing(self, url, selectors=None):
        logging.info(f"Scraping forum listing: {url}")
        soup = self._fetch_page(url)
        if not soup: return

        current_selectors = selectors if selectors else self.default_selectors["forum_listing"]
        threads_data = []
        for thread_container in soup.select(current_selectors["thread_container"]):
            title_elem = thread_container.select_one(current_selectors["title"])
            link_elem = thread_container.select_one(current_selectors["link"])
            author_elem = thread_container.select_one(current_selectors["author"])
            reply_count_elem = thread_container.select_one(current_selectors["reply_count"])

            title = title_elem.get_text(strip=True) if title_elem else ""
            link = urljoin(url, link_elem['href']) if link_elem and 'href' in link_elem.attrs else ""
            author = author_elem.get_text(strip=True) if author_elem else ""
            reply_count = reply_count_elem.get_text(strip=True) if reply_count_elem else "0"

            if title and link:
                thread_id = self._generate_id(link, title)
                self.db_manager.insert_data("articles", {
                    "id": thread_id,
                    "source_type": "ugc_forum_listing",
                    "source_url": link,
                    "title": title,
                    "content": f"Replies: {reply_count}",
                    "author": author,
                    "published_date": "",
                    "tags": "ugc,forum",
                    "extra_metadata": json.dumps({"reply_count": reply_count})
                })
                threads_data.append({"id": thread_id, "title": title, "url": link})
        return threads_data

    def scrape_forum_thread(self, url, selectors=None):
        logging.info(f"Scraping forum thread: {url}")
        soup = self._fetch_page(url)
        if not soup: return

        current_selectors = selectors if selectors else self.default_selectors["forum_thread"]
        posts_data = []
        for post_container in soup.select(current_selectors["post_container"]):
            author_elem = post_container.select_one(current_selectors["author"])
            content_elem = post_container.select_one(current_selectors["content"])
            date_elem = post_container.select_one(current_selectors["date"])

            author = author_elem.get_text(strip=True) if author_elem else ""
            content = content_elem.get_text(strip=True) if content_elem else ""
            published_date = date_elem.get_text(strip=True) if date_elem else ""

            if content:
                post_id = self._generate_id(url + content[:50], content) # Use part of content for ID
                self.db_manager.insert_data("articles", {
                    "id": post_id,
                    "source_type": "ugc_forum_post",
                    "source_url": url,
                    "title": content[:100], # Use first 100 chars as title
                    "content": content,
                    "author": author,
                    "published_date": published_date,
                    "tags": "ugc,forum,post",
                    "extra_metadata": ""
                })
                posts_data.append({"id": post_id, "title": content[:100], "url": url})
        return posts_data

    def collect_all(self, sources):
        all_collected_data = []
        for source_type, source_configs in sources.items():
            for config in source_configs:
                url = config["url"]
                selectors = config.get("selectors")
                competitor_name = config.get("competitor_name")

                if source_type == "news_site":
                    all_collected_data.extend(self.scrape_news_site(url, selectors))
                elif source_type == "trending":
                    all_collected_data.extend(self.scrape_trending_topics(url, selectors))
                elif source_type == "competitor_blog":
                    if competitor_name:
                        all_collected_data.extend(self.scrape_competitor_blog(url, competitor_name, selectors))
                    else:
                        logging.warning(f"Competitor name missing for competitor_blog source: {url}")
                elif source_type == "ugc_forum_listing":
                    all_collected_data.extend(self.scrape_forum_listing(url, selectors))
                elif source_type == "ugc_forum_thread":
                    all_collected_data.extend(self.scrape_forum_thread(url, selectors))
                else:
                    logging.warning(f"Unknown source type: {source_type}")
        return all_collected_data