from fastapi import Depends, HTTPException, status, Response, APIRouter
from sqlalchemy import func
from sqlalchemy.orm import Session
from typing import List
from .. import models, schemas, oauth2
from ..database import get_db

router = APIRouter(
    prefix="/posts",
    tags=["Posts"] #to structure the docs
)

# GEt all posts
@router.get("/", response_model=List[schemas.PostWithVotes])
def get_post(db: Session = Depends(get_db), limit: int = 10, skip: int = 0, search: str = ""):
    # Join posts and votes to get vote counts for each post
    posts = db.query(
        models.Post, 
        func.count(models.Vote.post_id).label("votes")
    ).join(
        models.Vote, 
        models.Vote.post_id == models.Post.id, 
        isouter=True  # LEFT JOIN (includes posts with 0 votes)
    ).group_by(
        models.Post.id
    ).filter(
        models.Post.title.contains(search)
    ).limit(limit).offset(skip).all()
    
    return posts

#get single post
@router.get("/{id}", response_model=schemas.PostWithVotes)
def get_post(id: int, db: Session = Depends(get_db)):
    # Query for a single post with vote count
    post = db.query(
        models.Post, 
        func.count(models.Vote.post_id).label("votes")
    ).join(
        models.Vote, 
        models.Vote.post_id == models.Post.id, 
        isouter=True
    ).group_by(
        models.Post.id
    ).filter(
        models.Post.id == id
    ).first()
    
    if not post:
        raise HTTPException(status_code=404, detail=f"Post with id: {id} not found")
    
    return post

# create posts
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_post(post: schemas.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    new_post = models.Post(owner_id=current_user.id, **post.model_dump())
    # new_post.owner_id = current_user.id
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

#delete post
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()

    if post is None:
        raise HTTPException(status_code=404, detail=f"Post with id: {id} not found")
    
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested action")

    post_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

# update post
@router.put("/{id}", response_model=schemas.Post)
def update_post(id: int, payload: schemas.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    
    if post is None:
        raise HTTPException(status_code=404, detail=f"Post with id: {id} not found")
    
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested action")
    
    post_query.update(payload.model_dump(exclude_unset=True), synchronize_session=False)
    db.commit()
    db.refresh(post)
    return post