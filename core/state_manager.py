import sqlite3
from core.config import DB_PATH

class StateManager:
    def __init__(self):
        self.db_path = DB_PATH
        self._init_db()

    def _init_db(self):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''CREATE TABLE IF NOT EXISTS file_events (id INTEGER PRIMARY KEY, timestamp DATETIME DEFAULT CURRENT_TIMESTAMP, event_type TEXT, file_path TEXT, process_name TEXT)''')
            cursor.execute('''CREATE TABLE IF NOT EXISTS system_status (id INTEGER PRIMARY KEY CHECK (id = 1), status TEXT, last_updated DATETIME DEFAULT CURRENT_TIMESTAMP)''')
            cursor.execute('''CREATE TABLE IF NOT EXISTS honey_assets (filename TEXT PRIMARY KEY)''')
            cursor.execute('''CREATE TABLE IF NOT EXISTS traceback_logs (id INTEGER PRIMARY KEY, log_text TEXT)''')
            cursor.execute("INSERT OR IGNORE INTO system_status (id, status) VALUES (1, 'Normal')")
            conn.commit()

    def register_honey_asset(self, filename: str):
        with sqlite3.connect(self.db_path) as conn:
            conn.cursor().execute("INSERT OR IGNORE INTO honey_assets (filename) VALUES (?)", (filename,))
            conn.commit()

    def is_honey_asset(self, filename: str) -> bool:
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT filename FROM honey_assets WHERE filename = ?", (filename,))
            return cursor.fetchone() is not None

    def log_event(self, event_type: str, file_path: str, process_name: str):
        with sqlite3.connect(self.db_path) as conn:
            conn.cursor().execute("INSERT INTO file_events (event_type, file_path, process_name) VALUES (?, ?, ?)", (event_type, file_path, process_name))
            conn.commit()

    def update_status(self, status: str):
        with sqlite3.connect(self.db_path) as conn:
            conn.cursor().execute("UPDATE system_status SET status = ?, last_updated = CURRENT_TIMESTAMP WHERE id = 1", (status,))
            conn.commit()

    def get_status(self) -> str:
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT status FROM system_status WHERE id = 1")
            row = cursor.fetchone()
            return row[0] if row else "Normal"

    def add_traceback_log(self, text: str):
        with sqlite3.connect(self.db_path) as conn:
            conn.cursor().execute("INSERT INTO traceback_logs (log_text) VALUES (?)", (text,))
            conn.commit()

    def get_traceback_logs(self):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT log_text FROM traceback_logs ORDER BY id ASC")
            return [row[0] for row in cursor.fetchall()]
