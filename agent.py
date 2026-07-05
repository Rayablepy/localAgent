import asyncio
from langchain.chat_models import init_chat_model
from deepagents import create_deep_agent

model = init_chat_model(
        model="running-model",
        model_provider="openai",
        base_url="http://localhost:1234/v1",
        api_key="not-needed",
        temperature=0.5
)
system="""
You are the user's personal AI assistant running locally on their computer. Your tools are not yet created, but you will 
be able to accept and read documents and files that the user gives you
"""


agent = create_deep_agent(model=model,system_prompt=system)

async def response(message:str):
    return await agent.ainvoke(
        {"messages": [{"role": "user", "content": message}]},
    )

while True:
    user = str(input("Enter prompt: ")).lower()
    if user == "q":
        break
    print("-"*100)
    modelresponse = asyncio.run(response(user))
    print(modelresponse["messages"][-1].content_blocks[0]["text"])
    print("-"*100)



