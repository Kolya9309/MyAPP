from pydantic import BaseModel
from datetime import date

class MealBase(BaseModel):
    name: str
    calories: float
    date: date

class MealCreate(MealBase):
    pass

class Meal(MealBase):
    id: int

    class Config:
        orm_mode = True

class Stats(BaseModel):
    total_meals: int
    total_calories: float

class LoginRequest(BaseModel):
    username: str
    password: str