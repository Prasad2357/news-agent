# domains/politics.py
def enhance_politics(item):
    item.setdefault("priority", 3)
    t = (item.get("title","") + " " + item.get("snippet","")).lower()
    if "maharashtra" in t or "mumbai" in t or "pune" in t:
        item["priority"] = 1
    elif "india" in t:
        item["priority"] = 2
    return item
