from datetime import datetime

from pydantic import BaseModel


class PostCreate(BaseModel):
    title: str
    body: str


class PostUpdate(BaseModel):
    title: str | None = None
    body: str | None = None


class PostResponse(BaseModel):
    id: str
    title: str
    body: str
    author_id: str
    author_name: str
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class PostListResponse(BaseModel):
    items: list[PostResponse]
    total: int
    page: int
    size: int


class TitleSuggestion(BaseModel):
    suggested_title: str
