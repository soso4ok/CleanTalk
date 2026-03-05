import logging
import time

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

from app.routers import comments

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="CleanTalk Comment Service",
    version="1.0.0",
    description="Comment CRUD with AI moderation pipeline",
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


app.include_router(comments.router)


@app.get("/health")
def health_check():
    return {"status": "ok", "service": "comment"}
