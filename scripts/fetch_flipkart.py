# Bootstrap HTML scraper. Replace with Flipkart Affiliate API after approval.
import requests
from bs4 import BeautifulSoup

def fetch_flipkart_keyword(keyword: str, max_items: int = 6):
  url = f"https://www.flipkart.com/search?q={requests.utils.quote(keyword)}"
  html = requests.get(url, headers={"User-Agent":"Mozilla/5.0"}).text
  soup = BeautifulSoup(html, "html.parser")
  out = []
  for a in soup.select("a")[:200]:
    title = a.get("title")
    href = a.get("href")
    if title and href and "/p/" in href:
      out.append({
        "title": title.strip(),
        "url": f"https://www.flipkart.com{href}",
        "price": "",
        "image": "",
        "source": "flipkart"
      })
      if len(out) >= max_items:
        break
  return out
