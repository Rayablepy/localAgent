import sqlite3
from database.db import conn
from langchain_core.tools import tool

@tool
def add_item(name:str, information:str, timestamp:str):
    """Add a new item/task to execute to a todo list.
    Args:
        name (str): The name of the item/task.
        information (str): The description of the item/task.
        timestamp (str): The timestamp of when the item/task was added.
    """
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO TodoList (name, information, timestamp) VALUES (?, ?, ?)",
        (name, information, timestamp)
    )
    conn.commit()

@tool
def alter_item_name(name:str, new_name:str):
    """Alter the name of an item/task in the todo list.
    Args:
        name (str): The name of the item/task.
        new_name (str): The new name of the item/task.
    """
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE TodoList SET name = ? WHERE name = ?",
        (new_name, name)
    )
    conn.commit()

@tool
def alter_item_description(name:str, new_description:str):
    """Alter the description of an item/task in the todo list.
    Args:
        name (str): The name of the item/task.
        new_description (str): The new description of the item/task.
    """
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE TodoList SET information = ? WHERE name = ?",
        (new_description, name)
    )
    conn.commit()

@tool
def alter_item_status(name:str, complete:int):
    """Alter the status of an item/task in the todo list.
    Args:
        name (str): The name of the item/task.
        complete (int): The new status of the item/task. 0 represents incomplete, 1 represents complete. IT CAN ONLY BE 0 OR 1.
    """
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE TodoList SET complete = ? WHERE name = ?",
        (complete, name)
    )
    conn.commit()

@tool
def delete_item(name:str):
    """Delete an item/task from the todo list.
    Args:
        name (str): The name of the item/task.
    """
    cursor = conn.cursor()
    cursor.execute(
        "DELETE FROM TodoList WHERE name = ?",
        (name,)
    )
    conn.commit()

todo_tool_list=[add_item, alter_item_name, alter_item_description, alter_item_status, delete_item]
