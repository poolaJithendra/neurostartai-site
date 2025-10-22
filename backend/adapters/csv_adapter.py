import csv, pathlib
from typing import List, Dict

def fetch(path: str = "data/sample_deals.csv") -> List[Dict]:
    p = pathlib.Path(path)
    if not p.exists():
        return []
    rows = []
    with p.open(newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for r in reader:
            r["original_price"] = float(r.get("original_price") or 0)
            r["deal_price"] = float(r.get("deal_price") or 0)
            r["discount_percent"] = round(100 * (1 - (r["deal_price"]/r["original_price"])) , 1) if r["original_price"] else 0
            rows.append(r)
    return rows
