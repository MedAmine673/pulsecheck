import asyncio
from fastapi import FastAPI

from scheduler import run_scheduler
from database import create_db_and_tables
from routers import monitors

app = FastAPI()


@app.on_event("startup")
async def on_startup():
    create_db_and_tables()
    asyncio.create_task(run_scheduler())


app.include_router(monitors.router)