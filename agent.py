from langchain.chat_models import init_chat_model
import streamlit as st
@st.cache_resource
def model():
    return init_chat_model(
        model="running-model",
        model_provider="openai",
        base_url="http://localhost:1234/v1",
        api_key="not-needed",
        temperature=0.6
    )
model = model()
def model_response(text:str):
    return model.stream(text)
