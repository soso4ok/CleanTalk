import logging
import time

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

from app.routers import posts

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="CleanTalk Post Service",
    version="1.1.0",
    description="""
    Microservice for managing blog posts.
    
    Features:
    * **Post Management**: Create, read, update, and delete blog posts.
    * **Pagination**: Built-in support for paginated post listings.
    * **Authorization**: JWT-based protection for creating, updating, and deleting posts.
    """,
    terms_of_service="http://example.com/terms/",
    contact={
        "name": "CleanTalk Social",
        "url": "http://localhost:5173/blog",
        "email": "blog@cleantalk.example.com",
    },
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.middleware("http")
async def log_requests(request: Request, call_next):
    start = time.time()
    response = await call_next(request)
    duration = round(time.time() - start, 3)
    logger.info("%s %s → %s (%.3fs)", request.method, request.url.path, response.status_code, duration)
    return response


app.include_router(posts.router)


@app.get("/health")
def health_check():
    return {"status": "ok", "service": "post"}
