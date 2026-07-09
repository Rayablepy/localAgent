# localAgent

A local-first personal AI assistant built on [LangChain Deep Agents](https://docs.langchain.com/oss/python/deepagents/overview) and LangGraph, running entirely on your own machine via a local model server (LM Studio).

The goal: an assistant with real memory, real tools, and real access to your own files and data — without sending everything to a third-party API.

---

## Overview

`localAgent` combines three subsystems into one coherent assistant:

- **Agent core** — a Deep Agent (planning, sub-agents, context management) served by a local LLM
- **Retrieval (RAG)** — a local vector store over your own documents, exposed to the agent as a tool
- **Tools & persistence** — filesystem, notes, calendar, and other tools, backed by local storage

---

## Features

### Current
- [x] Local model serving via LM Studio (OpenAI-compatible API)
- [x] Deep Agent core with planning and context management (via `deepagents`)
- [x] Local document embedding and retrieval pipeline (Chroma)

### In progress / planned
- [ ] Conversational memory across sessions (LangGraph checkpointer)
- [ ] RAG exposed as an agent tool (not a standalone script)
- [ ] Scoped filesystem access tool
- [ ] Notes / todo tool with local persistence
- [ ] Web search tool
- [ ] Chat UI (Streamlit)
- [ ] Calendar and email integration (read-only first)
- [ ] MCP server support for third-party apps
- [ ] Human-in-the-loop approval for sensitive actions (sending messages, deleting files, running shell commands)
- [ ] Voice input/output

---

## Architecture

```
User ──▶ UI (CLI / Streamlit) ──▶ Agent Core (deepagents) ──▶ Tools ──▶ Local data
                                          │
                                          ▼
                                   Local LLM (LM Studio)
```

The agent core never talks to the outside world directly — everything it can see or do is mediated through an explicit tool, each scoped to a specific directory, API, or data source. Sensitive tools (sending, deleting, executing) require human approval before running.

---

## Project Structure

```
localAgent/
├── agent/
│   ├── core.py            # agent construction (create_deep_agent)
│   └── system_prompt.py   # system prompt as a standalone template
├── tools/
│   ├── rag_tools.py
│   ├── filesystem_tools.py
│   ├── notes_tools.py
│   ├── calendar_tools.py
│   └── web_tools.py
├── memory/
│   ├── vectorstore.py     # embedding + indexing
│   └── checkpointer.py    # session/state persistence
├── db/
│   └── manager.py         # local SQLite persistence
├── ui/
│   ├── cli.py
│   └── streamlit_app.py
├── config/
│   ├── modelloader.py
│   └── settings.py        # tool toggles, sandboxed paths, permissions
├── seed-data/              # sample documents for local RAG
└── tests/
```

---

## Tech Stack

| Layer | Choice |
|---|---|
| Agent framework | LangChain `deepagents` + LangGraph |
| Local model serving | LM Studio (OpenAI-compatible endpoint) |
| Vector store | Chroma |
| Persistence | SQLite |
| UI | Streamlit |

---

## Roadmap

**Milestone 1 — Stable core**
Agent runs with persistent memory across turns; RAG works as a proper tool call, not a side effect of import.

**Milestone 2 — Personal assistant baseline**
Filesystem access, notes/todos, and web search available as tools; conversation history persisted and viewable.

**Milestone 3 — Connected assistant**
Calendar and email integrated (read-only); MCP support for external apps.

**Milestone 4 — Safe autonomy**
Human-in-the-loop approval on all state-changing tools; sandboxed permissions defined in config rather than left to the prompt.

**Milestone 5 — Full assistant experience**
Streamlit UI polished; optional voice I/O; sub-agents for heavier delegated tasks (e.g. research).

---

## Getting Started

```bash
git clone https://github.com/Rayablepy/localAgent.git
cd localAgent
pip install -r requirements.txt
cp .env.example .env   # set CHAT_MODEL and EMBEDDING_MODEL to your LM Studio model names
```

Requires [LM Studio](https://lmstudio.ai/) (or another OpenAI-compatible local server) running at `http://localhost:1234/v1` with a chat model and an embedding model loaded.

```bash
python agent.py
```

---

## Design Principles

- **Local-first** — no data leaves the machine unless a tool explicitly calls an external API, and that should be visible and intentional.
- **Tool-scoped, not prompt-scoped** — permissions and boundaries live in code (sandboxed paths, allowed actions), not in instructions the model is asked to follow.
- **Approve before acting** — anything irreversible (send, delete, execute) requires explicit confirmation.
- **Composable, not monolithic** — agent, retrieval, and persistence are separate modules that plug into the agent core via tools, not tangled together.

---

## License

TBD
