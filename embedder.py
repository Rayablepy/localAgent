from langchain_core.documents import Document
import pypdf
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma
from modelloader import embeddingmodelname
splitter = RecursiveCharacterTextSplitter(
    chunk_size = 1000,chunk_overlap=200, add_start_index=True
)

def load_pdf(path: str)->list[Document]:
    reader = pypdf.PdfReader(path)
    return [
        Document(
            page_content=page.extract_text() or "",
            metadata={"source": path, "page":i},
        )
    for i, page in enumerate(reader.pages)
    ]

docs = load_pdf("./seed-data/sampledata.pdf")
splits = splitter.split_documents(docs)

embeddings = OpenAIEmbeddings(
    model=embeddingmodelname,
    openai_api_base="http://localhost:1234/v1",
    openai_api_key="lm-studio",
    check_embedding_ctx_length=False#prevents remote context checking
)

vector_storage = Chroma(
    collection_name="localAgent-vectordb",
    embedding_function = embeddings,
    persist_directory="./chroma_langchain_db"
)

ids = vector_storage.add_documents(documents=splits)
async def embedderresult(query:str)->Document:
    result = await vector_storage.asimilarity_search(
        "Skills of user?"
    )
    return result[0]

print(embedderresult(""))