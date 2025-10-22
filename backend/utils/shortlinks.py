import os, requests

BITLY = os.getenv("BITLY_TOKEN")

def shorten(url: str) -> str:
    if not BITLY:
        return url
    try:
        r = requests.post(
            "https://api-ssl.bitly.com/v4/shorten",
            headers={"Authorization": f"Bearer {BITLY}", "Content-Type":"application/json"},
            json={"long_url": url}
        )
        if r.ok:
            return r.json().get("link", url)
    except Exception:
        pass
    return url
