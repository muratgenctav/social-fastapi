from fastapi import status, HTTPException, Depends, APIRouter
from sqlalchemy.sql.functions import func
from .. import models, schemas, oauth2
from sqlalchemy.orm import Session
from sqlalchemy import or_
from ..database import get_db
from typing import List, Optional

router = APIRouter(
    prefix="/posts",
    tags=["Posts"]
)

@router.get("/", response_model=List[schemas.PostGetResp])
def get_posts(
        kword: Optional[str] = None,
        searchin: str = "title-content",
        limit: int = 10,
        skip: int = 0,
        db: Session = Depends(get_db), 
        user: models.User = Depends(oauth2.get_current_user)
    ):
    base_query = db.query(
            models.Post, func.count(models.Vote.user_id).label("votes")
        ).join(
            models.Vote, models.Vote.post_id == models.Post.id, isouter=True
        ).group_by(
            models.Post.id
        )
    if kword:
        if searchin == "title-content":
            posts = base_query.filter(or_(models.Post.title.contains(kword), models.Post.content.contains(kword))).limit(limit).offset(skip).all()
        elif searchin == "title":
            posts = base_query.filter(models.Post.title.contains(kword)).limit(limit).offset(skip).all()
        elif searchin == "content":
            posts = base_query.filter(models.Post.content.contains(kword)).limit(limit).offset(skip).all()
        else:
            print(f"Parameter error: Invalid value for parameter searchin: {searchin}")
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Invalid value for parameter 'searchin'")
        if not posts:
            print(f"No post satisfies search criteria: kword={kword}, searchin={searchin}, limit={limit}, skip={skip}")
            raise HTTPException(
                status_code = status.HTTP_404_NOT_FOUND,
                detail = f"No post satisfies search criteria")
    else:
        posts = base_query.limit(limit).offset(skip).all()
        if not posts:
            print(f"No post left")
            raise HTTPException(
                status_code = status.HTTP_404_NOT_FOUND,
                detail = f"No post left")
    return posts

@router.get("/own", response_model=List[schemas.PostGetResp])
def get_own_posts(db: Session = Depends(get_db), user: models.User = Depends(oauth2.get_current_user)):
    posts = db.query(
            models.Post, func.count(models.Vote.user_id).label("votes")
        ).join(
            models.Vote, models.Vote.post_id == models.Post.id, isouter=True
        ).group_by(
            models.Post.id
        ).filter(
            models.Post.owner_id == user.id
        ).all()
    if not posts:
        print(f"User {user.id} has no post")
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = f"User has no post")
    return posts

@router.get("/{id}", response_model=schemas.PostGetResp)
def get_post(id: int, db: Session = Depends(get_db), user: models.User = Depends(oauth2.get_current_user)):
    post = db.query(
            models.Post, func.count(models.Vote.user_id).label("votes")
        ).join(
            models.Vote, models.Vote.post_id == models.Post.id, isouter=True
        ).group_by(
            models.Post.id
        ).filter(
            models.Post.id == id
        ).first()
    if not post:
        print(f"Key error: Could not locate post {id}")
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = f"Post {id} not found!")
    return post

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.PostCreateResp)
def create_post(post: schemas.PostCreateRqst, db: Session = Depends(get_db), user: models.User = Depends(oauth2.get_current_user)):
    new_post = models.Post(owner_id=user.id, **post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

@router.delete("/{id}")
def delete_post(id: int, db: Session = Depends(get_db), user: models.User = Depends(oauth2.get_current_user)):
    query = db.query(models.Post).filter(models.Post.id == id)
    post = query.first()
    if not post:
        print(f"Key error: Could not locate post {id}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with {id} not found!")
    if post.owner_id != user.id:
        print(f"Authorization error: User {user.id} cannot delete post {id}")
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Not authorized to perform requested action")
    query.delete(synchronize_session=False)
    db.commit()
    return {"message": f"Post {id} was successfully deleted."}

@router.put("/{id}", response_model=schemas.PostCreateResp)
def update_post(id: int, updated_post: schemas.PostCreateRqst,  db: Session = Depends(get_db), user: models.User = Depends(oauth2.get_current_user)):
    query = db.query(models.Post).filter(models.Post.id == id)
    post = query.first()
    if not post:
        print(f"Key error: Could not locate post with id: {id}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with {id} not found!")
    if post.owner_id != user.id:
        print(f"Authorization error: User {user.id} cannot update post {id}")
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Not authorized to perform requested action")
    query.update(updated_post.dict(), synchronize_session=False)
    db.commit()
    return query.first()