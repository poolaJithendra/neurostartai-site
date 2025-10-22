import os, json, argparse, pathlib, datetime
from slugify import slugify
from backend.adapters.amazon_in_adapter import fetch as fetch_amazon
from backend.adapters.csv_adapter import fetch as fetch_csv
from backend.llm_filter import score_deal
from backend.caption_generator import caption_for
from backend.image_generator import generate_card
from backend.utils.shortlinks import shorten
from backend.utils.affiliate import with_affiliate_params

SITE_BASE_URL = os.getenv("SITE_BASE_URL", "")
PUBLIC_DIR = "public"
POSTS_DIR = f"{PUBLIC_DIR}/posts"

def ensure_public():
    os.makedirs(PUBLIC_DIR, exist_ok=True)
    os.makedirs(POSTS_DIR, exist_ok=True)
    index_path = pathlib.Path(f"{PUBLIC_DIR}/index.html")
    if not index_path.exists():
        index_path.write_text("<!doctype html><title>NeuroStart.ai</title><div id='grid'></div><script src='deals.js'></script>", encoding="utf-8")
    css_path = pathlib.Path(f"{PUBLIC_DIR}/style.css")
    if not css_path.exists():
        css_path.write_text("body{font-family:system-ui;margin:24px}", encoding="utf-8")

def write_deals_js(deals):
    p = pathlib.Path(f"{PUBLIC_DIR}/deals.js")
    items = []
    for d in deals:
        items.append({
            "title": d.get("title"),
            "category": d.get("category"),
            "image_url": d.get("image_url"),
            "deal_price": d.get("deal_price"),
            "original_price": d.get("original_price"),
            "discount_percent": d.get("discount_percent"),
            "url": with_affiliate_params(d.get("affiliate_link","")),
            "score": d.get("score"),
            "ts": int(datetime.datetime.now().timestamp())
        })
    js = "const DEALS=" + json.dumps(items, ensure_ascii=False) + ";"
    p.write_text(js, encoding="utf-8")

def main(date: str, limit: int, post_instagram: bool, post_pinterest: bool):
    ensure_public()

    # 1) Fetch: Amazon if possible, else CSV
    deals = fetch_amazon()
    if not deals:
        deals = fetch_csv()

    # 2) score & pick
    enriched = []
    for d in deals:
        s = score_deal(d)
        d["score"] = s["score"]
        d["score_reason"] = s["reason"]
        enriched.append(d)
    enriched.sort(key=lambda x: x["score"], reverse=True)
    top = enriched[:limit]

    # 3) render assets
    day_dir = f"{POSTS_DIR}/{date}"
    os.makedirs(day_dir, exist_ok=True)
    manifest = []

    for d in top:
        slug = slugify(d.get("title",""))[:60]
        img_rel = f"{day_dir}/{slug}.jpg"
        generate_card(d, img_rel)

        link = with_affiliate_params(d.get("affiliate_link",""))
        short = shorten(link)
        caption = caption_for(d)

        post = {
            "title": d.get("title"),
            "image_path": img_rel,
            "image_url": f"{SITE_BASE_URL}posts/{date}/{slug}.jpg" if SITE_BASE_URL else img_rel,
            "caption": caption,
            "affiliate_link": short,
            "deal_price": d.get("deal_price"),
            "original_price": d.get("original_price"),
            "discount_percent": d.get("discount_percent"),
            "score": d.get("score"),
            "score_reason": d.get("score_reason"),
            "created_at": date
        }
        manifest.append(post)

    with open(f"{day_dir}/posts.json", "w", encoding="utf-8") as f:
        json.dump(manifest, f, ensure_ascii=False, indent=2)

    write_deals_js(top)

    # 4) Social posting (if configured)
    if SITE_BASE_URL and (post_instagram or post_pinterest):
        if post_instagram:
            try:
                from backend.instagram_poster import post_image
                for p in manifest:
                    post_image(p["image_url"], p["caption"])
            except Exception as e:
                print("Instagram error:", e)
        if post_pinterest:
            try:
                from backend.pinterest_poster import post_pin
                for p in manifest:
                    post_pin(p["title"], p["caption"], p["affiliate_link"], p["image_url"])
            except Exception as e:
                print("Pinterest error:", e)

    print(f"Generated {len(manifest)} posts in {day_dir}")

if __name__ == "__main__":
    import argparse, datetime
    ap = argparse.ArgumentParser()
    ap.add_argument("--date", default=datetime.date.today().isoformat())
    ap.add_argument("--limit", type=int, default=5)
    ap.add_argument("--post-instagram", dest="post_instagram", default="false")
    ap.add_argument("--post-pinterest", dest="post_pinterest", default="false")
    args = ap.parse_args()
    post_instagram = str(args.post_instagram).lower() in ("1","true","yes","y")
    post_pinterest = str(args.post_pinterest).lower() in ("1","true","yes","y")
    main(args.date, args.limit, post_instagram, post_pinterest)
