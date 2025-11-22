# tools/summarizer.py
import google.generativeai as genai
import os
from config import GEMINI_API_KEY
import time
genai.configure(api_key=GEMINI_API_KEY)

MODEL = "gemini-2.5-flash"

def summarize_item(title, snippet, url=None):
    prompt = f"""Summarize this news item concisely for a daily digest.

Title: {title}
Snippet: {snippet}
URL: {url}

Output:
- Two short bullet points (each <= 160 chars)
- One sentence: Why it matters: <reason>

Be factual and concise. If details are missing, do not invent them.
"""
    try:
        model = genai.GenerativeModel(MODEL)
        resp = model.generate_content(prompt)
        text = (resp.text or "").strip()
        # small throttle
        time.sleep(0.25)
        return text
    except Exception as e:
        # fallback: simple snippet fallback
        fallback = (snippet or "")[:250]
        return f"- {fallback}\nWhy it matters: See link {url}"
