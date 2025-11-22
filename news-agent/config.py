# config.py
import os
from dotenv import load_dotenv
load_dotenv()

# Credentials
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
FROM_EMAIL = os.getenv("DIGEST_FROM_EMAIL")
TO_EMAIL = os.getenv("DIGEST_TO_EMAIL")
SMTP_PASSWORD = os.getenv("DIGEST_SMTP_PASSWORD")

# Reddit
REDDIT_CLIENT_ID = os.getenv("REDDIT_CLIENT_ID")
REDDIT_CLIENT_SECRET = os.getenv("REDDIT_CLIENT_SECRET")
REDDIT_USER_AGENT = os.getenv("REDDIT_USER_AGENT", "tech-news-agent")

# Domain toggles (set to False to disable)
DOMAINS_ENABLED = {
    "tech": True,
    "finance": True,
    "politics": True,
    "football": True,
}

# how many items per domain (top N)
TOP_N_PER_DOMAIN = int(os.getenv("TOP_N_PER_DOMAIN", 5))

# Feeds (RSS + sample sources)
TECH_FEEDS = [
    "https://techcrunch.com/feed/",
    "https://www.theverge.com/rss/index.xml",
    "https://feeds.arstechnica.com/arstechnica/technology",
]

FINANCE_FEEDS = [
    "https://www.moneycontrol.com/rss/MCtopnews.xml",
    "https://economictimes.indiatimes.com/markets/rssfeeds/1977021501.cms",
    "https://www.livemint.com/rss/markets"
]

# Politics sources (India & Maharashtra target)
POLITICS_FEEDS = [
    "https://timesofindia.indiatimes.com/rssfeedstopstories.cms",
    "https://www.hindustantimes.com/rss/topnews/rssfeed.xml",
    # include local Maharashtra feed if available
]

# Football sources: main outlets and league-specific feeds / sections
FOOTBALL_FEEDS = [
    "https://www.skysports.com/feeds/news/football/rss.xml",
    "https://www.goal.com/en/rss/news",
    "https://www.espn.com/espn/rss/football/news",
    # add club-level or league RSS as needed
]

# Reddit subreddits (optional)
REDDIT_SOURCES = {
    "tech": ["technology", "MachineLearning"],
    "finance": ["IndianStockMarket", "IndiaInvestments"],
    "politics": ["india", "IndianPolitics"],
    "football": ["soccer", "arsenal"]
}

# DB path for dedupe
DB_PATH = "data/sent_items.db"
