from fastapi import status, HTTPException, Depends, APIRouter
from .. import models, schemas, utils
from sqlalchemy.orm import Session
from ..database import get_db

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.UserCreateResp)
def create_user(user: schemas.UserCreateRqst, db: Session = Depends(get_db)):
    # hash the password
    user.password = utils.hash(user.password)
    # create new user
    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.get("/{id}", response_model=schemas.UserGetResp)
def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        print(f"Key error: Could not locate user with id: {id}")
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = f"User {id} not found!")
    return user