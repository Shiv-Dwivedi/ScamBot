import google.generativeai as genai
from config import GEMINI_API_KEY

genai.configure(api_key=GEMINI_API_KEY)

model = genai.GenerativeModel("gemini-1.5-flash")  # or whatever latest model
generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 64,
    "max_output_tokens": 8192,
}
safety_settings = [
    {"category": "harmCategoryHarassment", "threshold": 3},
    {"category": "harmCategoryHateSpeech", "threshold": 3},
    {"category": "harmCategorySexuallyExplicit", "threshold": 3},
    {"category": "harmCategoryDangerousContent", "threshold": 3},
]

def sanitize_input(text: str) -> str:
    import re
    return re.sub(r"<[^>]*>", "", text)[:8192]

async def analyze_text(text: str):
    sanitized = sanitize_input(text)

    chat = model.start_chat(history=[
        {
            "role": "user",
            "parts": [{"text": "Analyze scam attempts. First explain your reasoning (under 5 points), then provide confidence percentage (0-100%) representing SCAM LIKELIHOOD in format 'Confidence: X%'"}],
        },
        {
            "role": "model",
            "parts": [{"text": "I will analyze messages for scam indicators..."}]
        },
    ])
    res = chat.send_message(sanitized)
    output = res.text.replace("*", "").replace("_", "")
    
    import re
    confidence = 0
    match = re.search(r"Confidence: (\d+)%", output)
    if match:
        confidence = int(match.group(1))
        output = output.replace(match.group(0), "").strip()

    return output, confidence
