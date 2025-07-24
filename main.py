from fastapi import FastAPI

import models
import database
from auth import routes as auth_routes
from meals import models as meal_models, routes as meal_routes

models.Base.metadata.create_all(bind=database.engine)
meal_models.Base.metadata.create_all(bind=database.engine)

app = FastAPI(title="MyAPP")

app.include_router(auth_routes.router, prefix="/auth", tags=["auth"])
app.include_router(meal_routes.router, prefix="/meals", tags=["meals"])
