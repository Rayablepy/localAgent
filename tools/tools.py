from .todo import todo_tool_list
from .rag import query_data

tool_list = todo_tool_list + [query_data]

print(tool_list)
