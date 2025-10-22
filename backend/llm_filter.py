import os

def score_deal(deal: dict) -> dict:
    api_key = os.getenv("OPENAI_API_KEY")
    # Heuristic scoring: discount + category + price sweet spot
    discount = float(deal.get("discount_percent") or 0)
    category = (deal.get("category") or "").lower()
    base = min(max(discount, 0), 90)
    if any(k in category for k in ["gadget","phone","earbud","smart","digital"]):
        base += 8
    if any(k in category for k in ["beauty","home","fitness","pets"]):
        base += 4
    try:
        dp = float(deal.get("deal_price") or 0)
        if 0 < dp < 1500: base += 5
    except: pass
    score = max(0, min(100, int(base)))
    reason = f"Heuristic score (discount={discount}%, category='{category}', price={deal.get('deal_price')})"
    return {"score": score, "reason": reason}
