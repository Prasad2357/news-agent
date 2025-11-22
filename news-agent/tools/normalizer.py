# tools/normalizer.py
import hashlib
from readability import Document
from bs4 import BeautifulSoup
import requests
try:
    from config import HEADERS
except Exception:
    HEADERS = None  # no-op, keep readability import working

def normalize_item(item):
    normalized = {
        "id": item.get("id") or hashlib.sha1((item.get("url","") + item.get("title","")).encode()).hexdigest(),
        "title": (item.get("title") or "").strip(),
        "url": item.get("url") or "",
        "snippet": (item.get("snippet") or "").strip(),
        "published": item.get("published") or "",
        "source": item.get("source") or "",
        "domain": item.get("domain") or "general",
        "raw": item
    }
    return normalized

def fetch_article_text(url, timeout=8):
    try:
        resp = requests.get(url, timeout=timeout, headers={"User-Agent":"TechDigestBot/1.0"})
        resp.raise_for_status()
        doc = Document(resp.text)
        title = doc.short_title()
        summary_html = doc.summary()
        soup = BeautifulSoup(summary_html, "html.parser")
        text = soup.get_text(separator="\n").strip()
        snippet = "\n".join(text.split("\n")[:6])
        return {"title": title or "", "text": text, "snippet": snippet}
    except Exception:
        # fallback: try simple parse
        try:
            r = requests.get(url, timeout=timeout, headers={"User-Agent":"TechDigestBot/1.0"})
            s = BeautifulSoup(r.text, "html.parser")
            title = s.title.string if s.title else ""
            first_p = s.find("p")
            snippet = first_p.text.strip() if first_p else ""
            return {"title": title or "", "text": "", "snippet": snippet}
        except Exception:
            return {"title":"", "text":"", "snippet":""}
