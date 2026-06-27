import os
from langchain_core.documents import Document
import ollama
model = 'qwen3-embedding:0.6b'
documents = [
    Document(
        page_content="User is proficient in AI tools",
        metadata={"source":"user-information"},
    )

]
