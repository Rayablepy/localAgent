from langchain.chat_models import init_chat_model
from deepagents import create_deep_agent

model = create_deep_agent(init_chat_model(
        model="running-model",
        model_provider="openai",
        base_url="http://localhost:1234/v1",
        api_key="not-needed",
        temperature=0.6
    ))

