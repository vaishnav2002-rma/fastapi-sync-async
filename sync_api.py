from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from pymongo import MongoClient
from typing import List
from datetime import datetime

# FastAPI app
app = FastAPI()

# MongoDB connection
client = MongoClient("mongodb://localhost:27017")
db = client.news_db
collection = db.articles

# News article model
class NewsArticle(BaseModel):
    title: str
    description: str = None
    url: str
    source: str
    published_date: datetime

@app.post("/add-news")
def add_news(article: NewsArticle):
    doc = article.model_dump()
    result = collection.update_one({"url": doc["url"]}, {"$set": doc}, upsert=True)
    if result.upserted_id or result.modified_count:
        return {"message": "Article added/updated."}
    else:
        return {"message": "No changes made (article already exists)."}

@app.get("/news")
def get_news():
    articles = list(collection.find())
    for a in articles:
        a["_id"] = str(a["_id"])
    return articles
