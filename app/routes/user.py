from fastapi import APIRouter, HTTPException, Depends, status
from .. import models, schemas
from passlib.context import CryptContext
from ..database import get_db
from sqlalchemy.orm import Session
from typing import List
from sqlalchemy import func

router = APIRouter(
  prefix="/users",
  tags=["users"]
)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# http://127.0.0.1:8000/users

# consultar todos los usuarios con el numero de posts creados

@router.get("/", response_model=List[schemas.UserOut])
async def get_users(db: Session = Depends(get_db)):
  # return db.query(models.User).all()
  
  users = db.query(models.User, func.count(models.Post.id).label("number_posts")).join(
    models.Post, models.Post.user_id == models.User.id).group_by(models.User.id).all()
  return users

# crear usuarios

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):

    user_found = db.query(models.User).filter(models.User.email == user.email).first()
    
    if user_found != None:
      raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                          detail="El usuario ya existe")
  
    hashed_password = pwd_context.hash(user.password)
    user.password = hashed_password

    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user
