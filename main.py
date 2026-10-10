import os
import asyncio
import json
import websockets
from fastapi import FastAPI
import uvicorn

app = FastAPI()

@app.get("/")
def home():
    return {"status": "XiaoZhi Tavily Bridge is running"}

@app.get("/search")
async def search(q: str):
    import httpx

    api_key = os.getenv("TAVILY_API_KEY")
    if not api_key:
        return {"error": "TAVILY_API_KEY is not configured"}

    async with httpx.AsyncClient(timeout=20) as client:
        response = await client.post(
            "https://api.tavily.com/search",
            json={
                "api_key": api_key,
                "query": q,
                "search_depth": "basic",
                "max_results": 5
            }
        )
        response.raise_for_status()
        data = response.json()

    return {
        "query": q,
        "results": [
            {
                "title": item.get("title"),
                "url": item.get("url"),
                "content": item.get("content")
            }
            for item in data.get("results", [])
        ]
    }

if __name__ == "__main__":
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=int(os.getenv("PORT", "8000"))
    )
