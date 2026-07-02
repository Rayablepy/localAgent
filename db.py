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
    def querydb(self,query):
        try:
            cursor=self.conn.cursor()
            cursor.execute(query)
            self.conn.commit()
            return cursor
        except sql.Error as e:
            print(f"Db encountered error: {e}")
            if self.conn:
                self.conn.rollback()
            return None
    def close(self):
        if self.conn:
            self.conn.close()

class MessageTable:
    def __init__(self,db_manager: DBManager):
        self.db = db_manager
        self._setup_table()

        def _setup_table(self):
            create_table = """
            CREATE TABLE IF NOT EXISTS messages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                content TEXT NOT NULL,
                origin TEXT NOT NULL,
                timestamp DATETIME NOT NULL,
            
            """
            self.db.querydb(create_table)

        def insert(self,content:str,origin:str,timestamp:datetime.datetime):






