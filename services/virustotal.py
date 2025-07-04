import aiohttp
from config import VT_API_KEY

async def check_url(url: str):
    headers = {"x-apikey": VT_API_KEY}
    async with aiohttp.ClientSession() as session:
        async with session.get(f"https://www.virustotal.com/api/v3/urls", params={"url": url}, headers=headers) as resp:
            if resp.status != 200:
                return {"malicious": False}
            data = await resp.json()
            try:
                stats = data["data"]["attributes"]["last_analysis_stats"]
                is_malicious = stats.get("malicious", 0) > 0
                return {"malicious": is_malicious, "stats": stats}
            except Exception:
                return {"malicious": False}
