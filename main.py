from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from datetime import date

app = FastAPI()

# --- Модели ---
class Meal(BaseModel):
    id: int
    name: str
    calories: int
    date: date

class MealCreate(BaseModel):
    name: str
    calories: int
    date: date

class Stats(BaseModel):
    total_meals: int
    total_calories: int

class LoginRequest(BaseModel):
    username: str
    password: str

# --- Псевдо-хранилище ---
db: List[Meal] = []
id_counter = 1

# --- Эндпоинты ---
@app.get("/")
def root():
    return {"message": "API is working!"}

@app.post("/meals", response_model=Meal)
def add_meal(meal: MealCreate):
    global id_counter
    new_meal = Meal(id=id_counter, **meal.dict())
    db.append(new_meal)
    id_counter += 1
    return new_meal

@app.get("/meals", response_model=List[Meal])
def get_meals():
    return db

@app.delete("/meals/{meal_id}")
def delete_meal(meal_id: int):
    global db
    db = [m for m in db if m.id != meal_id]
    return {"message": "Deleted"}

@app.get("/stats", response_model=Stats)
def get_stats(start_date: Optional[date] = None, end_date: Optional[date] = None):
    filtered = db
    if start_date:
        filtered = [m for m in filtered if m.date >= start_date]
    if end_date:
        filtered = [m for m in filtered if m.date <= end_date]
    return Stats(
        total_meals=len(filtered),
        total_calories=sum(m.calories for m in filtered)
    )

@app.post("/login")
def login(req: LoginRequest):
    if req.username == "nikolay" and req.password == "123456":
        return {"token": "fake-jwt-token"}
    raise HTTPException(status_code=401, detail="Invalid credentials")
