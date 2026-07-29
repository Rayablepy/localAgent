# Web Tools Implementation Plan

## Overview

Two complementary LangChain tools for web access:
1. **`web_fetch`** — lightweight research / content retrieval (httpx + BeautifulSoup + markdownify)
2. **`web_browser`** — full browser automation for forms, logins, JS-heavy pages (browser-use sub-agent)

---

## File Structure

| File | Action |
|------|--------|
| `tools/web_fetch.py` | New — `@tool` for content fetching |
| `tools/web_browser.py` | New — `@tool` wrapping browser-use Agent |
| `tools/tools.py` | Edit — register both tools |
| `config/settings.py` | Edit — enable `"web"`, add `SUBAGENT_MODEL_NAME` |
| `agent/system_prompt.py` | Edit — add `TOOL_NOTES` for `"web"` |
| `.env.example` | Edit — add `SUBAGENT_MODEL_NAME` |
| `pyproject.toml` | Edit — add `markdownify` dependency |

---

## Tool Details

### `web_fetch`

- **Stack**: `httpx` + `BeautifulSoup` + `markdownify`
- **JS**: No (HTTP GET + parse only)
- **Speed**: ~1-3s
- **Security**: Rejects localhost / internal IPs, enforces timeout, caps content length
- **Output**: Clean Markdown
- **Signature**:
  ```python
  @tool
  async def web_fetch(url: str, max_chars: int = 5000) -> str
  ```

### `web_browser`

- **Stack**: `browser-use.Agent` with Playwright (Chromium)
- **JS**: Yes (full browser)
- **Speed**: ~10-60s (sub-agent processes multi-step tasks)
- **Model**: `SUBAGENT_MODEL_NAME` env var → LM Studio endpoint (same base URL as main agent)
- **Security**: Rejects localhost / internal IPs; requires approval for non-HTTPS
- **Lifecycle**: Lazy browser init, reused across calls, cleaned up on shutdown
- **Signature**:
  ```python
  @tool
  async def web_browser(task: str, url: str | None = None) -> str
  ```

---

## Config Changes

### `config/settings.py`

- `SUBAGENT_MODEL_NAME` — read from env, fallback to `"qwen/qwen3.5-9b"` (same as main)
- `ENABLED_TOOLS` — uncomment `"web"`
- `WEB_BROWSER_HEADLESS` — default `True`

### `.env.example`

```
SUBAGENT_MODEL_NAME=qwen/qwen3.5-9b
```

---

## Security Rules

| Restriction | Tool | Behavior |
|---|---|---|
| localhost / 127.0.0.1 / internal IPs | both | Reject with error message |
| Internal ranges (10.x, 172.16-31.x, 192.168.x) | both | Reject with error message |
| Non-HTTPS URLs | `web_browser` | Require user approval before proceeding |
| Non-HTTPS URLs | `web_fetch` | Warn but allow (read-only, no risk) |
| Max content | `web_fetch` | Hard cap at `max_chars` (default 5000) |
| Max steps | `web_browser` | browser-use sub-agent has step limit |

---

## Dependencies to Install

```
pip install markdownify
playwright install chromium
```
