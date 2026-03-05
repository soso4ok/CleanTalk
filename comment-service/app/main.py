from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers import comments

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

app.include_router(comments.router)


@app.get("/health")
def health_check():
    return {"status": "ok", "service": "comment"}
