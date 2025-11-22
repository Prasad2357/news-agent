# agent.py
from config import DOMAINS_ENABLED, TOP_N_PER_DOMAIN
from tools.scraper import fetch_all
from tools.normalizer import normalize_item, fetch_article_text
from tools.dedupe import init_db, is_sent, mark_sent
from tools.classifier import classify_item
from tools.summarizer import summarize_item
from tools.email_sender import build_html_digest, send_email_html
from collections import defaultdict
import time

from domains.tech import enhance_tech
from domains.finance import enhance_finance
from domains.football import enhance_football
from domains.politics import enhance_politics

def apply_domain_logic(cat, item):
    if cat.startswith("football"):
        return enhance_football(item)
    if cat.startswith("politics"):
        return enhance_politics(item)
    if cat == "finance":
        return enhance_finance(item)
    if cat == "tech":
        return enhance_tech(item)
    return item

def run_agent():
    print("🤖 Agent starting...")
    init_db()

    # fetch fewer items per feed to keep top-N small
    raw_items = fetch_all(limit_per_feed=5, use_reddit=True)
    print(f"Fetched {len(raw_items)} raw items")

    normalized = []
    for item in raw_items:
        it = normalize_item(item)
        if not it.get("snippet"):
            info = fetch_article_text(it.get("url") or "")
            it["snippet"] = info.get("snippet", "")
            if not it.get("title"):
                it["title"] = info.get("title") or it.get("title")
        normalized.append(it)

    # classify & group
    grouped = defaultdict(list)  # {domain: {category: [items]}} but here domain=category root
    temp_map = defaultdict(list)

    for it in normalized:
        if is_sent(it["id"]):
            continue
        cls = classify_item(it.get("title",""), it.get("snippet",""))
        cat = cls.get("category", "other")
        # domain-level toggle (first part before underscore)
        domain_main = cat.split("_")[0]
        if not DOMAINS_ENABLED.get(domain_main, False):
            continue
        # enhance
        it = apply_domain_logic(cat, it)
        temp_map[cat].append(it)

    # limit top N per category using priority
    final_items = defaultdict(dict)  # {domain: {category: [items]}}
    for cat, items in temp_map.items():
        sorted_items = sorted(items, key=lambda x: x.get("priority", 10))
        final_items.setdefault(cat.split("_")[0], {})[cat] = sorted_items[:TOP_N_PER_DOMAIN]

    # Summarize and mark sent
    for domain, cats in final_items.items():
        for cat, items in cats.items():
            for it in items:
                it["summary"] = summarize_item(it.get("title",""), it.get("snippet",""), it.get("url"))
                mark_sent(it)
                time.sleep(0.2)

    # check empty
    total = sum(len(v2) for v in final_items.values() for v2 in v.values())
    if total == 0:
        print("No new items to send.")
        return

    # build email (expects structure domain->category->items)
    html_body = build_html_digest(final_items)
    send_email_html("📰 Your Daily Multi-Domain Digest", html_body)
    print("✅ Agent finished.")
