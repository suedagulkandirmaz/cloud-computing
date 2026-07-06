from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from app.database import Base, engine, SessionLocal
from app.routes import router
from app.exception_handler import http_exception_handler

app = FastAPI()

app.add_exception_handler(Exception, http_exception_handler)

Base.metadata.create_all(bind=engine)

app.include_router(router)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()