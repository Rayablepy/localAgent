import sqlite3 as sql
import datetime

db = open("history.db","w")
conn=sql.connect("history.db")
cursor = conn.cursor()

conn.execute("CREATE TABLE IF NOT EXISTS messages (content TEXT, origin TEXT, timestamp DATETIME)")
conn.commit()
def add(content:str,origin:str,timestamp:datetime.datetime):
    cursor.execute(
        "INSERT INTO messages VALUES (?,?,?)",(content,origin,timestamp)
    )
    conn.commit()

def readall():
    cursor.execute("SELECT * FROM messages")
    return cursor.fetchall()


