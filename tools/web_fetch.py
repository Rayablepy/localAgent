from langchain_core.tools import tool
from bs4 import BeautifulSoup
from markdownify import markdownify as md
import httpx
from pydantic import  AnyHttpUrl
from urllib.parse import urljoin
SELECTION = ["main","article",'[role="main"]',"#content",".content","body"]
TOREMOVE = ["script", "style","nav","aside","form","iframe","svg","noscript"]

def clean_page(soup: BeautifulSoup,url:str):
    for tag in TOREMOVE:
        for element in soup.find_all(tag):
            element.decompose()
    main=None
    for selector in SELECTION:
        main=soup.select_one(selector)
        if main:
            break
    if not main:
        main=soup.body or soup
    if url:
        for tag,attr in [('a', 'href'),("img", 'src')]:
            for element in main.find_all(tag):
                if attr in element.attrs:
                    element[attr] = urljoin(url, element[attr])
    return main

def convert_to_md(page:str,url:str,max_chars:int=5000) -> str:
    soup=BeautifulSoup(page,"html.parser")
    main = clean_page(soup,url)
    md_txt=md(
        str(main),
        heading_style="ATX",
        strip=TOREMOVE
    )
    if len(md_txt) > max_chars:
        md_txt = md_txt[:max_chars].rsplit('\n', 1)[0]
    return md_txt

@tool
async def web_fetch(url:AnyHttpUrl,max_chars:int=5000) -> str:
    """Performs an asynchronous HTTP GET request to the specified URL and returns the response as a markdown string.
    ONLY USE WHEN A SIMPLE READ IS NEEDED AND IF USER HAS EXPLICITLY PROVIDED A URL.

    Args:
        url (AnyHttpUrl): The URL to fetch.
        max_chars (int, optional): The maximum number of characters to return. Defaults to 5000.
    Returns:
        str: The response as a markdown string.
    """
    url = str(url)
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        return convert_to_md(response.text,url,max_chars)
