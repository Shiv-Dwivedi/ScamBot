from pyrogram import Client, filters
from services.virustotal import check_url
from services.gemini import analyze_text
import re

url_regex = r"(https?://[^\s]+)"

from pyrogram import Client, filters

def format_vt_stats(url, stats, malicious):
    return (
        f"{'⚠️ **Malicious Link Detected!**' if malicious else '✅ **Link Looks Safe!**'}\n\n"
        f"🔗 [{url}]({url})\n\n"
        f"📊 **VirusTotal Report:**\n"
        f"🛑 Malicious: {stats.get('malicious', 0)}\n"
        f"⚠️ Suspicious: {stats.get('suspicious', 0)}\n"
        f"✅ Harmless: {stats.get('harmless', 0)}\n"
        f"🕵️ Undetected: {stats.get('undetected', 0)}"
    )


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


@Client.on_message(filters.text)
async def auto_detect_handler(client, message):
    text = message.text
    urls = re.findall(url_regex, text)

    result_parts = []

    # Case 1: Only link
    if urls and text.strip() == urls[0]:
        url = urls[0]
        vt_result = await check_url(url)
        if vt_result["malicious"]:
           result_parts.append(format_vt_stats(url, vt_result["stats"], vt_result["malicious"]))
        else:
            result_parts.append(f"✅ URL looks safe:\n🔗 {url}")

    # Case 2: Text only (no link)
    elif not urls:
        scam_text, confidence = await analyze_text(text)
        result_parts.append(f"**🕵️ Scam Analysis:**\n{scam_text}\n\n**Confidence:**{confidence}%")

    # Case 3: Text + link(s)
    else:
        for url in urls:
            vt_result = await check_url(url)
            if vt_result["malicious"]:
                result_parts.append(format_vt_stats(url, vt_result["stats"], vt_result["malicious"]))
            else:
                result_parts.append(f"✅ URL looks safe:\n🔗 {url}")

        scam_text, confidence = await analyze_text(text)
        result_parts.append(f"**🕵️ Scam Analysis:**\n{scam_text}\n\n**Confidence: **{confidence}%")

    await message.reply(
        "\n\n".join(result_parts[:5]),
        disable_web_page_preview=True,
    )

