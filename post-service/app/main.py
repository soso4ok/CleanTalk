from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers import posts

app = FastAPI(
    title="CleanTalk Post Service",
    version="1.0.0",
    description="Blog post CRUD operations",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(posts.router)


@app.get("/health")
def health_check():
    return {"status": "ok", "service": "post"}
