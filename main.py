from fastapi import FastAPI # type: ignore
from routes import user_routes
from database import engine,Base
import models

app = FastAPI(title="ngms")

Base.metadata.create_all(bind=engine) #we are initializing the tables at app loading level
app.include_router(user_routes.router)
