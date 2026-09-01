import os
from dotenv import load_dotenv
from pathlib import Path
load_dotenv()

#tool list that agent will have access to, update when tools are added or removed
ENABLED_TOOLS: list[str] = [
    "rag",
    "filesystem",
    "todo/notes",
    # "calendar",
    # "web",
]

CHAT_MODEL_NAME=os.getenv("CHAT_MODEL_NAME")
EMBEDDING_MODEL_NAME=os.getenv("EMBEDDING_MODEL_NAME")

# directory that file system tool has access to (dedicated agent sandbox)
PROJECT_ROOT = Path.home() / "agent_project"

#(not yet fully implemented) read-only directories the agent can look into but never write to
READONLY_PATHS: list[Path] = [
    Path.home() / "Documents",
]

#high risk tools that require approval
REQUIRE_APPROVAL: set[str] = {
    "send_email",
    "delete_file",
    "run_shell_command",
    "create_calendar_event",
    "send_message",
}

# Local model server

LOCAL_MODEL_BASE_URL = "http://localhost:1234/v1"
LOCAL_MODEL_API_KEY = "not-needed"

# Persistence

DB_PATH = Path(__file__).resolve().parent.parent / "database" / "database.db"
CHROMA_PERSIST_DIR = Path(__file__).resolve().parent.parent / "chroma_langchain_db"

# Retrieval

EMBEDDING_MODEL_CONTEXT=int(os.getenv("EMBEDDING_MODEL_CONTEXT", 512))
EMBEDDING_MODEL_CHUNK=int(os.getenv("EMBEDDING_MODEL_CHUNK", 64))
RAG_TOP_K = 4

# Web tool limits (not yet implemented)

WEB_SEARCH_MAX_RESULTS = 5
WEB_FETCH_TIMEOUT_SECONDS = 15
