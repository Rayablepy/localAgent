import sqlite3
from database.db import conn
from langchain_core.tools import tool
import time
@tool
def add_item(name:str, information:str):
    """Add a new item/task to execute to a todo list.
    Args:
        name (str): The name of the item/task.
        information (str): The description of the item/task.
    Returns:
        str: The name of the item added at the time of execution.
    """
    cursor = conn.cursor()
    timestamp=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    cursor.execute(
        "INSERT INTO TodoList (name, information, timestamp) VALUES (?, ?, ?)",
        (name, information,timestamp)
    )
    conn.commit()
    return f"Item {name} added at {timestamp}"

@tool
def alter_item_name(name:str, new_name:str):
    """Alter the name of an item/task in the todo list.
    Args:
        name (str): The name of the item/task.
        new_name (str): The new name of the item/task.
    Returns:
        str: The name of the item changed and its new name.
    """
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE TodoList SET name = ? WHERE name = ?",
        (new_name, name)
    )
    conn.commit()
    return f"Item {name} changed to {new_name}"
@tool
def alter_item_description(name:str, new_description:str):
    """Alter the description of an item/task in the todo list.
    Args:
        name (str): The name of the item/task.
        new_description (str): The new description of the item/task.
    Returns:
        str: The name of the item changed and its new description.
    """
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE TodoList SET information = ? WHERE name = ?",
        (new_description, name)
    )
    conn.commit()
    return f"Item {name}'s description changed to {new_description}"

@tool
def alter_item_status(name:str, complete:int):
    """Alter the status of an item/task in the todo list.
    Args:
        name (str): The name of the item/task.
        complete (int): The new status of the item/task. 0 represents incomplete, 1 represents complete. IT CAN ONLY BE 0 OR 1.
    Returns:
        str: The name of the item changed and its new status.
    """
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE TodoList SET complete = ? WHERE name = ?",
        (complete, name)
    )
    conn.commit()
    return f"Item {name}'s status changed to {"complete" if complete == 0 else "incomplete"}"

@tool
def delete_item(name:str):
    """Delete an item/task from the todo list.
    Args:
        name (str): The name of the item/task.
    Returns:
        str: The name of the item deleted.
    """
    cursor = conn.cursor()
    cursor.execute(
        "DELETE FROM TodoList WHERE name = ?",
        (name,)
    )
    conn.commit()
    return f"Item {name} deleted"

todo_tool_list=[add_item, alter_item_name, alter_item_description, alter_item_status, delete_item]
