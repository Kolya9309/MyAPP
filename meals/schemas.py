from pydantic import BaseModel
from datetime import date
from typing import Optional

class MealCreate(BaseModel):
    name: str
    calories: int
    eaten_at: Optional[date] = None

class MealOut(BaseModel):
    id: int
    name: str
    calories: int
    eaten_at: date

    class Config:
        orm_mode = True
