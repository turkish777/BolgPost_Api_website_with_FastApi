# routers/posts.py
from fastapi import APIRouter, Depends, HTTPException , status
from sqlalchemy.orm import Session
import models, schemas, database
from auth import get_current_user, admin_required
from fastapi import BackgroundTasks

router = APIRouter(prefix="/posts", tags=["Posts"])

# background task 
def log_post_creation(post_id: int, username: str):
    print(f"[BACKGROUND] Post {post_id} created by user '{username}'")


# Create post
@router.post("/", response_model=schemas.PostOut)
def create_post(
    post: schemas.PostCreate,
    background_tasks: BackgroundTasks,
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(get_current_user),
):
    db_post = models.Post(
        title=post.title,
        content=post.content,
        owner_id=current_user.id
    )

    db.add(db_post)
    db.commit()
    db.refresh(db_post)

    # Run task AFTER response is sent
    background_tasks.add_task(
        log_post_creation,
        db_post.id,
        current_user.username
    )

    return db_post


# Get all posts
@router.get("/", response_model=list[schemas.PostOut])
def get_posts(db: Session = Depends(database.get_db)):
    return db.query(models.Post).all()


@router.delete("/{post_id}")
def delete_post(
    post_id: int,
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(get_current_user)
):
    post = db.query(models.Post).filter(
        models.Post.id == post_id
    ).first()

    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Post not found"
        )

    # RBAC CHECK
    if post.owner_id != current_user.id and current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not allowed to delete this post"
        )

    db.delete(post)
    db.commit()

    return {"msg": "Post deleted successfully"}


# Delete post (RBAC)
'''@router.delete("/{post_id}")
def delete_post(post_id: int, db: Session = Depends(database.get_db),
                current_user: models.User = Depends(get_current_user)):
    post = db.query(models.Post).filter(models.Post.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    if post.owner_id != current_user.id and current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Not allowed to delete")
    db.delete(post)
    db.commit()
    return {"detail": "Post deleted"}'''

