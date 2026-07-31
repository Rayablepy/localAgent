
from browser_use import ChatOpenAI, Agent
from browser_use.agent.views import MessageCompactionSettings
from config.settings import SUBAGENT_MODEL_NAME, LOCAL_MODEL_API_KEY, LOCAL_MODEL_BASE_URL
import asyncio

subagent_model = ChatOpenAI(
    model=SUBAGENT_MODEL_NAME,
    base_url=LOCAL_MODEL_BASE_URL,
    api_key=LOCAL_MODEL_API_KEY,
    temperature=0.2,
    max_completion_tokens=1024,
    frequency_penalty=0.0,
)

async def browsing_subagent(task):
    agent = Agent(
        task=task,
        llm=subagent_model,
        use_vision=False,
        use_thinking=False,
        enable_planning=False,
        use_judge=False,
        max_clickable_elements_length=10000,
        message_compaction=MessageCompactionSettings(trigger_char_count=2000),
        llm_timeout=300,
    )
    await agent.run()

if __name__ == "__main__":
    user = input("Enter task: ")
    asyncio.run(browsing_subagent(task=user))
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
