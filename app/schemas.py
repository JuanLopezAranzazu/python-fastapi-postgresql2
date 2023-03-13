from pydantic import BaseModel
from datetime import datetime
from typing import Optional

# schema para usuario

class UserCreate(BaseModel):
  email: str
  password: str
  
class User(UserCreate):
  id: int
  created_at: datetime
 

  class Config:
    orm_mode = True
    

class UserOut(BaseModel):
  User: User
  number_posts: int

  class Config:
    orm_mode = True

# schema para post

class PostCreate(BaseModel):
  title: str
  content: str
  
class Post(PostCreate):
  id: int
  user_id: int
  created_at: datetime

  class Config:
    orm_mode = True    
    

class PostOut(BaseModel):
  Post: Post
  User: User

  class Config:
    orm_mode = True   

# schemas para token

class Token(BaseModel):
  access_token: str
  token_type: str


class TokenData(BaseModel):
  id: Optional[str] = None

