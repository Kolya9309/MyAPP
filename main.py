from fastapi import FastAPI
from routers import users
from database import Base, engine

app = FastAPI()

Base.metadata.create_all(bind=engine)

app.include_router(users.router)

@app.get("/")
def read_root():
    return {"message": "API is working!"}