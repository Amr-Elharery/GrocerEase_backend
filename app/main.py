from fastapi import FastAPI
from api.routes.auth import router as auth_router
from core.database import engine, Base
from models.user import User

# Create database tables on startup
Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(auth_router)