
import asyncio
from playwright.sync_api import sync_playwright
from playwright_stealth import Stealth

browser = None
page = None

def get_page():
    global browser, page
    if page is None:
        with Stealth().use_sync(sync_playwright()) as p:
            browser = p.chromium.launch(
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

async def browser_open(url: AnyHttpUrl, max_chars: int = 4000) -> str:
    page = get_page()
    page.goto(url)
    page.wait_for_load_state("domcontentloaded")
    title = page.title()
    body = page.locator("body").inner_text()

    ...
    #TODO Navigate; returns title + page markdown + numbered table of interactive elements

if '__main__' == __name__:
    print(asyncio.run(browser_open('https://www.nyp.edu.sg/main')))
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
