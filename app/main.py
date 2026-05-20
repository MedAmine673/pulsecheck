import threading

from fastapi import FastAPI
from database import create_db_and_tables
from routers import monitors
from scheduler import run_scheduler

app = FastAPI()

@app.on_event("startup")
def on_startup():
    create_db_and_tables()
    
    thread = threading.Thread(target=run_scheduler, daemon=True)
    thread.start()
app.include_router(monitors.router)