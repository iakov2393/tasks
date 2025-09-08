import asyncio
import aiohttp
import json
from aiohttp import ClientError, ClientTimeout, TCPConnector

async def fetch_urls(input_file: str, output_file: str):
    connector = TCPConnector(limit=5)

    async def fetch(session: aiohttp.ClientSession, url: str):
        try:
            async with session.get(url, timeout=ClientTimeout(total=600)) as response:
                if response.status == 200:
                    try:
                        data = await response.json()
                    except Exception:
                        data = None
                    return {"url": url, "content": data}
                else:
                    return {"url": url, "content": None}
        except (asyncio.TimeoutError, ClientError, Exception):
            return {"url": url, "content": None}


    with open(input_file, "r", encoding="utf-8") as f:
        urls = [line.strip() for line in f if line.strip()]

    async with aiohttp.ClientSession(connector=connector) as session:
        tasks = [fetch(session, url) for url in urls]

        with open(output_file, "w", encoding="utf-8") as f_out:
            for coro in asyncio.as_completed(tasks):
                result = await coro
                f_out.write(json.dumps(result, ensure_ascii=False) + "\n")



if __name__ == "__main__":
    input_file = "urls.txt"
    output_file = "results.jsonl"
    asyncio.run(fetch_urls(input_file, output_file))
