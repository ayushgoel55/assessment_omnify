from fastapi import FastAPI

from src.api.booking import booking_router
from src.api.classes import class_router
from src.api.user_creation import user_router
from src.models.db_connection import Base

app=FastAPI()

@app.get("/")
def home_page():
    return "welcome to the booking app"

app.include_router(class_router)
app.include_router(booking_router)
app.include_router(user_router)
