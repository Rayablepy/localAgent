from langchain.agents import create_agent

model = create_agent(
    model="ollama:qwen3.5:0.8b",
    system_prompt="You are my helpful assistant"
)

while True:
    user = str(input("Prompt or q to quit: "))
    if user.lower() == "q":
        break
    result = model.invoke(
        {"messages": [{"role": "user", "content": user}]}
    )
    print(result["messages"][-1].content_blocks)