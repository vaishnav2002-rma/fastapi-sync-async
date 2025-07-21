from fastapi import FastAPI
from motor.motor_asyncio import AsyncIOMotorClient
import httpx

app = FastAPI()

# MongoDB setup
client = AsyncIOMotorClient("mongodb://localhost:27017")
db = client.news_db
collection = db.articles

# NewsAPI URL
API_URL = "https://newsapi.org/v2/everything?q=football&apiKey=455d9eef64ec4d8b96bf6f3017a0f760"

@app.post("/fetch-news")
async def fetch_and_store_news():
    # Fetch data from NewsAPI asynchronously
    async with httpx.AsyncClient() as http_client:
        response = await http_client.get(API_URL)
        if response.status_code != 200:
            return {"error": "Failed to fetch news from NewsAPI"}
        data = response.json()

    articles = data.get("articles", [])

    # Insert or update each article in MongoDB
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
        await collection.update_one({"url": doc["url"]}, {"$set": doc}, upsert=True)

    return {"message": f"{len(articles)} news articles fetched and stored."}

@app.get("/news")
async def get_news():
    # Fetch all articles from MongoDB asynchronously
    articles = []
    async for doc in collection.find():
        doc["_id"] = str(doc["_id"])  # Convert ObjectId to string
        articles.append(doc)
    return articles
