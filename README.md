# NeuroStart.ai — Unified GitHub Pack (India-first, LLM-ready)

This repository is a **single, production-ready pack** to launch an **AI-curated affiliate deals** product on **GitHub Pages**, with **daily automation**, **Amazon India adapter**, and **Instagram + Pinterest posting**.

## Highlights
- **Zero servers**: GitHub Actions cron generates your site & posts daily
- **Adapters**: Amazon India (PA-API v5, stubbed) + CSV fallback
- **Creative assets**: Pillow-generated **Instagram/Pinterest** images
- **Social**: Instagram Graph API + Pinterest API poster (token-based)
- **LLM-optional**: If `OPENAI_API_KEY` absent → smart heuristic ranking
- **Best UI**: Modern GH Pages site (search/filter/sort, SEO JSON-LD, RSS, sitemap)

---

## Quick Start

1) **Create a new GitHub repo** and upload this pack.
2) Enable **GitHub Pages** → serve from the `/public` folder.
3) In **Settings → Secrets and variables → Actions**, add:
   **Secrets**
   - `IG_ACCESS_TOKEN` (Instagram Business long-lived)
   - `IG_USER_ID` (Instagram Business numeric id)
   - `PINTEREST_ACCESS_TOKEN`
   **Variables**
   - `AFFILIATE_TAG` = `neurostart-21`
   - `OPENAI_API_KEY` = (optional)
   - `HUGGINGFACE_API_TOKEN` = (optional, for your own use later)
   - `PINTEREST_APP_ID` = (optional, not needed for simple pin posting)
   - `PINTEREST_APP_SECRET` = (optional)
   - `PINTEREST_BOARD_ID` = your board id (e.g., "1234567890123")
   - `SITE_BASE_URL` = `https://<your-username>.github.io/<your-repo>/`
   - `BRAND_NAME` = `NeuroStart.ai`
   - `DEFAULT_HASHTAGS` = `#DealsIndia #OfferAlert #SaveMore #BudgetBuys`
4) Commit & push. The cron will run each morning (08:00 IST), generate
   - `/public/deals.js`,
   - `/public/posts/YYYY-MM-DD/*.jpg`,
   - and optionally **post to Instagram + Pinterest** if secrets exist.

> Until you add Amazon keys (PA-API), the adapter will **fallback to the included CSV sample** so you can see everything working.

---

## Local Dev
```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env  # set SITE_BASE_URL etc. for local
python backend/pipeline.py --limit 4 --post-instagram false --post-pinterest false
```

---

## Folder Structure
```
backend/
  adapters/
    amazon_in_adapter.py   # PA-API v5 stub + CSV fallback
    csv_adapter.py
  caption_generator.py
  image_generator.py
  instagram_poster.py
  pinterest_poster.py
  llm_filter.py
  pipeline.py
  utils/
    affiliate.py
    shortlinks.py
data/
  sample_deals.csv
public/
  index.html, style.css, script.js, deals.js, robots.txt, sitemap.xml, feed.xml, icons/*
.github/workflows/
  cron.yml     # daily generator
  site.yml     # sitemap/feed refresher
.env.example
requirements.txt
```

---

## Notes on Amazon PA-API (India)
- You’ll need: **Access Key**, **Secret Key**, **Associate Tag** (yours is `neurostart-21`).
- The provided adapter includes a **signing stub** and a **mock fallback**.
- When keys are present, it will query Amazon India endpoints to fetch products by keywords.
- Always comply with Amazon Associates Program Policies.

Enjoy building! 🚀
