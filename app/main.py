from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from . import models
from .database import engine
from .routers import user, post, auth, vote
from .config import settings

# create database schema
# not needed since we now use alembic
# models.Base.metadata.create_all(bind=engine)

# create app
app = FastAPI()

# CORS settings
origins = [] # no domain except local may access the API
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# include routers created within individual router files
app.include_router(auth.router)
app.include_router(user.router)
app.include_router(post.router)
app.include_router(vote.router)

# add home route for welcoming
@app.get("/")
def root():
    return {"message": "Welcome to FastAPI Social App"}