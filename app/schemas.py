from pydantic import BaseModel, EmailStr, Field
from datetime import datetime
# Pydantic model for request body validation
class PostBase(BaseModel):
    title: str
    content: str
    is_published: bool = True

class PostCreate(PostBase):
    pass

# for response sending
class Post(PostBase):
    id: int
    created_at: datetime
    owner: 'UserResponse'  # Forward reference
    class Config:
        from_attributes = True # convert SQLAlchemy models to Pydantic models in dict formtat. it produces {"id": 1, "title": "sample", ...} from [<sqlalchemy object>]

# for response with votes
class PostWithVotes(BaseModel):
    Post: Post  # Nested Post object
    votes: int  # Vote count
    
    class Config:
        from_attributes = True


class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

# for token response
class Token(BaseModel):
    access_token: str
    token_type: str

# for token data
class TokenData(BaseModel):
    id: int

class Vote(BaseModel):
    post_id: int
    dir: int = Field(ge=0, le=1, description="1 for upvote, 0 for remove vote") # Field is used to add metadata to the field