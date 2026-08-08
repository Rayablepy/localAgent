import sqlite3
from tools.tools import tool_list
from config.settings import ENABLED_TOOLS, PROJECT_ROOT
from agent.system_prompt import build_system_prompt
from config.settings import CHAT_MODEL_NAME, DB_PATH
from langchain.chat_models import init_chat_model
from deepagents import create_deep_agent
from deepagents.backends import FilesystemBackend,CompositeBackend,StateBackend, StoreBackend
from langgraph.store.sqlite.aio import AsyncSqliteStore


model = init_chat_model(
        model=CHAT_MODEL_NAME,
        model_provider="openai",
        base_url="http://localhost:1234/v1",
        api_key="not-needed",
        temperature=0.5
)
tools=tool_list

DB_PATH.parent.mkdir(parents=True,exist_ok=True)
conn=sqlite3.connect(DB_PATH,check_same_thread=False)
local_store = AsyncSqliteStore(conn)
local_store.setup()

backend=CompositeBackend(
    default=StateBackend(),
    routes={
        "/longtermmemories/": StoreBackend(store=local_store,namespace=lambda _: ("localAgent","longterm")),
        "/project/": FilesystemBackend(root_dir=PROJECT_ROOT,virtual_mode=True)
    }
)
agent = create_deep_agent(model=model,system_prompt=build_system_prompt(ENABLED_TOOLS),tools=tools,backend=backend)

async def response(message:str):
    return await agent.ainvoke(
        {"messages": [{"role": "user", "content": message}]},
    )
