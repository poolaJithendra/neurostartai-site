# scripts/llm.py
import os
import json
import httpx

# Modes:
#   LLM_MODE=off  -> no network calls; local, deterministic fallbacks
#   LLM_MODE=hf   -> use Hugging Face endpoint defined by HF_API_URL_TEXT
LLM_MODE = os.getenv("LLM_MODE", "off").strip().lower()

def _local_text(prompt: str) -> str:
    """
    Deterministic local fallback for captions/scoring text.
    Keeps pipeline green if LLM is disabled or unavailable.
    """
    p = (prompt or "").strip()
    return p[:160].replace("\n", " ")

async def hf_text(prompt: str) -> str:
    """
    Unified text function used by the pipeline.
    Falls back locally if LLM_MODE != 'hf' or on any HTTP/parse error.
    """
    if LLM_MODE != "hf":
        return _local_text(prompt)

    url = os.getenv("HF_API_URL_TEXT", "").strip()
    token = os.getenv("HUGGINGFACE_API_TOKEN", "").strip()
    if not url or not token:
        return _local_text(prompt)

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    }
    payload = {"inputs": prompt}

    timeout = httpx.Timeout(30.0, connect=10.0)
    try:
        async with httpx.AsyncClient(timeout=timeout) as client:
            r = await client.post(url, headers=headers, content=json.dumps(payload))
            if r.status_code != 200:
                return _local_text(prompt)
            data = r.json()
            # Normalize common HF formats
            if isinstance(data, list) and data and isinstance(data[0], dict):
                # T5/BART style responses
                gen = data.get("generated_text")
                if isinstance(gen, str) and gen.strip():
                    return gen.strip()
                gen = data.get("summary_text")
                if isinstance(gen, str) and gen.strip():
                    return gen.strip()
            # Fallback: stringify safely
            return _local_text(str(data))
    except Exception:
        return _local_text(prompt)
