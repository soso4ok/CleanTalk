from sqlalchemy import func
from sqlalchemy.orm import Session

from app.models import Post
from app.schemas import PostCreate, PostUpdate


def get_posts(db: Session, page: int = 1, size: int = 10) -> tuple[list[Post], int]:
    total = db.query(func.count(Post.id)).scalar() or 0
    offset = (page - 1) * size
    posts = (
        db.query(Post)
        .order_by(Post.created_at.desc())
        .offset(offset)
        .limit(size)
        .all()
    )
    return posts, total


def get_post_by_id(db: Session, post_id: str) -> Post | None:
    return db.query(Post).filter(Post.id == post_id).first()


def create_post(db: Session, post_in: PostCreate, author_id: str, author_name: str) -> Post:
    post = Post(
        title=post_in.title,
        body=post_in.body,
        author_id=author_id,
        author_name=author_name,
    )
    db.add(post)
    db.commit()
    db.refresh(post)
    return post


def update_post(db: Session, post: Post, post_in: PostUpdate) -> Post:
    if post_in.title is not None:
        post.title = post_in.title
    if post_in.body is not None:
        post.body = post_in.body
    db.commit()
    db.refresh(post)
    return post


def delete_post(db: Session, post: Post) -> None:
    db.delete(post)
    db.commit()
