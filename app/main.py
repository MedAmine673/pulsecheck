from fastapi import FastAPI
from database import create_db_and_tables
import models

from routers import monitors

app = FastAPI()

@app.on_event("startup")
def on_startup():
    create_db_and_tables()

app.include_router(monitors.router)