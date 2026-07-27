import os
from dotenv import load_dotenv
load_dotenv()
CHAT_MODEL_NAME=os.getenv("CHAT_MODEL_NAME")
ACTUAL_FILE_PATH="./user_data/"
EMBEDDING_MODEL_NAME=os.getenv("EMBEDDING_MODEL_NAME")
EMBEDDING_MODEL_CONTEXT=int(os.getenv("EMBEDDING_MODEL_CONTEXT", 512))
EMBEDDING_MODEL_CHUNK=int(os.getenv("EMBEDDING_MODEL_CHUNK", 64))
