import asyncio
import aiohttp
import os
from datetime import datetime

async def fetch_pixiv_image(session, keyword=None, r18=0):
    api_url = "https://api.lolicon.app/setu/v1"
    params = {
        "num": 1,
        "r18": r18
    }
    if keyword:
        params["tag"] = keyword
    async with session.get(api_url, params=params, timeout=10) as resp:
        resp.raise_for_status()
        data = await resp.json()
        return data['data'][0]['url']

async def download_image(session, url, folder, idx):
    async with session.get(url) as resp:
        resp.raise_for_status()
        ext = url.split('.')[-1]
        filename = f"{datetime.now().strftime('%Y%m%d_%H%M%S')}_{idx}.{ext}"
        path = os.path.join(folder, filename)
        content = await resp.read()
        with open(path, 'wb') as f:
            f.write(content)
        print(f"Downloaded: {path}")

async def main():
    os.makedirs('img', exist_ok=True)
    total_time = 60        # seconds
    interval = 2           # seconds
    download_count = total_time // interval

    async with aiohttp.ClientSession() as session:
        for i in range(download_count):
            try:
                img_url = await fetch_pixiv_image(session, r18=1)
                await download_image(session, img_url, 'img', i)
            except Exception as e:
                print(f"Error: {e}")
            if i < download_count - 1:
                await asyncio.sleep(interval)

if __name__ == "__main__":
    asyncio.run(main())