from fastapi import APIRouter, HTTPException, Depends, status, Response
from .. import models, schemas
from ..database import get_db
from sqlalchemy.orm import Session
from typing import List
from ..middlewares import oauth2

router = APIRouter(
  prefix="/posts",
  tags=["posts"]
)

# http://127.0.0.1:8000/posts

# consultar todos los posts

@router.get("/", response_model=List[schemas.PostOut])
async def get_posts(db: Session = Depends(get_db)):
  # return db.query(models.Post).filter(models.Post.user_id == current_user.id).all()
  
  posts = db.query(models.Post, models.User).join(
    models.User, models.User.id == models.Post.user_id).all()
  return posts

# consultar todos los posts del usuario autenticado

@router.get("/by_user", response_model=List[schemas.Post])
async def get_posts(db: Session = Depends(get_db), 
                    current_user: int = Depends(oauth2.get_current_user)):
  return db.query(models.Post).filter(models.Post.user_id == current_user.id).all()

# consultar un post

@router.get("/{id}", response_model=schemas.Post)
async def get_post(db: Session = Depends(get_db), 
                    current_user: int = Depends(oauth2.get_current_user)):
  post_query = db.query(models.Post).filter(models.Post.id == id)
  
  post = post_query.first()
  
  if post == None:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail="El post no existe")
  
  if post.user_id != current_user.id:
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                        detail="No estas autorizado")
  
  return post

# crear posts

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
async def create_post(post: schemas.PostCreate, db: Session = Depends(get_db), 
                 current_user: int = Depends(oauth2.get_current_user)):
    new_post = models.Post(user_id=current_user.id, **post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return new_post
  
# editar posts
  
@router.put("/{id}", response_model=schemas.Post)
def update_post(id: int, updated_post: schemas.PostCreate, db: Session = Depends(get_db), 
                current_user: int = Depends(oauth2.get_current_user)):

    post_query = db.query(models.Post).filter(models.Post.id == id)

    post = post_query.first()

    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="El post no existe")

    if post.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="No estas autorizado")

    post_query.update(updated_post.dict(), synchronize_session=False)

    db.commit()

    return post_query.first()

# eliminar posts

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db), 
                current_user: int = Depends(oauth2.get_current_user)):

    post_query = db.query(models.Post).filter(models.Post.id == id)

    post = post_query.first()

    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="El post no existe")

    if post.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="No estas autorizado")

    post_query.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)

