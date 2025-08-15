# Bootstrap HTML scraper. Replace with Amazon PA-API after approval.
import requests
from bs4 import BeautifulSoup
from .config import AFFILIATE_TAG

def fetch_amazon_keyword(keyword: str, max_items: int = 8):
  url = f"https://www.amazon.in/s?k={requests.utils.quote(keyword)}"
  html = requests.get(url, headers={"User-Agent":"Mozilla/5.0"}).text
  soup = BeautifulSoup(html, "html.parser")
  out = []
  for card in soup.select("[data-component-type='s-search-result']")[:max_items]:
    a = card.select_one("h2 a")
    title = a.select_one("span").get_text(strip=True) if a else None
    href = a["href"] if a else None
    price = (card.select_one(".a-price .a-offscreen") or {}).get_text(strip=True) if card.select_one(".a-price .a-offscreen") else None
    img = card.select_one("img")["src"] if card.select_one("img") else None
    if not title or not href:
      continue
    link = f"https://www.amazon.in{href}"
    joiner = "&" if "?" in link else "?"
    if AFFILIATE_TAG:
      link = f"{link}{joiner}tag={AFFILIATE_TAG}"
    out.append({"title": title, "url": link, "price": price or "", "image": img or "", "source": "amazon"})
  return out
