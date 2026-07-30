from langchain_core.tools import tool
from bs4 import BeautifulSoup
from markdownify import markdownify as md
import re
import httpx
import asyncio
from urllib.parse import urljoin
SELECTION = ["main","article",'[role="main"]',"#content",".content","body"]
TOREMOVE = ["script", "style","nav","aside","form","iframe","svg","noscript"]

def clean_page(soup: BeautifulSoup,url:str) -> str:
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

def convert_to_md(page:str,url:str) -> str:
    soup=BeautifulSoup(page,"html.parser")
    main = clean_page(soup,url)
    md_txt=md(
        str(main),
        strip=TOREMOVE
    )
    

async def web_fetch():
    async with httpx.AsyncClient() as client:
        response = await client.get("https://books.toscrape.com")
        soup = BeautifulSoup(response.text, 'html.parser')
        print(soup)

asyncio.run(web_fetch())
