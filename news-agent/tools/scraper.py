# tools/scraper.py
import feedparser
import requests
from datetime import datetime
from urllib.parse import urlparse
import hashlib
from bs4 import BeautifulSoup
import os
import time
from config import REDDIT_SOURCES, REDDIT_CLIENT_ID, REDDIT_CLIENT_SECRET, REDDIT_USER_AGENT

try:
    import praw
    _HAS_PRAW = True
except Exception:
    _HAS_PRAW = False

HEADERS = {"User-Agent": "TechDigestBot/1.0 (+https://example.com)"}

def _mkid(url, title=""):
    key = (url or "") + (title or "")
    return hashlib.sha1(key.encode("utf-8")).hexdigest()

def fetch_rss_urls(feed_urls, max_per_feed=5, domain_tag="general"):
    items = []
    for url in feed_urls:
        try:
            feed = feedparser.parse(url)
            entries = getattr(feed, "entries", [])[:max_per_feed]
            for entry in entries:
                link = entry.get("link", "") or entry.get("id", "")
                title = entry.get("title", "").strip()
                snippet = entry.get("summary", "") or entry.get("description", "")
                item = {
                    "id": _mkid(link, title),
                    "title": title,
                    "url": link,
                    "snippet": snippet,
                    "published": entry.get("published", str(datetime.utcnow())),
                    "source": urlparse(url).netloc,
                    "domain": domain_tag
                }
                items.append(item)
        except Exception as e:
            print("Feed error:", url, e)
    return items

def fetch_reddit(subreddit_list, limit=5, domain_tag="general"):
    items = []
    if not _HAS_PRAW:
        print("praw not installed or failed to import — skipping reddit")
        return items
    if not (REDDIT_CLIENT_ID and REDDIT_CLIENT_SECRET):
        print("Reddit credentials missing — skipping reddit")
        return items

    reddit = praw.Reddit(client_id=REDDIT_CLIENT_ID,
                         client_secret=REDDIT_CLIENT_SECRET,
                         user_agent=REDDIT_USER_AGENT)
    for sub in subreddit_list:
        try:
            for post in reddit.subreddit(sub).hot(limit=limit):
                link = post.url
                title = post.title
                snippet = (post.selftext or "")[:400]
                item = {
                    "id": _mkid(link, title),
                    "title": title,
                    "url": link,
                    "snippet": snippet,
                    "published": str(datetime.utcfromtimestamp(post.created_utc)),
                    "source": f"reddit/{sub}",
                    "domain": domain_tag
                }
                items.append(item)
        except Exception as e:
            print("Reddit error for", sub, e)
    return items

def fetch_article_text(url, timeout=6):
    if not url:
        return {"title": "", "snippet": ""}
    try:
        res = requests.get(url, headers=HEADERS, timeout=timeout)
        res.raise_for_status()
        soup = BeautifulSoup(res.text, "html.parser")
        title = soup.title.text.strip() if soup.title else ""
        p = soup.find("p")
        snippet = p.text.strip() if p else ""
        return {"title": title, "snippet": snippet}
    except Exception:
        return {"title": "", "snippet": ""}

def fetch_all(limit_per_feed=5, use_reddit=True):
    """
    Collects items across domain feeds configured in config.py.
    Returns list of item dicts.
    """
    from config import TECH_FEEDS, FINANCE_FEEDS, POLITICS_FEEDS, FOOTBALL_FEEDS, REDDIT_SOURCES

    all_items = []
    # fetch each domain's feeds with domain tag
    all_items += fetch_rss_urls(TECH_FEEDS, max_per_feed=limit_per_feed, domain_tag="tech")
    all_items += fetch_rss_urls(FINANCE_FEEDS, max_per_feed=limit_per_feed, domain_tag="finance")
    all_items += fetch_rss_urls(POLITICS_FEEDS, max_per_feed=limit_per_feed, domain_tag="politics")
    all_items += fetch_rss_urls(FOOTBALL_FEEDS, max_per_feed=limit_per_feed, domain_tag="football")

    if use_reddit:
        # reddit per domain
        for domain, subs in REDDIT_SOURCES.items():
            all_items += fetch_reddit(subs, limit=limit_per_feed, domain_tag=domain)

    # small sleep to be polite
    time.sleep(0.2)
    return all_items
