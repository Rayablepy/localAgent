import sqlite3
from db import conn
def add_item(connection: sqlite3.Connection, name:str, information:str, timestamp:str):
    cursor = connection.cursor()
    cursor.execute(
        "INSERT INTO TodoList (name, information, timestamp) VALUES (?, ?, ?)",
        (name, information, timestamp)
    )
    connection.commit()

def alter_item_name(connection: sqlite3.Connection, name:str, new_name:str):
    cursor = connection.cursor()
    cursor.execute(
        "UPDATE TodoList SET name = ? WHERE name = ?",
        (new_name, name)
    )
    connection.commit()

def alter_item_description(connection: sqlite3.Connection, name:str, new_description:str):
    cursor = connection.cursor()
    cursor.execute(
        "UPDATE TodoList SET information = ? WHERE name = ?",
        (new_description, name)
    )
    connection.commit()

def alter_item_status(connection: sqlite3.Connection, name:str, complete:int):
    cursor = connection.cursor()
    cursor.execute(
        "UPDATE TodoList SET complete = ? WHERE name = ?",
        (complete, name)
    )
    connection.commit()
