from langchain_core.tools import tool
import httpx
import asyncio

async def web_fetch():
    async with httpx.AsyncClient() as client:
        response = await client.get("https://books.toscrape.com")
        response = response.text

asyncio.run(web_fetch())
