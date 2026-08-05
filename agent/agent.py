from tools.tools import tool_list
from config.settings import ENABLED_TOOLS
from agent.system_prompt import build_system_prompt
from config.settings import CHAT_MODEL_NAME
from langchain.chat_models import init_chat_model
from deepagents import create_deep_agent
from langgraph.checkpoint.memory import InMemorySaver
from deepagents.middleware.filesystem import FileSystemMiddleware
from langchain.agents.middleware import ToDoListMiddleware
checkpointer = InMemorySaver()
model = init_chat_model(
        model=CHAT_MODEL_NAME,
        model_provider="openai",
        base_url="http://localhost:1234/v1",
        api_key="not-needed",
        temperature=0.5
)
tools=tool_list
middleware = [ToDoListMiddleware(),FileSystemMiddleware()]
agent = create_deep_agent(model=model,system_prompt=build_system_prompt(ENABLED_TOOLS),tools=tools,middleware=middleware)

async def response(message:str):
    return await agent.ainvoke(
        {"messages": [{"role": "user", "content": message}]},
    )
