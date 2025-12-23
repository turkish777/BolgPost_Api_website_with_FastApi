# routers/posts.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import models, schemas, database
from auth import get_current_user, admin_required

router = APIRouter(prefix="/posts", tags=["Posts"])

# Create post
@router.post("/", response_model=schemas.PostOut)
def create_post(post: schemas.PostCreate, db: Session = Depends(database.get_db),
                current_user: models.User = Depends(get_current_user)):
    db_post = models.Post(title=post.title, content=post.content, owner_id=current_user.id)
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    return db_post

# Get all posts
@router.get("/", response_model=list[schemas.PostOut])
def get_posts(db: Session = Depends(database.get_db)):
    return db.query(models.Post).all()

# Delete post (RBAC)
@router.delete("/{post_id}")
def delete_post(post_id: int, db: Session = Depends(database.get_db),
                current_user: models.User = Depends(get_current_user)):
    post = db.query(models.Post).filter(models.Post.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    if post.owner_id != current_user.id and current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Not allowed to delete")
    db.delete(post)
    db.commit()
    return {"detail": "Post deleted"}
