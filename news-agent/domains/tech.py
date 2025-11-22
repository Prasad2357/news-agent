# domains/tech.py
def enhance_tech(item):
    # Place-holder for tech-specific enrichment (e.g., detect product, company)
    # Add priority heuristics if needed
    item.setdefault("priority", 2)
    text = (item.get("title","") + " " + item.get("snippet","")).lower()
    if any(k in text for k in ["ai", "gpt", "openai", "model", "machine learning"]):
        item["priority"] = 1
    return item
