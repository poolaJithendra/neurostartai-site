import asyncio

from .fetch_amazon import fetch_amazon_keyword
from .fetch_flipkart import fetch_flipkart_keyword
from .fetch_generic import fetch_generic
from .normalize import normalize
from .rank_filter import enrich

KEYWORDS = [
    "wireless earbuds under 2000",
    "vitamin c serum",
    "smartwatch deals",
    "gaming mouse",
    "protein powder",
    "dog treats",
]

async def gather_raw():
    items = []
    for kw in KEYWORDS:
        try:
            items += fetch_amazon_keyword(kw, 6)
        except Exception as e:
            print("amazon", kw, e)
        try:
            items += fetch_flipkart_keyword(kw, 4)
        except Exception as e:
            print("flipkart", kw, e)
    items += fetch_generic()
    return items

async def agent_run():
    raw = await gather_raw()
    norm = normalize(raw)
    ranked = await enrich(norm)
    return ranked
