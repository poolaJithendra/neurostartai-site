import os
from backend.utils.affiliate import append_disclosure

DEFAULT_HASHTAGS = os.getenv("DEFAULT_HASHTAGS", "#DealsIndia #OfferAlert #SaveMore #BudgetBuys")

def caption_for(deal: dict) -> str:
    title = deal.get("title","").strip()
    dp = deal.get("deal_price")
    op = deal.get("original_price")
    off = deal.get("discount_percent")
    cat = deal.get("category","")
    base = f"🔥 Deal Alert: {title}\n₹{int(float(dp or 0))} (was ₹{int(float(op or 0))}) — {int(float(off or 0))}% OFF\nCategory: {cat}\nLink in bio or on site!\n{DEFAULT_HASHTAGS}"
    return append_disclosure(base)
