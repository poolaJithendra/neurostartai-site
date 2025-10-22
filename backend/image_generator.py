import io, os, textwrap, requests
from PIL import Image, ImageDraw, ImageFont

FONT_PATH = None
W, H = 1080, 1350

def _load_image(url: str) -> Image.Image:
    try:
        r = requests.get(url, timeout=20)
        r.raise_for_status()
        im = Image.open(io.BytesIO(r.content)).convert("RGB")
        return im
    except Exception:
        return Image.new("RGB", (W, H), (245,245,245))

def _fit_image(im: Image.Image) -> Image.Image:
    im = im.copy()
    im.thumbnail((W, int(H*0.62)))
    bg = Image.new("RGB", (W, int(H*0.62)), (255,255,255))
    x = (W - im.width)//2
    y = (bg.height - im.height)//2
    bg.paste(im, (x,y))
    return bg

def generate_card(deal: dict, save_path: str):
    title = deal.get("title","")
    dp = int(float(deal.get("deal_price") or 0))
    op = int(float(deal.get("original_price") or 0))
    off = int(float(deal.get("discount_percent") or 0))
    image_url = deal.get("image_url")

    canvas = Image.new("RGB", (W, H), (250, 250, 255))
    draw = ImageDraw.Draw(canvas)
    font_big = ImageFont.load_default()
    font_med = ImageFont.load_default()

    prod = _load_image(image_url)
    prod = _fit_image(prod)
    canvas.paste(prod, (0, 0))

    y0 = int(H*0.64)
    draw.rectangle([(40, y0), (W-40, y0+260)], fill=(255,255,255))
    title_wrapped = textwrap.fill(title, width=28)
    draw.text((60, y0+20), title_wrapped, font=font_big, fill=(20,20,20))

    price_line = f"₹{dp}  (₹{op})  •  {off}% OFF"
    draw.text((60, y0+150), price_line, font=font_med, fill=(30,30,30))

    badge_w, badge_h = 220, 90
    draw.rounded_rectangle([(W-badge_w-60, y0+20), (W-60, y0+20+badge_h)], radius=20, fill=(240, 240, 255), outline=(40,40,200))
    draw.text((W-badge_w-40, y0+50-12), f"{off}% OFF", font=font_big, fill=(40,40,200))

    draw.rectangle([(0,H-110),(W,H)], fill=(35,35,45))
    draw.text((40, H-80), "NeuroStart.ai • Best Deals Daily", font=font_med, fill=(255,255,255))
    draw.text((40, H-50), "Link in bio • Tap to buy", font=font_med, fill=(220,220,220))

    os.makedirs(os.path.dirname(save_path), exist_ok=True)
    canvas.save(save_path, "JPEG", quality=92)
    return save_path
