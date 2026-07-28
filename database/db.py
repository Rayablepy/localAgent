import sqlite3
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
DB_PATH = SCRIPT_DIR / "database.db"

conn = sqlite3.connect(DB_PATH)

cursor=conn.cursor()
cursor.execute(
    "CREATE TABLE IF NOT EXISTS TodoList ("
    "id INTEGER PRIMARY KEY, name TEXT, information TEXT, timestamp TEXT,complete BOOLEAN)"
)
try:
    conn.commit()
    print("Table created successfully")
except sqlite3.OperationalError:
    print("Error executing table creation")
