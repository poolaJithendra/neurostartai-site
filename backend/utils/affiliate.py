import os

BRAND = os.getenv("BRAND_NAME", "NeuroStart.ai")
AFFILIATE_TAG = os.getenv("AFFILIATE_TAG", "neurostart-21")

def with_affiliate_params(url: str) -> str:
    # For Amazon: ensure tag is appended
    if "amazon." in url and "tag=" not in url and AFFILIATE_TAG:
        sep = "&" if "?" in url else "?"
        return f"{url}{sep}tag={AFFILIATE_TAG}"
    return url

def append_disclosure(caption: str) -> str:
    note = "\n\nAffiliate note: We may earn a small commission at no extra cost to you."
    return caption.strip() + note
