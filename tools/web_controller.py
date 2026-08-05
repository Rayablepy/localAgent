from pydantic import AnyHttpUrl
from pathlib import Path
from playwright.sync_api import sync_playwright, Browser, Page, BrowserContext, Playwright
from playwright_stealth import Stealth
from langchain_core.tools import tool

INTERACTIVES_TABLE: str | None = None
playwright: Playwright | None = None
browser: Browser | None = None
context: BrowserContext | None = None
page: Page | None = None

def interactives_rendererjs() -> str:
    global INTERACTIVES_TABLE
    if INTERACTIVES_TABLE is None:
        INTERACTIVES_TABLE = (Path(__file__).parent / "js_middleware" / "interactives_table.js").read_text()
    return INTERACTIVES_TABLE

def get_page() -> Page:
    global playwright, browser, context, page
    if page is None:
        playwright = sync_playwright().start()
        browser = playwright.chromium.launch(
            headless=True,
            args=[
                "--disable-blink-features=AutomationControlled",
                "--no-sandbox",
                "--disable-infobars",
            ]
        )
        context = browser.new_context(
            viewport={"width": 1920, "height": 1080},
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        )
        page = context.new_page()
        Stealth().apply_stealth_sync(page)
    return page
@tool
def browser_open(url: str, max_chars: int = 4000) -> str:
    '''Opens a browser page to the specified URL and returns page title, body content and a numbered table of interactive elements.
    Args:
        url (str): The URL to open(MUST BE A VALID URL)
        max_chars (int, optional): The maximum number of characters to include in the body content. Defaults to 4000.
    Returns:
        str: A formatted string containing the page title, body content and a numbered table of interactive elements.
    '''
    page = get_page()
    page.goto(url, timeout=30_000)
    page.wait_for_load_state("domcontentloaded")
    title = page.title()
    body = page.locator("body").inner_text()[:max_chars].rsplit('\n', 1)[0]
    interactives: list[dict[str, str | int | bool]] = page.evaluate(interactives_rendererjs())
    rows = [f"{r['index']:>3} {r['tag']:<14} {r['label']}" + (f" = {r['value']}" if r['value'] else "") for r in interactives]
    return f"Title: {title}\nBody: {body}\n\nInteractive elements:\n" + "\n".join(rows)

#@tool
async def browser_click(index: int) -> str:
    ...
    #TODO Click element by its number from the last enumeration; returns fresh page summary + elements

#@tool
async def browser_click_text(text: str) -> str:
    ...
    #TODO Click the element whose visible text matches ("Sign in"); robust for buttons/links

#@tool
async def browser_fill(index: int, value: str) -> str:
    ...
    #TODO Fill an input by its number; returns fresh page summary + elements

#@tool
async def browser_select(index: int, option: str) -> str:
    ...
    #TODO Pick an option in a dropdown; returns fresh page summary + elements

#@tool
async def browser_submit() -> str:
    ...
    #TODO Submit the active form; returns fresh page summary + elements

#@tool
async def browser_read(max_chars: int = 5000) -> str:
    ...
    #TODO Extract current page as markdown (SPA content web_fetch can't reach)

#@tool
async def browser_wait(ms: int = 2000) -> str:
    ...
    #TODO Wait for page load / settle; returns current page summary

browser_tools=[browser_open]
