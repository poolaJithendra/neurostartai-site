import json

def write_deals(items, path="deals.json"):
  with open(path, "w", encoding="utf-8") as f:
    json.dump(items, f, ensure_ascii=False, indent=2)
  print(f"Wrote {len(items)} deals to {path}")
