from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.crud import create_comment, delete_comment, get_comment_by_id, get_comments_for_post
from app.database import get_db
from app.dependencies import TokenData, get_current_user
from app.moderation import moderate_comment
from app.schemas import CommentCreate, CommentResponse, ModerationResult

router = APIRouter(prefix="/comments", tags=["comments"])


@router.get(
    "",
    response_model=list[CommentResponse],
    summary="List comments for a post",
    description="Retrieves all comments associated with a specific `post_id`.",
)
def list_comments(
    post_id: str = Query(..., description="The UUID of the post to fetch comments for"),
    db: Session = Depends(get_db),
):
    comments = get_comments_for_post(db, post_id)
    return [CommentResponse.model_validate(c) for c in comments]


@router.post(
    "",
    response_model=ModerationResult,
    status_code=status.HTTP_201_CREATED,
    summary="Submit a new comment",
    description="""
    Submits a comment for moderation and storage. 
    
    The comment body is analyzed by the configured AI backend (Gemini by default). 
    * If classified as **spam**, a 422 error is returned.
    * If classified as **hide**, the comment is saved but remains invisible in standard listings.
    * If classified as **ok**, the comment is saved and published.
    """,
    responses={
        401: {"description": "Missing or invalid authentication token"},
        422: {"description": "Comment rejected as spam by AI moderator"},
    },
)
async def submit_comment(
    comment_in: CommentCreate,
    db: Session = Depends(get_db),
    user: TokenData = Depends(get_current_user),
):
    verdict = await moderate_comment(comment_in.body)

    if verdict == "spam":
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Your comment was classified as spam and has been rejected.",
        )

    comment = create_comment(
        db,
        comment_in,
        author_id=user.user_id,
        author_name=user.username,
        status=verdict,
    )

    return ModerationResult(
        comment_id=comment.id,
        verdict=verdict,
        body=comment.body,
    )


@router.delete(
    "/{comment_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a comment",
    description="Removes a comment from the database. Only the author of the comment is allowed to delete it.",
    responses={
        401: {"description": "Missing or invalid authentication token"},
        403: {"description": "Access denied: Not the comment owner"},
        404: {"description": "Comment not found"},
    },
)
def remove_comment(
    comment_id: str,
    db: Session = Depends(get_db),
    user: TokenData = Depends(get_current_user),
):
    comment = get_comment_by_id(db, comment_id)
    if comment is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Comment not found"
        )
    if comment.author_id != user.user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Not the comment owner"
        )
    delete_comment(db, comment)
