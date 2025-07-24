from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import date
from typing import List

from ..database import SessionLocal
from .. import models
from .models import Meal
from .schemas import MealCreate, MealOut
from ..auth.utils import jwt, SECRET_KEY, ALGORITHM
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="Invalid token")
        return username
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

@router.post("/", response_model=MealOut)
def add_meal(meal: MealCreate, db: Session = Depends(get_db), username: str = Depends(get_current_user)):
    user = db.query(models.User).filter(models.User.username == username).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    eaten_at = meal.eaten_at or date.today()
    db_meal = Meal(name=meal.name, calories=meal.calories, eaten_at=eaten_at, user_id=user.id)
    db.add(db_meal)
    db.commit()
    db.refresh(db_meal)
    return db_meal

@router.get("/", response_model=List[MealOut])
def get_meals(db: Session = Depends(get_db), username: str = Depends(get_current_user)):
    user = db.query(models.User).filter(models.User.username == username).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return db.query(Meal).filter(Meal.user_id == user.id).order_by(Meal.eaten_at.desc()).all()
