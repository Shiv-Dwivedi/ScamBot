import re

def sanitize_input(text: str) -> str:
    # Remove any HTML/Telegram-style tags
    cleaned = re.sub(r"<[^>]*>", "", text)
    # Remove excessive whitespace
    cleaned = re.sub(r"\s+", " ", cleaned).strip()
    # Limit to first 8192 characters (Gemini max token length limit)
    return cleaned[:8192]
