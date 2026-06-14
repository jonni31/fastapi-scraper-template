"""FastAPI Scraper Template."""
import time
from datetime import datetime
from typing import Optional
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, HttpUrl
import httpx
from bs4 import BeautifulSoup

app = FastAPI(title="Scraper API")
LIMITS = {}

def check_limit():
    now = time.time()
    LIMITS.setdefault("g", [])
    LIMITS["g"] = [t for t in LIMITS["g"] if now-t < 60]
    if len(LIMITS["g"]) >= 30: return False
    LIMITS["g"].append(now); return True

class Req(BaseModel):
    url: HttpUrl
    selector: Optional[str] = None

async def scrape(url, selector=None):
    h = {"User-Agent": "Mozilla/5.0 Chrome/120.0.0.0"}
    async with httpx.AsyncClient(timeout=15, follow_redirects=True) as c:
        r = await c.get(str(url), headers=h)
        r.raise_for_status()
    soup = BeautifulSoup(r.text, "html.parser")
    items = [e.get_text(strip=True) for e in soup.select(selector)] if selector else [soup.get_text(strip=True)[:5000]]
    return {"url": str(url), "count": len(items), "data": items, "ts": datetime.utcnow().isoformat()}

@app.get("/")
def health(): return {"status": "ok"}

@app.post("/scrape")
async def scrape_one(req: Req):
    if not check_limit(): raise HTTPException(429)
    try: return await scrape(req.url, req.selector)
    except Exception as e: raise HTTPException(400, str(e))
