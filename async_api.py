from fastapi import FastAPI
from pydantic import BaseModel
from motor.motor_asyncio import AsyncIOMotorClient
from typing import Optional, List
from datetime import datetime

app = FastAPI()

# MongoDB (async)
client = AsyncIOMotorClient("mongodb://localhost:27017")
db = client.news_db
collection = db.articles

# Pydantic model for incoming news data
class NewsArticle(BaseModel):
    title: str
    description: Optional[str] = None
    url: str
    source: str
    published_date: datetime

@app.post("/add-news")
async def add_news(article: NewsArticle):
    doc = article.dict()
    result = await collection.update_one({"url": doc["url"]}, {"$set": doc}, upsert=True)
    if result.upserted_id or result.modified_count:
        return {"message": "Article added/updated."}
    else:
        return {"message": "No changes made (article already exists)."}

@app.get("/news")
async def get_news():
    articles = []
    async for doc in collection.find():
        doc["_id"] = str(doc["_id"])
        articles.append(doc)
    return articles
