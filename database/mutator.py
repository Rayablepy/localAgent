import sqlite3

def add_item(connection):
    cursor = connection.cursor()
    cursor.execute(
        "INSERT INTO TodoList (name, information, timestamp) VALUES (?, ?, ?)",
        ("Write report", "write user's report","2024")
    )
    connection.commit()