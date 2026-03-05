from datetime import datetime

from pydantic import BaseModel


class CommentCreate(BaseModel):
    post_id: str
    body: str


class CommentResponse(BaseModel):
    id: str
    post_id: str
    author_id: str
    author_name: str
    body: str
    status: str
    created_at: datetime

    model_config = {"from_attributes": True}


class ModerationResult(BaseModel):
    comment_id: str
    verdict: str  # ok | hide | spam
    body: str
