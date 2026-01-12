from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
import jwt #PyJWT==2.10.1
from datetime import datetime, timedelta, timezone
from . import schemas, database, models
from fastapi.security.oauth2 import OAuth2PasswordBearer
from .config import settings
oauth2_scheme =  OAuth2PasswordBearer(tokenUrl="auth/login")

SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes

# Create a JWT token
def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# Verify and decode a JWT token
def verify_access_token(token: str, credentials_exception):
    try:
        # Decode the JWT token and extract the payload
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        # print(payload)
        user_id = payload.get("user_id")
        if user_id is None:
            raise credentials_exception
        token_data = schemas.TokenData(id=int(user_id))
    except jwt.PyJWTError:
        raise credentials_exception
    return token_data

# Dependency to get the current user based on the token
def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(database.get_db)):
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Could not validate credentials",headers={"WWW-Authenticate": "Bearer"},)
    token_data = verify_access_token(token, credentials_exception)
    user = db.query(models.User).filter(models.User.id == token_data.id).first()
    if user is None:
        raise credentials_exception
    return user 