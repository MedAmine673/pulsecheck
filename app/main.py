import asyncio
from fastapi import FastAPI

from app.scheduler import run_scheduler
from app.database import create_db_and_tables
from app.routers import monitors

app = FastAPI()


@app.on_event("startup")
async def on_startup():
    create_db_and_tables()
    asyncio.create_task(run_scheduler())


@app.get("/health")
def health():
    return {"status": "ok"}


app.include_router(monitors.router)