# Tech News Agent

Lightweight FastAPI-based agent to scrape, summarize, classify, and deliver technology news.

**Status:** Work in progress — README placeholder with screenshot area.

**Repository layout (high level):**

- `agent.py`, `main.py` — core orchestration and FastAPI entrypoint
- `domains/` — per-domain pipelines (tech, finance, politics, etc.)
- `tools/` — scrapers, normalizers, dedupe, summarizer, email sender
- `data/` — raw and processed data
- `static/` — static assets (screenshots, example outputs)
- `requirements.txt` — Python dependencies

## Quickstart

Prerequisites:

- Python 3.10+ (recommended)
- Git

1. Create and activate a virtual environment (Windows PowerShell):

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

2. Install dependencies:

```powershell
pip install -r requirements.txt
```

3. Run the app (development):

```powershell
pip install uvicorn
uvicorn main:app --reload --port 8000
```

Visit http://127.0.0.1:8000/docs for the OpenAPI docs.

## Screenshot

![App screenshot](static\news1.png)
![App screenshot](static\news2.png)

## Development notes

- Use `tools/` scripts to run scrapers and processors locally.
- Keep secrets out of the repo: use `.env` or environment variables (see `config.py`).

## Contributing

Feel free to open issues or PRs. Add tests under a `tests/` directory if you add functionality.

## License

TBD
tech-news-agent/
│
├── agent.py               # Master controller
├── main.py                # Entry point
│
├── domains/
│   ├── tech.py             # Tech news pipeline
│   ├── finance.py          # Indian stock market pipeline
│   ├── ai_research.py      # Optional: AI papers
│   └── others.py           # Future domains
│
├── tools/
│   ├── scraper.py          # Modular scrapers (RSS, Reddit, APIs)
│   ├── summarizer.py       # Summarization + keyword extraction
│   ├── deduplication.py    # Deduplicate articles
│   ├── topic_classifier.py # Topic tagging (Tech, Finance, AI)
│   ├── email_sender.py     # Email service
│   └── utils.py
│
├── data/
│   ├── raw/
│   ├── processed/
│   └── history.json
│
├── configs/
│   ├── sources.yaml        # All RSS, API, subreddit, Twitter handles etc.
│   └── credentials.env
│
└── requirements.txt
