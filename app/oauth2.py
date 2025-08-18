from jose import JWTError, jwt
from datetime import datetime, timedelta
from . import schemas, database, models
from sqlalchemy.orm import Session
from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer
from .config import settings

'''
    ENVIRONMENT VARIABLES -> are variables that you configure on a computer (doesn't matter what system)
    and any application that we run on our computer will be able to access it
    this is more of a security problem so we don't hardcode our global variable like
    SECRET_KEY or some database related variables
'''

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login')

'''
    SECRET KEY
    ALGORITHM
    EXPIRATION TIME -> TO LIMIT THE TIME OF THE USER HOW MUCH IT WILL BE LOGED IN
'''

SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes


def create_access_token(data: dict):
    data_copy = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    data_copy.update({"exp": expire})

    jwt_token = jwt.encode(data_copy, SECRET_KEY, algorithm=ALGORITHM)

    return jwt_token


def verify_access_token(token: str, credentials_exception):
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
    # Dependency for our request -> so we make sure our user has a valid token
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED, detail=f"Invalid credentials", headers={"WWW-Authenticate": "Bearer"})

    token_user = verify_access_token(token, credentials_exception)

    user = db.query(models.User).filter(
        models.User.id == token_user.id).first()

    return user
