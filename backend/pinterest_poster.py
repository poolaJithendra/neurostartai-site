import os, requests

ACCESS_TOKEN = os.getenv("PINTEREST_ACCESS_TOKEN")
BOARD_ID = os.getenv("PINTEREST_BOARD_ID")

def post_pin(title: str, description: str, link: str, image_url: str) -> bool:
    if not (ACCESS_TOKEN and BOARD_ID):
        print("[pinterest] Missing PINTEREST_ACCESS_TOKEN or BOARD_ID; skipping.")
        return False
    try:
        url = "https://api.pinterest.com/v5/pins"
        headers = {"Authorization": f"Bearer {ACCESS_TOKEN}", "Content-Type":"application/json"}
        data = {
            "board_id": BOARD_ID,
            "title": title[:100],
            "description": description[:500],
            "link": link,
            "media_source": {"source_type":"image_url", "url": image_url}
        }
        r = requests.post(url, headers=headers, json=data, timeout=30)
        if not r.ok:
            print("Pinterest failed:", r.text); return False
        print("[pinterest] Pin created:", r.json()); return True
    except Exception as e:
        print("Pinterest error:", e); return False
