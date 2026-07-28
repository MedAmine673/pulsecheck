import asyncio
import time
from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.scheduler import run_scheduler
from app.database import create_db_and_tables
from app.routers import monitors


def wait_for_db():
    """Retry DB connection until it's ready (important for Docker)."""
    for _ in range(10):
        try:
            create_db_and_tables()
            return
        except Exception:
            time.sleep(1)
    raise Exception("Database not ready after multiple attempts")


async def safe_scheduler():
    """Run scheduler safely so crashes are visible."""
    try:
        await run_scheduler()
    except Exception as e:
        print(f"Scheduler crashed: {e}")


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup logic
    wait_for_db()
    asyncio.create_task(safe_scheduler())

    yield  # <-- app is now running

    # Shutdown logic (optional for now)
    # You could add cleanup here later


app = FastAPI(lifespan=lifespan)


@app.get("/health")
def health():
    return {"status": "ok"}


app.include_router(monitors.router)