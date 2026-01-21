from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from .. import models, oauth2
from ..database import get_db
from ..utils import verify_password
from ..schemas import Token, RefreshRequest, LogoutRequest

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"] # to structure the docs
)

@router.post("/login", response_model=Token)
def login(input_user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    """
    Returns both the access and refresh tokens
    """
    
    # find user by email and store in db_user_credentials if exists
    db_user_credentials = db.query(models.User).filter(models.User.email == input_user_credentials.username).first()

    # if user not found, raise 404
    if db_user_credentials is None:
        raise HTTPException(status_code=404, detail="User not found")
    
    # verify password by comparing hashed passwords
    if not verify_password(input_user_credentials.password, db_user_credentials.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    # Create ACCESS token (short-lived)
    access_token = oauth2.create_access_token(data={"user_id": db_user_credentials.id})
    
    # Create REFRESH token (long-lived, 30 days, stored in DB)
    refresh_token = oauth2.create_refresh_token(db_user_credentials.id, db)

    #Return BOTH tokens
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }  

@router.post("/refresh", response_model=Token)
def refresh_token(request: RefreshRequest, db: Session = Depends(get_db)):
    """
    Refresh endpoint: Exchange a valid refresh token for a new access token.
    Also rotates the refresh token for added security.
    """
    # Verify the refresh token
    user_id = oauth2.verify_refresh_token(request.refresh_token, db)
    
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired refresh token"
        )
    
    # Create NEW access token
    access_token = oauth2.create_access_token(data={"user_id": user_id})
    
    # OPTIONAL: Rotate refresh token (revoke old, create new)
    # This is more secure but means user needs to store the new refresh token
    oauth2.revoke_refresh_token(request.refresh_token, db)
    new_refresh_token = oauth2.create_refresh_token(user_id, db)
    
    # Return new tokens
    return {
        "access_token": access_token,
        "refresh_token": new_refresh_token,
        "token_type": "bearer"
    }

# logout the user on the current device
@router.post("/logout")
def logout(request: LogoutRequest, db: Session = Depends(get_db)):
    """
    Logout endpoint: Revokes the refresh token.
    """
    success = oauth2.revoke_refresh_token(request.refresh_token, db)
    
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Refresh token not found"
        )
    
    return {"message": "Successfully logged out"}


@router.post("/logout-all")
def logout_all(current_user: models.User = Depends(oauth2.get_current_user), db: Session = Depends(get_db)):
    """
    Logout from all devices: Revokes ALL refresh tokens for the current user.
    Requires a valid access token.
    """
    oauth2.revoke_all_user_tokens(current_user.id, db)
    
    return {"message": "Successfully logged out from all devices"}