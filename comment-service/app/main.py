import logging
import time

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

from app.routers import comments

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="CleanTalk Comment Service",
    version="1.1.0",
    description="""
    Microservice for managing blog comments with an automated AI moderation pipeline.
    
    Features:
    * **CRUD Operations**: List, Submit, and Remove comments.
    * **AI Moderation**: Automatic classification (ok, hide, spam) using backend-agnostic AI handlers (Gemini, HuggingFace, or Mock).
    * **Authorization**: JWT-based protection for sensitive operations.
    """,
    terms_of_service="http://example.com/terms/",
    contact={
        "name": "CleanTalk Support",
        "url": "http://localhost:5173/support",
        "email": "support@cleantalk.example.com",
    },
    license_info={
        "name": "Apache 2.0",
        "url": "https://www.apache.org/licenses/LICENSE-2.0.html",
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


app.include_router(comments.router)


@app.get("/health")
def health_check():
    return {"status": "ok", "service": "comment"}
