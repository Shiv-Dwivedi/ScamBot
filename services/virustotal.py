import aiohttp
import base64
from config import VT_API_KEY

async def check_url(url: str):
    try:
        # 1. Encode URL (URL-safe base64 without padding)
        encoded_url = base64.urlsafe_b64encode(url.encode()).decode().strip("=")
        print(f"[VT] Encoded URL: {encoded_url}")

        # 2. Set headers
        headers = {
            "x-apikey": VT_API_KEY
        }

        vt_url = f"https://www.virustotal.com/api/v3/urls/{encoded_url}"
        print(f"[VT] Requesting: {vt_url}")

        async with aiohttp.ClientSession() as session:
            async with session.get(vt_url, headers=headers) as resp:
                print(f"[VT] Status Code: {resp.status}")
                if resp.status != 200:
                    print("[VT] Error Response:", await resp.text())
                    return {"malicious": False, "error": "Failed VT API response"}
                
                data = await resp.json()
                print("[VT] Full Response JSON:", data)

        # 3. Parse result
        try:
            stats = data["data"]["attributes"]["last_analysis_stats"]
            print(f"[VT] Analysis Stats: {stats}")
            is_malicious = stats.get("malicious", 0) > 0
            return {"malicious": is_malicious, "stats": stats}
        except Exception as e:
            print("[VT] JSON parsing error:", str(e))
            return {"malicious": False, "error": "Failed to parse stats"}

    except Exception as e:
        print("❌ VirusTotal API Error:", str(e))
        return {"malicious": False, "error": "Exception raised"}