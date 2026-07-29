from langchain_core.tools import tool
from markdownify import markdownify as md
import httpx
import asyncio

async def web_fetch():
    async with httpx.AsyncClient() as client:
        response = await client.get("https://books.toscrape.com")
        response = response.text
        print(md(response,strip=['script']))

asyncio.run(web_fetch())
