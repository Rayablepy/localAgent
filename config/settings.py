
from pathlib import Path
#tool list that agent will have access to, update when tools are added or removed
ENABLED_TOOLS: list[str] = [
    # "rag",
    # "filesystem",
    # "notes",
    # "calendar",
    # "web",
]

# directory that file system tool has access to
WORKSPACE_ROOT = Path.home() / "localAgent-workspace"

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

DB_DIR = Path.home() / "localAgent-workspace" / "localAgent.db"
CHROMA_PERSIST_DIR = Path(__file__).resolve().parent.parent / "chroma_langchain_db"

# Retrieval

RAG_CHUNK_SIZE = 1000
RAG_CHUNK_OVERLAP = 200
RAG_TOP_K = 4

# Web tool limits (not yet implemented)

WEB_SEARCH_MAX_RESULTS = 5
WEB_FETCH_TIMEOUT_SECONDS = 15