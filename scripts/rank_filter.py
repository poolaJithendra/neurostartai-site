# scripts/rank_filter.py
import re
from .llm import hf_text

SCORING = (
    "Rate the following product title for mainstream shopping appeal on a 0-10 scale. "
    "Return only a number.\nTitle: {t}"
)

CAPTION = (
    "Write a concise, benefit-focused, single-sentence caption (<80 chars) for this product. "
    "Return only the caption.\nTitle: {t}"
)

def _safe_number(txt: str, default: float = 5.0) -> float:
    if not txt:
        return default
    m = re.search(r"(\d+(?:\.\d+)?)", txt)
    try:
        return float(m.group(1)) if m else default
    except Exception:
        return default

async def score(title: str) -> float:
    txt = await hf_text(SCORING.format(t=title))
    return _safe_number(txt, 5.0)

async def caption(title: str) -> str:
    txt = await hf_text(CAPTION.format(t=title))
    if not txt:
        return (title or "").strip()[:80]
    # Single line, trimmed
    return txt.replace("\n", " ").strip()[:80]

async def enrich(items):
    """
    Adds 'score' and 'caption' to each item with robust fallbacks.
    Always returns at most 24 items sorted by score desc.
    """
    enriched = []
    for it in items:
        title = it.get("title") or ""
        s = await score(title)
        c = await caption(title)
        it["score"] = s
        it["caption"] = c
        enriched.append(it)
    return sorted(enriched, key=lambda x: x.get("score", 0), reverse=True)[:24]
