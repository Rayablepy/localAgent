import sqlite3
from pathlib import Path
SCRIPT_DIR = Path(__file__).resolve().parent
DB_PATH = SCRIPT_DIR / "database.db"

conn = sqlite3.connect(DB_PATH)

cursor=conn.cursor()
