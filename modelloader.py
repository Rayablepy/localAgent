
import os
from dotenv import load_dotenv
load_dotenv()

chatmodelname_restricted = os.getenv('CHAT_MODEL')
embeddingmodelname_restricted = os.getenv('EMBEDDING_MODEL')
if chatmodelname_restricted is None or embeddingmodelname_restricted is None:
    raise EnvironmentError("CHAT_MODEL or EMBEDDING_MODEL environment variables not set")
else:
    chatmodelname=chatmodelname_restricted
    embeddingmodelname=embeddingmodelname_restricted

