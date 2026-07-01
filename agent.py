from langchain.chat_models import init_chat_model

model = init_chat_model(
    model="running-model",
    model_provider="lmstudio",
    base_url="http://localhost:1234/v1",
    api_key="not-needed",
    temperature=0.6
)

async def model_response(text:str):
    response = await model.invoke(text)
    return str(response)