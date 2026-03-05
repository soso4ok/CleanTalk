from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.crud import create_post, delete_post, get_post_by_id, get_posts, update_post
from app.database import get_db
from app.dependencies import TokenData, get_current_user
from app.schemas import PostCreate, PostListResponse, PostResponse, PostUpdate

router = APIRouter(prefix="/posts", tags=["posts"])


@router.get("", response_model=PostListResponse)
def list_posts(
    page: int = Query(1, ge=1),
    size: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db),
):
    posts, total = get_posts(db, page=page, size=size)
    return PostListResponse(
        items=[PostResponse.model_validate(p) for p in posts],
        total=total,
        page=page,
        size=size,
    )


@router.post("", response_model=PostResponse, status_code=status.HTTP_201_CREATED)
def create_new_post(
    post_in: PostCreate,
    db: Session = Depends(get_db),
    user: TokenData = Depends(get_current_user),
):
    post = create_post(db, post_in, author_id=user.user_id, author_name=user.username)
    return post


@router.get("/{post_id}", response_model=PostResponse)
def read_post(post_id: str, db: Session = Depends(get_db)):
    post = get_post_by_id(db, post_id)
    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
    return post


@router.put("/{post_id}", response_model=PostResponse)
def update_existing_post(
    post_id: str,
    post_in: PostUpdate,
    db: Session = Depends(get_db),
    user: TokenData = Depends(get_current_user),
):
    post = get_post_by_id(db, post_id)
    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
    if post.author_id != user.user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not the post owner")
    return update_post(db, post, post_in)


@router.delete("/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_existing_post(
    post_id: str,
    db: Session = Depends(get_db),
    user: TokenData = Depends(get_current_user),
):
    post = get_post_by_id(db, post_id)
    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
    if post.author_id != user.user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not the post owner")
    delete_post(db, post)
