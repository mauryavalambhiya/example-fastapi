from fastapi.middleware.cors import CORSMiddleware
from . routers import post,user,auth,vote
from fastapi import Depends, FastAPI, Response , status, HTTPException
from psycopg2.extras import RealDictCursor
from sqlalchemy.orm import Session
from . import models,schemas,utils
from fastapi.middleware.cors import CORSMiddleware

# from typing import Optional, List
# from fastapi.params import Body
# from pydantic import BaseModel
# import uvicorn 
# import psycopg2
# from .database import SessionLocal, engine,get_db
# from .config import settings

# models.Base.metadata.create_all(bind=engine)

# Making app instance
app = FastAPI()

# origins = ["https://www.google.com"]
origins = ["*"]
# for public api origins=["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(user.router)
app.include_router(post.router)
app.include_router(auth.router)
app.include_router(vote.router)


@app.get("/")
def root():
    return {"massage" : "Hello world on root "}

# =========================================================================================
# =========================================================================================

