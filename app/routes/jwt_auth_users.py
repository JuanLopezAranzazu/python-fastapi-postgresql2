from fastapi import APIRouter, HTTPException, Depends, status
from .. import models, schemas
from passlib.context import CryptContext
from ..database import get_db
from sqlalchemy.orm import Session
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from ..middlewares import oauth2

router = APIRouter(
  prefix="/authentication",
  tags=["authentication"]  
)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# http://127.0.0.1:8000/authentication

@router.post("/login", response_model=schemas.Token)
async def login(user_credentials: OAuth2PasswordRequestForm = Depends() ,db: Session = Depends(get_db)):
  user = db.query(models.User).filter(
        models.User.email == user_credentials.username).first()

  if not user:
      raise HTTPException(
          status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid Credentials")

  if not pwd_context.verify(user_credentials.password, user.password):
      raise HTTPException(
          status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid Credentials")

  # create a token
  access_token = oauth2.create_access_token(data={"user_id": user.id})

  return {"access_token": access_token, "token_type": "bearer"}
