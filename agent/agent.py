
from config.settings import ENABLED_TOOLS
from system_prompt import build_system_prompt
from modelloader import chatmodelname
import asyncio
from langchain.chat_models import init_chat_model
from deepagents import create_deep_agent
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.graph import StateGraph

checkpointer = InMemorySaver()
model = init_chat_model(
        model=chatmodelname,
        model_provider="openai",
        base_url="http://localhost:1234/v1",
        api_key="not-needed",
        temperature=0.5
)

agent = create_deep_agent(model=model,system_prompt=build_system_prompt(ENABLED_TOOLS))

async def response(message:str):
    return await agent.ainvoke(
        {"messages": [{"role": "user", "content": message}]},
    )

while True:
    user = str(input("Enter prompt: ")).lower()
    if user == "q":
        break
    print("-"*75)
    modelresponse = asyncio.run(response(user))
    print(modelresponse["messages"][-1].content_blocks[0]['text'])
    print("-"*75)



