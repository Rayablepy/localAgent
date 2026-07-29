import sqlite3
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
DB_PATH = SCRIPT_DIR / "database.db"

conn = sqlite3.connect(DB_PATH)

cursor=conn.cursor()
cursor.execute(
    "CREATE TABLE IF NOT EXISTS TodoList ("
    "id INTEGER PRIMARY KEY, name TEXT NOT NULL, information TEXT NOT NULL, timestamp TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,complete BOOLEAN DEFAULT 0)"
)
try:
    conn.commit()
    print("Table created successfully")
except sqlite3.OperationalError:
    print("Error executing table creation")
