# tools/classifier.py
import google.generativeai as genai
import os
from config import GEMINI_API_KEY
genai.configure(api_key=GEMINI_API_KEY)

MODEL = "gemini-2.5-flash"  # adjust if needed

# basic local fallback heuristic
def _heuristic(title, snippet):
    t = (title + " " + snippet).lower()
    if any(k in t for k in ["arsenal", "gunners", "mikel arteta"]):
        return "football_arsenal"
    if any(k in t for k in ["match", "goal", "league", "fifa", "transfer", "arsenal", "manchester", "barcelona", "realmadrid"]):
        return "football_europe"
    if any(k in t for k in ["maharashtra", "mumbai", "pune", "nagpur"]):
        return "politics_maharashtra"
    if any(k in t for k in ["india", "modi", "government", "lok sabha", "parliament"]):
        return "politics_india"
    if any(k in t for k in ["stock", "nifty", "sensex", "ipo", "market", "shares", "rbi"]):
        return "finance"
    if any(k in t for k in ["ai", "gpt", "openai", "machine learning", "model"]):
        return "tech"
    return "other"

def classify_item(title, snippet):
    # run heuristic first if short text
    if not title and not snippet:
        return {"category": "other"}

    # build prompt
    prompt = f"""
Classify the following news item into one of these categories:
tech, finance, politics_india, politics_maharashtra, football_europe, football_arsenal, other

Return only the category keyword.

Title: {title}
Snippet: {snippet}
"""
    try:
        model = genai.GenerativeModel(MODEL)
        resp = model.generate_content(prompt)
        text = (resp.text or "").strip().lower()
        # normalize
        text = text.splitlines()[0].strip()
        # if model output is unexpected, fallback to heuristic
        if text in ["tech", "finance", "politics_india", "politics_maharashtra", "football_europe", "football_arsenal", "other"]:
            return {"category": text}
        # fallback parse short words in text
        for k in ["arsenal", "maharashtra", "india", "football", "match", "stock", "ai"]:
            if k in text:
                return {"category": _heuristic(title, snippet)}
        return {"category": _heuristic(title, snippet)}
    except Exception as e:
        # fallback
        return {"category": _heuristic(title, snippet)}
