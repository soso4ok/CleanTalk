from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers import users

app = FastAPI(
    title="CleanTalk Auth Service",
    version="1.0.0",
    description="User registration, login, and JWT authentication",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(users.router, tags=["auth"])


@app.get("/health")
def health_check():
    return {"status": "ok", "service": "auth"}
