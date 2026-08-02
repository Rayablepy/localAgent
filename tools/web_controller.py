import httpx
from tools.web_fetch import convert_to_md
from langchain_core.tools import tool
from pydantic import AnyHttpUrl
from bs4 import BeautifulSoup
import asyncio
async def browser_open(url: AnyHttpUrl, max_chars: int = 4000):
    url = str(url)
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        main_page = convert_to_md(response.text,str(url))
        soup = BeautifulSoup(response.text, "html.parser")
        interactives = [
            "a",
            "button",
            "details",
            "embed",
            "iframe",
            "input",
            "label",
            "select",
            "textarea",
            "audio",
            "video",
            "summary"
        ]
        interactives = soup.find_all(interactives)
        interactives_list= [f"{i}:{element}" for i, element in enumerate(interactives)]
        title = soup.title.string
        full_page=f"Page title:\n {title} \n Main page as markdown: \n {main_page} \n Interactive elements:\n {str(interactives_list)}"
        return full_page
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
