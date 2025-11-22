# domains/finance.py
def enhance_finance(item):
    # Finance-specific heuristics (detect tickers, markets, 'nifty', 'sensex', 'rbi')
    item.setdefault("priority", 2)
    t = (item.get("title","") + " " + item.get("snippet","")).lower()
    if any(k in t for k in ["nifty", "sensex", "rbi", "market", "stock", "ipo"]):
        item["priority"] = 1
    return item
