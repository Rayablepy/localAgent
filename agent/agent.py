import asyncio
from tools.tools import tool_list
from config.settings import ENABLED_TOOLS, PROJECT_ROOT, MODEL_BASE_URL, MODEL_PROVIDER
from agent.system_prompt import build_system_prompt
from config.settings import CHAT_MODEL_NAME, DB_PATH, OPENROUTER_API_KEY
from langchain.chat_models import init_chat_model
from deepagents import create_deep_agent
from deepagents.backends import FilesystemBackend,CompositeBackend,StateBackend, StoreBackend
from langgraph.store.sqlite.aio import AsyncSqliteStore

DB_PATH.parent.mkdir(parents=True,exist_ok=True)
PROJECT_ROOT.mkdir(parents=True,exist_ok=True)
'''
model = init_chat_model(
    model=CHAT_MODEL_NAME,
    model_provider=MODEL_PROVIDER,
    base_url=MODEL_BASE_URL,
    api_key=OPENROUTER_API_KEY,
    model_kwargs={"extra_body": {"provider": {"max_price": {"prompt": 0, "completion": 0}}}},
)
tools=tool_list
async def response(message: str):
    async with AsyncSqliteStore.from_conn_string(DB_PATH) as store:
        await store.setup()
        backend=CompositeBackend(
            default=StateBackend(),
            routes={
                "/longtermmemories/": StoreBackend(store=store,namespace=lambda _: ("localAgent","longterm")),
                "/project/": FilesystemBackend(root_dir=PROJECT_ROOT,virtual_mode=True)
            }
        )
        agent = create_deep_agent(
            model=model,
            system_prompt=build_system_prompt(ENABLED_TOOLS),
            memory=["/longtermmemories/AGENTS.md"],
            tools=tools,
            backend=backend,
            store=store,
        )
        result = await agent.ainvoke(
            {"messages": [{"role": "user", "content": message}]},
        )
        await asyncio.sleep(0)
        return result
        '''
store = None
backend=None
agent=None

async def build_agent():
    global store
    global backend
    global agent
    if not agent:
        return agent
    store=AsyncSqliteStore.from_conn_string(DB_PATH)
    await store.__aenter__()
    await store.setup()
    backend=backend=CompositeBackend(
            default=StateBackend(),
            routes={
                "/longtermmemories/": StoreBackend(store=store,namespace=lambda _: ("localAgent","longterm")),
                "/project/": FilesystemBackend(root_dir=PROJECT_ROOT,virtual_mode=True)
            }
        )
