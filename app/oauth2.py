from fastapi import Depends, status, HTTPException
from fastapi.security.oauth2 import OAuth2PasswordBearer
from jose import JWTError, jwt
from datetime import datetime, timedelta

from sqlalchemy.orm.session import Session
from . import schemas, database, models
from .config import settings

# routing endpoint for login
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

SECRET_KEY = settings.jwt_secret_key # created by: openssl rand -hex 32
ALGORITHM = settings.jwt_algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = settings.jwt_expire_minutes

def create_access_token(data: dict):
    """
    Creates an access token valid for ACCESS_TOKEN_EXPIRE_MINUTES putting data into payload.

    Parameters
    ----------
    data : dict
        Data to be encoded in the payload.

    Returns
    -------
    str
        Access token.
    """
    to_encode = data.copy()
    time_expiration = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": time_expiration})

    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def verify_access_token(token: str, credentials_exception):
    """
    Verifies an access token.

    Parameters
    ----------
    token : str
        Token to verify.
    credentials_exception : Exception
        Exception to raise when an error occurs.

    Raises
    ------
    credential_exception
        Passed as a parameter.

    Returns
    -------
    schemas.TokenData
        User data within the token's payload.   
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        id: str = payload.get("user_id")
        if id is None:
            raise credentials_exception
        token_data = schemas.TokenData(id=id)
    except JWTError:
        raise credentials_exception
    
    return token_data

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(database.get_db)):
    """
    Takes the access token from a path operation (for which this function is passed as a dependency),
    verifies the token, and then extracts the user data from the database.

    Parameters
    ----------
    token : str
        Access token to be decoded/validated.

    Returns
    -------
    models.User
        User data whose id is within the token's payload. 
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials.", 
        headers={"WWW-Authenticate": "Bearer"}
    )

    token_data = verify_access_token(token, credentials_exception)
    user = db.query(models.User).filter(models.User.id == token_data.id).first()
    return user
