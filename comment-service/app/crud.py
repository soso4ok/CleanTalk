from sqlalchemy.orm import Session

from app.models import Comment
from app.schemas import CommentCreate


def get_comments_for_post(db: Session, post_id: str) -> list[Comment]:
    return (
        db.query(Comment)
        .filter(Comment.post_id == post_id, Comment.status == "ok")
        .order_by(Comment.created_at.asc())
        .all()
    )


def create_comment(
    db: Session,
    comment_in: CommentCreate,
    author_id: str,
    author_name: str,
    status: str = "ok",
) -> Comment:
    comment = Comment(
        post_id=comment_in.post_id,
        author_id=author_id,
        author_name=author_name,
        body=comment_in.body,
        status=status,
    )
    db.add(comment)
    db.commit()
    db.refresh(comment)
    return comment


def get_comment_by_id(db: Session, comment_id: str) -> Comment | None:
    return db.query(Comment).filter(Comment.id == comment_id).first()


def delete_comment(db: Session, comment: Comment) -> None:
    db.delete(comment)
    db.commit()
