from tools.rag import query_data
from tools.todo import todo_tool_list
from tools.web_fetch import web_fetch
from tools.web_controller import browser_tools

tool_list = [
    query_data,
    *todo_tool_list,
    web_fetch,
    *browser_tools
]
