# FastAPI with MongoDB (Async and Sync) for Processing News

## Overview

This guide introduces how to build high-performance APIs using **FastAPI** integrated with **MongoDB**, covering both **synchronous** and **asynchronous** approaches. We will explore the following:

- What is FastAPI?
- What is MongoDB?
- Sync vs Async in FastAPI
- Setting up MongoDB Connection (Sync and Async)
- Designing News Processing API
- Practical Code Examples (Sync and Async)
- Performance Considerations

---

## Section 1: What is FastAPI?

### Explanation:
**FastAPI** is a modern, high-performance web framework for building APIs with Python. It is built on **Starlette** for the web layer and **Pydantic** for data validation.

### Key Features:
- Asynchronous support using Python's `async` and `await`.
- Automatic API documentation (Swagger & ReDoc).
- High performance comparable to Node.js and Go.

---

## Section 2: What is MongoDB?

### Explanation:
**MongoDB** is a NoSQL database that stores data in **JSON-like documents**. It is highly scalable, flexible, and widely used in modern applications.

### Why MongoDB with FastAPI?
- Schema flexibility for dynamic data (e.g., news articles).
- Native JSON support for easy API integration.

---

## Section 3: Sync vs Async in FastAPI

### Sync (Synchronous):
- Uses standard blocking I/O.
- Simpler to implement but less efficient for high-concurrency scenarios.

### Async (Asynchronous):
- Uses `async` and `await` for non-blocking I/O.
- Handles thousands of requests concurrently with fewer resources.

**When to choose Async?**
- When the app handles multiple I/O-bound operations like database calls or API requests.

---

## Section 4: Setting up MongoDB Connection

### 4.1 Synchronous Setup with `pymongo`
```python
from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017")
db = client.news_db
collection = db.articles
```

### 4.2 Asynchronous Setup with `motor`
```python
from motor.motor_asyncio import AsyncIOMotorClient

client = AsyncIOMotorClient("mongodb://localhost:27017")
db = client.news_db
collection = db.articles
```

---

## Section 5: Designing News Processing API

### Requirements:
- Add a news article (title, content, tags, published_date).
- Fetch all news articles.
- Fetch by tag.

### Data Model (Pydantic):
```python
from pydantic import BaseModel
from typing import List
from datetime import datetime

class NewsArticle(BaseModel):
    title: str
    content: str
    tags: List[str]
    published_date: datetime
```

---

## Section 6: Sync Implementation

### Full Example:
```python
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
```

---

## Section 7: Async Implementation

### Full Example:
```python
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
```

---

## Section 8: Performance Considerations

- **Async Advantage:** Better for concurrent requests.
- Use **indexes** in MongoDB for faster queries.
- Use **connection pooling** for optimized DB performance.
- Avoid blocking calls in async routes.

---

## Section 9: Summary Table

| Feature        | Sync (pymongo)      | Async (motor)           |
|---------------|---------------------|--------------------------|
| Blocking      | Yes                | No                       |
| Performance   | Lower under load   | High concurrency support |
| Ease of use   | Simple             | Slightly complex         |

---

## Section 10: Knowledge Check — Interview Questions

1. What is FastAPI and why is it fast?
2. Explain Sync vs Async in FastAPI.
3. Why use MongoDB with FastAPI?
4. What is `motor` and how is it different from `pymongo`?
5. How to implement non-blocking DB operations in FastAPI?
6. What happens if you use blocking calls inside an async route?
7. Explain the role of Pydantic in FastAPI.
8. How does connection pooling affect performance?
9. When should you choose sync over async?
10. How to handle large datasets in MongoDB efficiently?

---

This article equips you with both theory and practical skills to implement scalable FastAPI applications using MongoDB with synchronous and asynchronous patterns.
