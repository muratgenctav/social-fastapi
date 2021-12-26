from fastapi import status, APIRouter, Depends
from fastapi.exceptions import HTTPException
from .. import models, schemas, oauth2
from sqlalchemy.orm import Session
from ..database import get_db

router = APIRouter(
    prefix="/votes",
    tags=["Vote"]
)

@router.post("/", status_code=status.HTTP_201_CREATED)
def vote(vote: schemas.VoteRqst, db: Session = Depends(get_db), user: models.User = Depends(oauth2.get_current_user)):
    post_query = db.query(models.Post).filter(models.Post.id == vote.post_id)
    post_item = post_query.first()
    if not post_item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post {vote.post_id} does not exist")
    vote_query = db.query(models.Vote).filter(models.Vote.post_id == vote.post_id, models.Vote.user_id == user.id)
    vote_item = vote_query.first()
    if (vote.dir == schemas.VoteDirEnum.vote):
        if vote_item:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"User {user.id} has already voted on the post {vote.post_id}")
        new_vote = models.Vote(post_id = vote.post_id, user_id = user.id)
        db.add(new_vote)
        db.commit()
        return {"message": "Vote has been successfully added."}
    else:
        if not vote_item:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Could not find a vote from user {user.id} to the post {vote.post_id}")
        vote_query.delete(synchronize_session=False)
        db.commit()
        return{"message": "Vote has been successfully deleted."}