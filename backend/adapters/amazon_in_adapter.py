"""Amazon India Product Advertising API v5 adapter (stub + fallback).

Notes:
- Requires AWS Access Key, Secret Key, and Associate Tag (AFFILIATE_TAG).
- Proper PA-API v5 requests need signed headers (AWS4-HMAC-SHA256). This file
  provides a placeholder function `signed_request` with TODOs. Until keys are set,
  `fetch` falls back to CSV.

Replace TODOs with a real signer (or use any approved SDK). Always follow Amazon policy.
"""

import os, time, json, hashlib, hmac, datetime, requests
from typing import List, Dict
from .csv_adapter import fetch as fetch_csv
from backend.utils.affiliate import with_affiliate_params

ACCESS_KEY = os.getenv("AMAZON_ACCESS_KEY")
SECRET_KEY = os.getenv("AMAZON_SECRET_KEY")
PARTNER_TAG = os.getenv("AFFILIATE_TAG", "neurostart-21")
PARTNER_TYPE = "Associates"
REGION = "eu-west-1"  # PA-API recommends based on marketplace; adjust as needed
HOST = "webservices.amazon.in"
ENDPOINT = f"https://{HOST}/paapi5/searchitems"

def signed_request(payload: dict) -> dict:
    """TODO: Implement AWS V4 signing for PA-API.
    For now, return {} so we can fallback.
    """
    return {}

def fetch(keywords: List[str] = None, limit: int = 10) -> List[Dict]:
    keywords = keywords or ["deals", "gadgets", "discount"]
    if not (ACCESS_KEY and SECRET_KEY and PARTNER_TAG):
        # No keys -> fallback to CSV sample
        return fetch_csv()

    # Prepare payload (per PA-API v5 spec)
    payload = {
        "PartnerTag": PARTNER_TAG,
        "PartnerType": PARTNER_TYPE,
        "Keywords": " ".join(keywords),
        "SearchIndex": "All",
        "ItemCount": min(limit, 10),
        "Resources": [
            "Images.Primary.Large",
            "ItemInfo.Title",
            "Offers.Listings.Price",
        ]
    }

    try:
        resp = signed_request(payload)
        if not resp:
            # if signer not implemented, fallback
            return fetch_csv()
        # Parse items
        items = []
        for it in resp.get("SearchResult", {}).get("Items", []):
            title = (((it.get("ItemInfo") or {}).get("Title") or {}).get("DisplayValue")) or "Amazon Item"
            image_url = (((it.get("Images") or {}).get("Primary") or {}).get("Large") or {}).get("URL")
            offer = ((it.get("Offers") or {}).get("Listings") or [{}])[0]
            price = ((((offer.get("Price") or {}).get("Amount")) or 0.0))
            orig = price  # Without full price history we use list price if available
            url = (it.get("DetailPageURL") or "")
            url = with_affiliate_params(url)

            if not (title and image_url and price):
                continue
            items.append({
                "id": it.get("ASIN"),
                "title": title,
                "description": "",
                "category": "Digital & Gadgets",
                "image_url": image_url,
                "original_price": float(orig) or 0.0,
                "deal_price": float(price) or 0.0,
                "discount_percent": 0.0,  # compute if list price available
                "affiliate_link": url,
                "source": "amazon_in"
            })
        if items:
            # compute discount if possible
            for d in items:
                op, dp = d.get("original_price") or 0, d.get("deal_price") or 0
                d["discount_percent"] = round(100*(1 - (dp/op)),1) if op else 0
            return items
        return fetch_csv()
    except Exception:
        return fetch_csv()
