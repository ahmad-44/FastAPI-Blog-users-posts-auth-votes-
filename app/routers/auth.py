from fastapi import APIRouter, Depends, HTTPException
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from .. import models, oauth2
from ..database import get_db
from ..utils import verify_password
from ..schemas import Token

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"] # to structure the docs
)

@router.post("/login", response_model=Token)
def login(input_user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    # find user by email and store in db_user if exists
    db_user_credentials = db.query(models.User).filter(models.User.email == input_user_credentials.username).first()

    # if user not found, raise 404
    if db_user_credentials is None:
        raise HTTPException(status_code=404, detail="User not found")
    
    # verify password by comparing hashed passwords
    if not verify_password(input_user_credentials.password, db_user_credentials.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    #create and return a token 
    access_token = oauth2.create_access_token(data={"user_id": db_user_credentials.id})
   
    return {"access_token": access_token, "token_type": "bearer"}   