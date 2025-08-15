# Optional: post top deals to Pinterest
import json, httpx, asyncio
from .config import PINTEREST_ACCESS_TOKEN, PINTEREST_BOARD_ID

PIN_API = "https://api.pinterest.com/v5/pins"

async def post_pin(title, link, image_url, note):
  headers = {"Authorization": f"Bearer {PINTEREST_ACCESS_TOKEN}"}
  payload = {
    "board_id": PINTEREST_BOARD_ID,
    "title": title[:100],
    "description": note[:488],
    "link": link,
    "media_source": {"source_type": "image_url", "url": image_url}
  }
  async with httpx.AsyncClient(timeout=60) as client:
    r = await client.post(PIN_API, headers=headers, json=payload)
    r.raise_for_status()
    return r.json()

async def post_from_deals(path="deals.json", limit=3):
  with open(path, "r", encoding="utf-8") as f:
    deals = json.load(f)
  for d in deals[:limit]:
    try:
      print("Posting:", d["title"])
      await post_pin(d["title"], d["url"], d["image"], d.get("caption",""))
    except Exception as e:
      print("Pin failed:", e)

if __name__ == "__main__":
  asyncio.run(post_from_deals())
