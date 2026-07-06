from langchain_core.documents import Document
from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma

documents = [
    Document(
        page_content="User likes python",
        metadata={"source":"seed-data"}
    )
]

embeddings = OpenAIEmbeddings(
    model="nomic-ai/nomic-embed-text-v1.5-GGUF",
    openai_api_base="http://localhost:1234/v1",
    openai_api_key="lm-studio",
    check_embedding_ctx_length=False#prevents remote context checking
)

vector = embeddings.embed_query(documents[0].page_content)

assert vector is not None

vector_storage = Chroma(
    collection_name="localAgent-vectordb",
    enbedding_function = embeddings,
    persist_directory="./chroma_langchain_db"
)
#print(f"Generated vectors:\n{vector}")