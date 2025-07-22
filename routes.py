from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import SessionLocal
from .. import models
from . import schemas, utils

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/register", response_model=schemas.Token)
def register(user: schemas.UserCreate, db: Session = Depends(get_db)):
    existing = db.query(models.User).filter(models.User.username == user.username).first()
    if existing:
        raise HTTPException(status_code=400, detail="User already exists")
    hashed = utils.hash_password(user.password)
    db_user = models.User(username=user.username, hashed_password=hashed)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    token = utils.create_access_token(data={"sub": db_user.username})
    return {"access_token": token, "token_type": "bearer"}

@router.post("/login", response_model=schemas.Token)
def login(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.username == user.username).first()
    if not db_user or not utils.verify_password(user.password, db_user.hashed_password):
        raise HTTPException(status_code=400, detail="Invalid credentials")
    token = utils.create_access_token(data={"sub": db_user.username})
    return {"access_token": token, "token_type": "bearer"}
