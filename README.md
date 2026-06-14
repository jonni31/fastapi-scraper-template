# 🕷️ FastAPI Scraper Template

Production-ready web scraper with FastAPI.

## Features
- ⚡ Async FastAPI endpoints
- 🕸️ BeautifulSoup + httpx
- 🛡️ Rate limiting
- 📊 JSON output

## Install
```bash
pip install -r requirements.txt
uvicorn main:app --reload
```

## Usage
```bash
curl -X POST http://localhost:8000/scrape \
  -H "Content-Type: application/json" \
  -d '{"url":"https://example.com","selector":"h1"}'
```

## API
| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Health check |
| `/scrape` | POST | Scrape a URL |
| `/docs` | GET | Swagger UI |