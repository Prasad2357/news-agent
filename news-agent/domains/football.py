# domains/football.py
def enhance_football(item):
    item.setdefault("priority", 3)
    t = (item.get("title","") + " " + item.get("snippet","")).lower()
    # Arsenal priority
    if "arsenal" in t or "arteta" in t:
        item["priority"] = 1
    # Top 5 league keywords bump
    if any(k in t for k in ["premier league", "la liga", "serie a", "bundesliga", "ligue 1", "uefa"]):
        item["priority"] = min(item["priority"], 2)
    return item
