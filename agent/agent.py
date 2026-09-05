import asyncio

from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
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

model = init_chat_model(
    model=CHAT_MODEL_NAME,
    model_provider=MODEL_PROVIDER,
    base_url=MODEL_BASE_URL,
    api_key=OPENROUTER_API_KEY,
    model_kwargs={"extra_body": {"provider": {"max_price": {"prompt": 0, "completion": 0}}}},
)

store = None
store_context_manager = None
backend=None
agent=None

async def build_agent():
    global store
    global store_context_manager
    global backend
    global agent
    if agent:
        return agent
    store_context_manager = AsyncSqliteStore.from_conn_string(DB_PATH)
    store = await store_context_manager.__aenter__()
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
        tools=tool_list,
        backend=backend,
        store=store,
    )

    return agent

EMPTY_RESPONSE_FOLLOWUP = (
    "Your previous response was empty. "
    "Please reply to my request now with a written answer."
)
FALLBACK_RESPONSE = "I wasn't able to generate a response. Please rephrase or try again."


def text_builder(blocks):
    texts = []
    for block in blocks:
        if isinstance(block, str):
            if block.strip():
                texts.append(block)
        elif isinstance(block, dict):
            btype = block.get("type")
            if btype in ("text", "thinking", "reasoning") and isinstance(block.get("text"), str) and block["text"].strip():
                texts.append(block["text"])
            elif btype == "reasoning" and isinstance(block.get("summary"), list):
                for s in block["summary"]:
                    if isinstance(s, str) and s.strip():
                        texts.append(s)
                    elif isinstance(s, dict) and isinstance(s.get("text"), str) and s["text"].strip():
                        texts.append(s["text"])
    return "\n".join(texts).strip()


def message_text(m):

    content = getattr(m, "content", None)
    if isinstance(content, str) and content.strip():
        return content.strip()
    if isinstance(content, list):
        text = text_builder(content)
        if text:
            return text
    content_blocks = getattr(m, "content_blocks", None)
    if content_blocks:
        text = text_builder(content_blocks)
        if text:
            return text
    extra = getattr(m, "additional_kwargs", None) or {}
    for key in ("reasoning_content", "reasoning_details"):
        val = extra.get(key)
        if isinstance(val, str) and val.strip():
            return val.strip()
    return ""

def extract_answer(state):
    for m in reversed(state.get("messages", [])):
        if isinstance(m, (HumanMessage, SystemMessage)):
            continue
        text = message_text(m)
        if text:
            return text
    return ""

async def response(message: str):
    agent = await build_agent()
    state = await agent.ainvoke({"messages": [{"role": "user", "content": message}]})
    if not extract_answer(state):
        followup = {"role": "user", "content": EMPTY_RESPONSE_FOLLOWUP}
        state = await agent.ainvoke({"messages": [*state.get("messages", []), followup]})
    final = extract_answer(state) or FALLBACK_RESPONSE
    last = state.get("messages", [])[-1]
    if isinstance(last, AIMessage):
        last.content = final
        last.tool_calls = []
        last.tool_call_chunks = []
    return state