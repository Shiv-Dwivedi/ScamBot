from pyrogram import Client, filters
from services.virustotal import check_url
from services.gemini import analyze_text
import re

url_regex = r"(https?://[^\s]+)"

from pyrogram import Client, filters

@Client.on_message(filters.command("start"))
async def start_handler(client, message):
    await message.reply(
        f"👋 Hello {message.from_user.first_name}!\n\n"
        "I'm a smart scam detection bot.\n\n"
        "🔍 If you send me any message, I will:\n"
        "1. Analyze it for **scam attempts** using Gemini\n"
        "2. Scan any **links** in the message for threat\n\n"
        "No commands needed — just send a message or URL.\n\n"
        "🔗 By: [Shiv Dwivedi](https://github.com/your-username/your-repo)",
        disable_web_page_preview=True
    )


@Client.on_message(filters.text )
async def auto_detect_handler(client, message):
    text = message.text
    found_urls = re.findall(url_regex, text)

    results = []

    # If there's a URL, check with VirusTotal
    if found_urls:
        for url in found_urls:
            vt_result = await check_url(url)
            if vt_result["malicious"]:
                results.append(f"⚠️ URL flagged as malicious:\n🔗 {url}\nStats: {vt_result['stats']}")
            else:
                results.append(f"✅ URL looks safe:\n🔗 {url}")

    # Scam analysis regardless of links
    scam_analysis, confidence = await analyze_text(text)
    results.append(f"🕵️ Scam Analysis:\n{scam_analysis}\n\nConfidence: {confidence}%")

    await message.reply("\n\n".join(results[:5]))  # Avoid too much output
