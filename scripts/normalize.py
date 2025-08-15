def normalize(items):
  out, seen = [], set()
  for it in items:
    t = (it.get("title") or "").strip()
    u = (it.get("url") or "").strip()
    if not t or not u:
      continue
    key = (t.lower()[:80], u.split("?")[0])
    if key in seen:
      continue
    seen.add(key)
    out.append({
      "title": t[:140],
      "url": u,
      "price": it.get("price") or "",
      "image": it.get("image") or "",
      "source": it.get("source") or "",
    })
  return out
