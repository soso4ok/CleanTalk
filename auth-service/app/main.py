import logging
import time

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

from app.routers import users

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="CleanTalk Auth Service",
    version="1.1.0",
    description="""
    Microservice for managing user authentication and profile data.
    
    Features:
    * **Identity Management**: User registration and login.
    * **Secure Access**: JWT-based authentication for other microservices.
    * **Profile Access**: Retrieve the current user's profile and identity.
    """,
    terms_of_service="http://example.com/terms/",
    contact={
        "name": "CleanTalk Security",
        "url": "http://localhost:5173/security",
        "email": "security@cleantalk.example.com",
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


app.include_router(users.router, tags=["auth"])


@app.get("/health")
def health_check():
    return {"status": "ok", "service": "auth"}
