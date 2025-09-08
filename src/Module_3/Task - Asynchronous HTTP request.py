import asyncio
import aiohttp
import json

urls = [
    "https://example.com",
    "https://httpbin.org/status/404",
    "https://nonexistent.url"
]


async def fetch_urls(urls: list[str], file_path: str):
    results = {}

    async with aiohttp.ClientSession() as session:
        async def fetch(url: str):
            try:
                async with session.get(url, timeout=10) as response:
                    status = response.status
            except Exception:
                status = 0
            results[url] = status
            return {'url': url, 'status_code': status}

        tasks = [fetch(url) for url in urls]
        done = await asyncio.gather(*tasks)

    with open(file_path, 'w', encoding='utf-8') as f:
        for item in done:
            f.write(json.dumps(item, ensure_ascii=False) + "\n")

    return results



if __name__ == '__main__':
    asyncio.run(fetch_urls(urls, './results.jsonl'))