from langchain.chat_models import init_chat_model
from langchain_core.tools import tool
from langchain.agents import create_agent
from playwright_stealth import Stealth
from playwright.sync_api import sync_playwright
subagent_model = init_chat_model(
        model="",
        model_provider="openai",
        base_url="http://localhost:1234/v1",
        api_key="not-needed",
        temperature=0.3
)

subagent = create_agent(model=subagent_model)
#deprecated function
'''
def web_browse(search: str)->str:
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
        page.goto("https://duckduckgo.com/")

        page.wait_for_selector("input[name='q'], [role='combobox'], form", timeout=5000)
        page.wait_for_load_state("domcontentloaded")

        search_box = page.locator("input[name='q']")
        search_box.fill(search)
        search_box.press("Enter")
        page.wait_for_load_state("domcontentloaded")

        page.wait_for_selector("article[data-testid='result']")
        results = page.locator("article[data-testid='result']").all()
        links = []
        for r in results:
            link = r.locator("a[href]").first
            href = link.get_attribute("href")
            title = r.locator("h2").inner_text()
            links.append({"title": title, "url": href})

        return(f"All links found related to search query : \n{links}")
        browser.close()
'''

print(web_browse("Nanyang polytechnic"))
