from fastapi import status, HTTPException, Depends, APIRouter
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from .. import database, schemas, models, utils, oauth2

router = APIRouter(
    tags=["Authentication"]
)

@router.post("/login", response_model=schemas.Token)
def login(credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):
    # check if the user exists
    user = db.query(models.User).filter(models.User.email == credentials.username).first()
    if not user:
        print(f"Could not find user with email: {credentials.username}")
        raise HTTPException(
            status_code = status.HTTP_401_UNAUTHORIZED,
            detail = f"Invalid username or password!", 
            headers={"WWW-Authenticate": "Bearer"})
    # verify user password
    if not utils.verify(credentials.password, user.password):
        print(f"User email and password do not match.")
        raise HTTPException(
            status_code = status.HTTP_401_UNAUTHORIZED,
            detail = f"Invalid username or password!", 
            headers={"WWW-Authenticate": "Bearer"})
    # create and return a token
    access_token = oauth2.create_access_token(data = {"user_id": user.id})
    return {"access_token": access_token, "token_type": "bearer"}
