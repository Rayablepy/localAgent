# Web Tools Implementation Plan

## Overview

Two complementary web-access paths, both bound **directly to the main agent** (no sub-agent):

1. **`web_fetch`** — lightweight research / content retrieval (httpx + BeautifulSoup + markdownify)
2. **`browser_*`** — deterministic Playwright action tools for forms, logins, JS-heavy pages

> **Why not browser-use?** browser-use.Agent is a per-step LLM loop: every step re-serializes the page DOM into the LLM context and requires a structured JSON tool call. On a local model that means ~30s-3min *per step*, context overflows quickly (task gets forgotten), and step/LLM timeouts expire. Deterministic Playwright tools eliminate per-step LLM calls — only the main agent's own reasoning is used, and each action executes in milliseconds.

---

## File Structure

| File | Action |
|------|--------|
| `tools/web_fetch.py` | Kept — existing `@tool` for content fetching (already built) |
| `tools/web_browser.py` | Rewrite — Playwright session manager + discrete `browser_*` action tools |
| `tools/web_browse.py` | Kept — browser-use sub-agent, **experimental script only** (`if __name__ == "__main__"`), NOT registered as a tool |
| `tools/tools.py` | Edit — register `browser_*` tools in `tool_list` |
| `config/settings.py` | Edit — enable `"web"`, add browser settings |
| `agent/system_prompt.py` | Edit — add `TOOL_NOTES` for `"web"` + usage guidance |
| `web-tools-plan.md` | This file |

---

## Tool Details

### `web_fetch` (already built, unchanged)

- **Stack**: `httpx` + `BeautifulSoup` + `markdownify`
- **JS**: No (HTTP GET + parse only)
- **Speed**: ~1-3s
- **Use when**: quick reads, articles, docs, research — page doesn't need JS
- **Signature**:
  ```python
  @tool
  async def web_fetch(url: AnyHttpUrl, max_chars: int = 5000) -> str
  ```

### `browser_*` tools (new)

- **Stack**: Playwright (`playwright.async_api`), Chromium, headless
- **JS**: Yes (full browser)
- **Speed**: each action ~ms; a form fill = ~3-4 tool calls, total seconds
- **Binding**: directly to the main agent (plain `@tool`s in `tool_list`)
- **Session**: module-level async singleton — one Chromium browser + one page, lazy init, persisted across tool calls for the process lifetime (navigate → fill → submit works across calls)
- **Element targeting**: numbered elements + visible-text clicks. **No CSS selectors required** — a local model will hallucinate selectors. Numbers and text are reliable.

#### Tool signatures

```python
@tool
async def browser_open(url: str, max_chars: int = 4000) -> str
    # Navigate; returns title + page markdown + numbered table of interactive elements

@tool
async def browser_click(index: int) -> str
    # Click element by its number from the last enumeration; returns fresh page summary + elements

@tool
async def browser_click_text(text: str) -> str
    # Click the element whose visible text matches ("Sign in"); robust for buttons/links

@tool
async def browser_fill(index: int, value: str) -> str
    # Fill an input by its number; returns fresh page summary + elements

@tool
async def browser_select(index: int, option: str) -> str
    # Pick an option in a dropdown; returns fresh page summary + elements

@tool
async def browser_submit() -> str
    # Submit the active form; returns fresh page summary + elements

@tool
async def browser_read(max_chars: int = 5000) -> str
    # Extract current page as markdown (SPA content web_fetch can't reach)

@tool
async def browser_wait(ms: int = 2000) -> str
    # Wait for page load / settle; returns current page summary
```

Every mutating action (`click`, `click_text`, `fill`, `select`, `submit`) re-enumerates the page and returns a **fresh numbered element table** so the agent always targets current state.

#### Element enumeration (internal JS, read-only)

Runs on `browser_open` and after each mutation. Collects interactive elements into a compact table:

| column | meaning |
|---|---|
| index | number the agent references |
| tag/type | `input`, `select`, `textarea`, `button`, `a` |
| label | from `label[for]`, wrapping `<label>`, `aria-label`, `placeholder`, `name`, `id` |
| text | visible text (buttons/links) |
| value | current value if set |

---

## Config Changes

### `config/settings.py`

```python
ENABLED_TOOLS = [
    "rag",
    "todo/notes",
    "web",          # uncomment
]

# Web browser tool settings
WEB_BROWSER_HEADLESS = True            # run Chromium headless
WEB_BROWSER_NAV_TIMEOUT = 30000        # ms, navigation timeout
WEB_ALLOW_HTTP = False                 # block http:// URLs unless user opts in
WEB_READ_MAX_CHARS = 4000              # default page summary length
```

### `.env.example`

- `SUBAGENT_MODEL_NAME` stays (only used by the experimental `web_browse.py` script)

---

## Security Rules

| Restriction | Tool(s) | Behavior |
|---|---|---|
| localhost / 127.0.0.1 / `::1` | both | Reject with error message |
| Private IP ranges (10.x, 172.16-31.x, 192.168.x) | both | Reject with error message |
| Non-http(s) schemes (file:, ftp:, etc.) | both | Reject |
| Hostname resolves to internal IP | both | Reject after DNS resolution (SSRF mitigation) |
| Non-HTTPS URLs | `browser_*` | Block unless `WEB_ALLOW_HTTP=True` |
| Non-HTTPS URLs | `web_fetch` | Warn but allow (read-only, no risk) |
| Max content | both | Hard cap via `max_chars` |
| Raw JS execution | `browser_*` | **Never exposed** — all page JS is internal & read-only |
| Session persistence | `browser_*` | Ephemeral in-memory only, nothing written to disk |

---

## Dependencies

All already installed:
- `playwright` 1.61.0 + chromium browser binaries (in `~/Library/Caches/ms-playwright`)
- `markdownify` 1.2.3
- `browser-use` 0.11.13 (only for the experimental script)

No new installs needed.

---

## Build Order

1. `tools/web_browser.py` — session manager (`_get_page()` singleton) + SSRF guard `_validate_url()` + enumeration JS
2. `tools/web_browser.py` — the eight `@tool` functions
3. `tools/tools.py` — register all `browser_*` tools
4. `config/settings.py` — enable `"web"`, add settings
5. `agent/system_prompt.py` — `TOOL_NOTES["web"]` + guidance (web_fetch for reads; browser tools for forms/logins; reference elements by number; confirm before submitting data/credentials)
6. Smoke-test the flow manually

## Smoke Test

1. `python -c "import tools.web_browser"` — imports clean
2. Drive `browser_open` → enumerate → `browser_fill` → `browser_submit` on a test form
3. Confirm SSRF guard rejects `http://localhost:1234`, `http://192.168.1.1`, etc.
