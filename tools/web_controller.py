import httpx
from langchain_core.tools import tool


@tool
async def browser_open(url: str, max_chars: int = 4000) -> str:
    ...
    #TODO Navigate; returns title + page markdown + numbered table of interactive elements

@tool
async def browser_click(index: int) -> str:
    ...
    #TODO Click element by its number from the last enumeration; returns fresh page summary + elements

@tool
async def browser_click_text(text: str) -> str:
    ...
    #TODO Click the element whose visible text matches ("Sign in"); robust for buttons/links

@tool
async def browser_fill(index: int, value: str) -> str:
    ...
    #TODO Fill an input by its number; returns fresh page summary + elements

@tool
async def browser_select(index: int, option: str) -> str:
    ...
    #TODO Pick an option in a dropdown; returns fresh page summary + elements

@tool
async def browser_submit() -> str:
    ...
    #TODO Submit the active form; returns fresh page summary + elements

@tool
async def browser_read(max_chars: int = 5000) -> str:
    ...
    #TODO Extract current page as markdown (SPA content web_fetch can't reach)

@tool
async def browser_wait(ms: int = 2000) -> str:
    ...
    #TODO Wait for page load / settle; returns current page summary
