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
            query += " WHERE " + " AND ".join(condition_clauses)

        try:
            cursor = self.conn.cursor()
            cursor.execute(query, tuple(params))
            return cursor.fetchall()
        except sqlite3.Error as e:
            logging.error(f"Error fetching data from '{table_name}': {e}")
            return []