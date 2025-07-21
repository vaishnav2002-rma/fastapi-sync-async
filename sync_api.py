from fastapi import FastAPI
from pymongo import MongoClient
import requests

app = FastAPI()

# MongoDB setup
client = MongoClient("mongodb://localhost:27017")
db = client.news_db
collection = db.articles

# NewsAPI URL
API_URL = "https://newsapi.org/v2/everything?q=football&apiKey=455d9eef64ec4d8b96bf6f3017a0f760"

@app.post("/fetch-news")
def fetch_and_store_news():
    response = requests.get(API_URL)
    if response.status_code != 200:
        return {"error": "Failed to fetch news from NewsAPI"}
    
    data = response.json()
    articles = data.get("articles", [])

    for article in articles:
        doc = {
            "source": article["source"]["name"],
            "author": article.get("author"),
            "title": article.get("title"),
            "description": article.get("description"),
            "url": article.get("url"),
            "urlToImage": article.get("urlToImage"),
            "publishedAt": article.get("publishedAt"),
            "content": article.get("content"),
        }
        # Use the URL as a unique identifier to avoid duplicates
        collection.update_one({"url": doc["url"]}, {"$set": doc}, upsert=True)

    return {"message": f"{len(articles)} news articles fetched and stored."}

@app.get("/news")
def get_news():
    articles = list(collection.find())
    for a in articles:
        a["_id"] = str(a["_id"])  # Convert ObjectId to string
    return articles
