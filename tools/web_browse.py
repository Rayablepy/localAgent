from langchain.chat_models import init_chat_model
from langchain_core.tools import tool
from langchain.agents import create_agent
from config.settings import SUBAGENT_MODEL_NAME

subagent_model = init_chat_model(
        model=SUBAGENT_MODEL_NAME,
        model_provider="openai",
        base_url="http://localhost:1234/v1",
        api_key="not-needed",
        temperature=0.3
)

subagent = create_agent(model=subagent_model)
@tool
def web_browse(instructions: str)->str:
    result=subagent.invoke({"messages": [{"role": "user", "content": instructions}]})
    return result
