from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
import jwt #PyJWT==2.10.1
from datetime import datetime, timedelta, timezone
import secrets
from . import schemas, database, models
from fastapi.security.oauth2 import OAuth2PasswordBearer
from .config import settings
oauth2_scheme =  OAuth2PasswordBearer(tokenUrl="auth/login")

SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes
REFRESH_TOKEN_EXPIRE_DAYS = settings.refresh_token_expire_days

# Create a JWT ACCESS token
def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({
        "exp": expire,
        "type": "access"  # IMPORTANT: Mark as access token
    })

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# CREATE a REFRESH token (long-lived, stored in DB)
def create_refresh_token(user_id: int, db: Session):
    """
    Creates a refresh token and stores it in the database.
    Returns the token string.
    """
    # Generate a cryptographically secure random token
    token = secrets.token_urlsafe(32)
    
    # Calculate expiration (30 days from now)
    expires_at = datetime.now(timezone.utc) + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    
    # Create database record
    db_token = models.RefreshToken(
        user_id=user_id,
        token=token,
        expires_at=expires_at
    )
    
    db.add(db_token)
    db.commit()
    db.refresh(db_token)
    
    return token

# VERIFY a REFRESH token
def verify_refresh_token(token: str, db: Session):
    """
    Verifies a refresh token is valid:
    - Exists in database
    - Not revoked
    - Not expired
    Returns user_id if valid, None otherwise.
    """
    db_token = db.query(models.RefreshToken).filter(
        models.RefreshToken.token == token,
        models.RefreshToken.is_revoked == False,
        models.RefreshToken.expires_at > datetime.now(timezone.utc)
    ).first()

    if not db_token:
        return None
    
    return db_token.user_id

# REVOKE a refresh token (for logout)
def revoke_refresh_token(token: str, db: Session):
    """
    Marks a refresh token as revoked.
    Only finds tokens that are NOT already revoked.
    """
    db_token = db.query(models.RefreshToken).filter(
        models.RefreshToken.token == token,
        models.RefreshToken.is_revoked == False  # ← Only find non-revoked tokens
    ).first()
    
    if not db_token:
        return False  # Token not found OR already revoked
    
    # Token exists and is not revoked
    db_token.is_revoked = True
    db.commit()
    return True

# REVOKE ALL refresh tokens for a user (for password change, etc.)
def revoke_all_user_tokens(user_id: int, db: Session):
    """
    Revokes all refresh tokens for a specific user.
    Useful when user changes password or needs to logout everywhere.
    """
    db.query(models.RefreshToken).filter(
        models.RefreshToken.user_id == user_id,
        models.RefreshToken.is_revoked == False
    ).update({"is_revoked": True})
    db.commit()

# Verify and decode a JWT token
def verify_access_token(token: str, credentials_exception):
    try:
        # Decode the JWT token and extract the payload
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        # print(payload)
        user_id = payload.get("user_id")
        token_type = payload.get("type")
        
        # IMPORTANT: Make sure it's an access token, not a refresh token!
        if token_type != "access":
            raise credentials_exception
        
        if user_id is None:
            raise credentials_exception
        
        token_data = schemas.TokenData(id=int(user_id), type=token_type)
        
    except jwt.PyJWTError:
        raise credentials_exception
    return token_data

# Dependency to get the current user based on the token
def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(database.get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    token_data = verify_access_token(token, credentials_exception)
    user = db.query(models.User).filter(models.User.id == token_data.id).first()
    if user is None:
        raise credentials_exception
    return user 