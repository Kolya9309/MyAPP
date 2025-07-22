from fastapi import FastAPI
from . import models, database
from .auth import routes as auth_routes

models.Base.metadata.create_all(bind=database.engine)

app = FastAPI(title="MyAPP")

app.include_router(auth_routes.router, prefix="/auth", tags=["auth"])
