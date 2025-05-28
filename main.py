from fastapi import FastAPI 
from routes import user_routes
from database import engine,Base
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI(title="ngms")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods: GET, POST, PUT, DELETE, etc.
    allow_headers=["*"],  # Allows all headers
)

Base.metadata.create_all(bind=engine) #we are initializing the tables at app loading level
app.include_router(user_routes.router)


