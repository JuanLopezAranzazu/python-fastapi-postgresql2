from fastapi import FastAPI
from . import models
from .database import engine
from .config import settings

from .routes import jwt_auth_users, post, user

# models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# uvicorn app.main:app --reload
# http://127.0.0.1:8000

@app.get("/")
async def root():
  return { "message": "API CON AUTENTICACION" }

@app.get("/config/")
async def get_config():
  return {
    "access_token_expire_minutes": settings.access_token_expire_minutes,
    "database_name": settings.database_name
  }

# routes
app.include_router(jwt_auth_users.router)
app.include_router(post.router)
app.include_router(user.router)

