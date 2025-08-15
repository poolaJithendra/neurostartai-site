import httpx

from .config import HUGGINGFACE_API_TOKEN, HF_API_URL_TEXT

HEADERS = {"Authorization": f"Bearer {HUGGINGFACE_API_TOKEN}"} if HUGGINGFACE_API_TOKEN else {}

async def hf_text(prompt: str, max_new_tokens: int = 96) -> str:
    payload = {"inputs": prompt, "parameters": {"max_new_tokens": max_new_tokens}}
    async with httpx.AsyncClient(timeout=60) as client:
        r = await client.post(HF_API_URL_TEXT, headers=HEADERS, json=payload)
        r.raise_for_status()
        data = r.json()
    if isinstance(data, list) and data and "generated_text" in data[0]:
        return data[0]["generated_text"]
    if isinstance(data, dict) and "generated_text" in data:
        return data["generated_text"]
    if isinstance(data, list) and data and "summary_text" in data:
        return data["summary_text"]
    return str(data)
