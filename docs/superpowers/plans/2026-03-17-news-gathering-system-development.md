# 新闻采集系统开发计划

> **For agentic workers:** REQUIRED: Use superpowers:subagent-driven-development (if subagents available) or superpowers:executing-plans to implement this plan. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Develop a comprehensive news gathering system to provide inspiration for WeChat official account articles, meeting specific measurable objectives for industry news, trending topics, competitor content, and UGC analysis.

**Architecture:** The system will consist of modules for data acquisition, processing, analysis, and output. It will leverage web scraping and natural language processing (NLP) for sentiment and topic analysis.

**Tech Stack:** Python, BeautifulSoup, Requests, NLTK/spaCy, SQLite.

---

### Task 1: 项目初始化与基础结构搭建

**Files:**
- Create: `news_gathering_system/` (directory)
- Create: `news_gathering_system/__init__.py`
- Create: `news_gathering_system/main.py`
- Create: `news_gathering_system/config.py`
- Create: `requirements.txt`
- Create: `README.md`

- [ ] **Step 1: 创建项目根目录和基本文件**

```bash
mkdir news_gathering_system
touch news_gathering_system/__init__.py
touch news_gathering_system/main.py
touch news_gathering_system/config.py
touch requirements.txt
touch README.md
```

- [ ] **Step 2: 编写 `requirements.txt`**

```
requests
beautifulsoup4
nltk
# spaCy (optional, for more advanced NLP)
# pandas (for data handling)
```

- [ ] **Step 3: 编写 `config.py` 初始内容**

```python
# Configuration settings for the news gathering system
DATABASE_PATH = 'news_data.db'
LOG_FILE = 'news_gathering.log'
```

- [ ] **Step 4: 编写 `main.py` 初始内容**

```python
# Main entry point for the news gathering system
def run_system():
    print("News Gathering System started.")
    # Future: Orchestrate data acquisition, processing, analysis

if __name__ == "__main__":
    run_system()
```

- [ ] **Step 5: 编写 `README.md` 初始内容**

```markdown
# News Gathering System

This system is designed to collect news and content inspiration for WeChat official account articles.

## Features (Planned)
- Industry News Acquisition
- Trending Topics Monitoring
- Competitor Content Analysis
- User-Generated Content (UGC) Analysis

## Setup
1. Clone the repository.
2. Install dependencies: `pip install -r requirements.txt`
3. Run the system: `python news_gathering_system/main.py`
```

- [ ] **Step 6: 提交初始项目结构**

```bash
git add news_gathering_system/ requirements.txt README.md
git commit -m "feat: Initialize project structure and basic files"
```

### Task 2: 数据存储模块设计与实现

**Files:**
- Create: `news_gathering_system/storage/` (directory)
- Create: `news_gathering_system/storage/__init__.py`
- Create: `news_gathering_system/storage/database_manager.py`
- Create: `tests/test_database_manager.py`

- [ ] **Step 1: 创建数据存储目录和文件**

```bash
mkdir news_gathering_system/storage
touch news_gathering_system/storage/__init__.py
touch news_gathering_system/storage/database_manager.py
mkdir tests
touch tests/test_database_manager.py
```

- [ ] **Step 2: 编写 `tests/test_database_manager.py` 的 failing test**

```python
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
```

- [ ] **Step 3: 运行测试以验证其失败**

Run: `pytest tests/test_database_manager.py -v`
Expected: FAIL with "ModuleNotFoundError: No module named 'news_gathering_system.storage.database_manager'" or similar, as the implementation is not yet present.

- [ ] **Step 4: 编写 `news_gathering_system/storage/database_manager.py` 的最小实现**

```python
import sqlite3
import logging
from news_gathering_system.config import DATABASE_PATH

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class DatabaseManager:
    def __init__(self, db_path=DATABASE_PATH):
        self.db_path = db_path
        self.conn = None
        self.connect()

    def connect(self):
        try:
            self.conn = sqlite3.connect(self.db_path)
            logging.info(f"Connected to database: {self.db_path}")
        except sqlite3.Error as e:
            logging.error(f"Database connection error: {e}")
            self.conn = None

    def close_connection(self):
        if self.conn:
            self.conn.close()
            logging.info("Database connection closed.")

    def create_table(self, table_name, columns):
        if not self.conn:
            logging.error("No database connection to create table.")
            return

        column_defs = ", ".join([f"{name} {type_def}" for name, type_def in columns.items()])
        query = f"CREATE TABLE IF NOT EXISTS {table_name} ({column_defs})"
        try:
            cursor = self.conn.cursor()
            cursor.execute(query)
            self.conn.commit()
            logging.info(f"Table '{table_name}' created or already exists.")
        except sqlite3.Error as e:
            logging.error(f"Error creating table '{table_name}': {e}")

    def insert_data(self, table_name, data):
        if not self.conn:
            logging.error("No database connection to insert data.")
            return

        columns = ", ".join(data.keys())
        placeholders = ", ".join(["?" for _ in data.values()])
        query = f"INSERT OR IGNORE INTO {table_name} ({columns}) VALUES ({placeholders})"
        try:
            cursor = self.conn.cursor()
            cursor.execute(query, tuple(data.values()))
            self.conn.commit()
            logging.info(f"Data inserted into '{table_name}'.")
        except sqlite3.Error as e:
            logging.error(f"Error inserting data into '{table_name}': {e}")

    def fetch_data(self, table_name, conditions=None):
        if not self.conn:
            logging.error("No database connection to fetch data.")
            return []

        query = f"SELECT * FROM {table_name}"
        params = []
        if conditions:
            condition_clauses = []
            for col, val in conditions.items():
                condition_clauses.append(f"{col} = ?")
                params.append(val)
            query += " WHERE " + " AND ".肿瘤.join(condition_clauses)

        try:
            cursor = self.conn.cursor()
            cursor.execute(query, tuple(params))
            return cursor.fetchall()
        except sqlite3.Error as e:
            logging.error(f"Error fetching data from '{table_name}': {e}")
            return []
```

- [ ] **Step 5: 运行测试以验证其通过**

Run: `pytest tests/test_database_manager.py -v`
Expected: PASS

- [ ] **Step 6: 提交数据存储模块**

```bash
git add news_gathering_system/storage/ tests/test_database_manager.py
git commit -m "feat: Implement database manager for data storage"
```

### Task 3: 前端界面开发与部署 (Cloudflare)

**Files:**
- Create: `news_gathering_system/frontend/` (directory)
- Create: `news_gathering_system/frontend/index.html`
- Create: `news_gathering_system/frontend/style.css`
- Create: `news_gathering_system/frontend/script.js`
- Modify: `news_gathering_system/main.py` (for serving frontend or API)

- [ ] **Step 1: 创建前端目录和基本文件**

```bash
mkdir news_gathering_system/frontend
touch news_gathering_system/frontend/index.html
touch news_gathering_system/frontend/style.css
touch news_gathering_system/frontend/script.js
```

- [ ] **Step 2: 编写 `news_gathering_system/frontend/index.html` 初始内容**

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>新闻采集系统</title>
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <header>
        <h1>新闻采集系统</h1>
    </header>
    <main>
        <section id="dashboard">
            <h2>灵感仪表盘</h2>
            <!-- Content will be loaded here by script.js -->
        </section>
    </main>
    <footer>
        <p>&copy; 2026 新闻采集系统</p>
    </footer>
    <script src="script.js"></script>
</body>
</html>
```

- [ ] **Step 3: 编写 `news_gathering_system/frontend/style.css` 初始内容**

```css
body {
    font-family: Arial, sans-serif;
    margin: 0;
    padding: 0;
    background-color: #f4f4f4;
    color: #333;
}

header {
    background-color: #333;
    color: #fff;
    padding: 1em 0;
    text-align: center;
}

main {
    padding: 20px;
    max-width: 1200px;
    margin: 20px auto;
    background-color: #fff;
    box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
}

footer {
    text-align: center;
    padding: 1em 0;
    background-color: #333;
    color: #fff;
    position: fixed;
    bottom: 0;
    width: 100%;
}
```

- [ ] **Step 4: 编写 `news_gathering_system/frontend/script.js` 初始内容**

```javascript
document.addEventListener('DOMContentLoaded', () => {
    const dashboard = document.getElementById('dashboard');
    dashboard.innerHTML += '<p>加载灵感数据...</p>';
    // Future: Fetch data from backend API and display
});
```

- [ ] **Step 5: 提交前端基础结构**

```bash
git add news_gathering_system/frontend/
git commit -m "feat: Add basic frontend structure"
```

- [ ] **Step 6: 部署前端到 Cloudflare Pages**

    **前提:** 需要用户提供 Cloudflare 账户的 API Token 和 Zone ID，或者手动在 Cloudflare Pages 上创建项目并连接到此 Git 仓库。

    **假设:** 我们将使用 Cloudflare Pages 的 Git 集成功能进行部署。

    1.  **在 Cloudflare Pages 上创建新项目：**
        *   登录 Cloudflare 仪表盘。
        *   导航到 Pages。
        *   点击“创建项目”并连接到此 Git 仓库。
        *   配置构建设置（通常对于纯静态前端，默认设置即可，或者指定构建命令为 `npm install && npm run build` 如果有构建步骤）。
        *   指定输出目录为 `news_gathering_system/frontend`。
        *   保存并部署。

    2.  **验证部署：**
        *   访问 Cloudflare Pages 提供的预览 URL，确认前端页面正常显示。

- [ ] **Step 7: 更新 `main.py` 以支持前端 (可选，如果后端需要提供API)**

    ```python
    # Modify news_gathering_system/main.py
    # Add a simple web server to serve the frontend or API endpoints
    # Example using Flask (requires 'Flask' in requirements.txt)
    # from flask import Flask, send_from_directory
    #
    # app = Flask(__name__, static_folder='frontend', static_url_path='')
    #
    # @app.route('/')
    # def serve_index():
    #     return send_from_directory(app.static_folder, 'index.html')
    #
    # @app.route('/api/inspirations')
    # def get_inspirations():
    #     # Future: Fetch data from database and return as JSON
    #     return {"data": ["灵感1", "灵感2"]}
    #
    # def run_system():
    #     print("News Gathering System started.")
    #     # If running Flask app:
    #     # app.run(debug=True)
    #
    # if __name__ == "__main__":
    #     run_system()
    ```

- [ ] **Step 8: 提交 `main.py` 更新 (如果进行了修改)**

    ```bash
    git add news_gathering_system/main.py
    git commit -m "feat: Update main.py for frontend serving/API (optional)"
    ```
