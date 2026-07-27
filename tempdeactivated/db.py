#file temporarily not in use
'''
import sqlite3 as sql
import datetime

class DBManager:
    def __init__(self,db_name):
        self.db_name = db_name
        self.conn = None
        self._connect()
    def _connect(self):
        try:
            self.conn = sql.connect(self.db_name)
        except sql.Error as e:
            print(f"Db encountered error: {e}")
            raise
    def querydb(self,query,params=()):
        try:
            cursor=self.conn.cursor()
            cursor.execute(query,params)
            self.conn.commit()
            return cursor
        except sql.Error as e:
            print(f"Db encountered error: {e}")
            return None
    def close(self):
        if self.conn:
            self.conn.close()

class MessageTable:
    def __init__(self, db_manager: DBManager):
        self.db = db_manager
        self._setup_table()

    def _setup_table(self):
        create_table = """
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            content TEXT NOT NULL,
            origin TEXT NOT NULL,
            timestamp DATETIME NOT NULL
            )
        """
        self.db.querydb(create_table)

    def insert(self, content: str, origin: str, timestamp: datetime.datetime):
        self.db.querydb("""
                        INSERT INTO messages (content,origin,timestamp) VALUES (?, ?, ?)""",
                        (content, origin, timestamp.isoformat()))
        print("Message inserted")

    def get_all(self):
        cursor = self.db.querydb("SELECT * FROM messages ORDER BY timestamp DESC")
        results = []
        if cursor:
            for row in cursor.fetchall():
                results.append({
                    "id": row[0],
                    "content": row[1],
                    "origin": row[2],
                    "timestamp": row[3],
                })
        return results

    def update(self,id: int, content: str, origin: str):
        if not content and not origin and not id:
            print("Parameters not fulfilled")
            return
        self.db.querydb("""
        UPDATE messages SET content=?,origin=? WHERE id = ?
        """,(content,origin,id))
        print("Message updated")

    def delete(self,id:int):
        self.db.querydb(""" 
        DELETE FROM messages where id = ?
        """,(id,))
        if self.db.conn:
            print("Deleted message")
        else:
            print("Encountered error")


db = DBManager("localAgent.db")
message_table = MessageTable(db)
'''


