import re
from .llm import hf_text

SCORING = """Score 0-10 for Indian shoppers. Consider discount potential, popularity, clarity, broad appeal.
Return ONLY a number.

Title: {t}"""

CAPTION = """Short Pinterest caption for Indian audience, ≤14 words, 1 emoji, no hashtags.
Title: {t}"""

async def score(t: str) -> float:
  txt = await hf_text(SCORING.format(t=t))
  m = re.search(r"(\d+(?:\.\d+)?)", txt or "")
  return float(m.group(1)) if m else 5.0

async def caption(t: str) -> str:
  txt = await hf_text(CAPTION.format(t=t))
  return (txt or "").strip().split("\n")[0][:120]

async def enrich(items):
  enriched = []
  for it in items:
    s = await score(it["title"])
    c = await caption(it["title"])
    it["score"] = s
    it["caption"] = c
    enriched.append(it)
  return sorted(enriched, key=lambda x: x.get("score",0), reverse=True)[:24]
