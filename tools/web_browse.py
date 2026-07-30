from langchain.chat_models import init_chat_model
from langchain_core.tools import tool
from langchain.agents import create_agent

from playwright.sync_api import sync_playwright
subagent_model = init_chat_model(
        model="",
        model_provider="openai",
        base_url="http://localhost:1234/v1",
        api_key="not-needed",
        temperature=0.3
)

subagent = create_agent(model=subagent_model)

def web_browse(search: str)->str:
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        page.goto("https://www.google.com")
        page.wait_for_load_state("domcontentloaded")
        search_box = page.locator("textarea[name='q']")
        search_box.fill(search)
        search_box.press("Enter")
        page.wait_for_load_state("domcontentloaded")
        page.wait_for_selector("h3")
        links = page.locator("h3").all()
        return(f"All links found related to search query : \n{links}")
        browser.close()

print(web_browse("Nanyang polytechnic"))
