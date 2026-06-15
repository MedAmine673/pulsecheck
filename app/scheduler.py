import asyncio
import datetime
import time
import httpx

from sqlmodel import Session, select

from database import engine
from models import Monitor, CheckResult


async def check_monitor(client, monitor):
    start = time.time()

    try:
        response = await client.get(monitor.url, timeout=5.0)
        response_time = int((time.time() - start) * 1000)

        return CheckResult(
            monitor_id=monitor.id,
            status_code=response.status_code,
            response_time=response_time,
            timestamp=datetime.datetime.utcnow(),
            is_up=response.status_code < 400
        )

    except Exception:
        return CheckResult(
            monitor_id=monitor.id,
            status_code=0,
            response_time=0,
            timestamp=datetime.datetime.utcnow(),
            is_up=False
        )


async def check_once():
    # 1. Get monitors (still sync DB)
    with Session(engine) as session:
        monitors = session.exec(select(Monitor)).all()

    # 2. Create async HTTP client
    async with httpx.AsyncClient() as client:
        tasks = [check_monitor(client, m) for m in monitors]

        # 3. Run all requests concurrently
        results = await asyncio.gather(*tasks)

    # 4. Save results (sync DB again)
    with Session(engine) as session:
        for result in results:
            session.add(result)

        session.commit()


async def run_scheduler():
    while True:
        print("Running checks...")
        await check_once()
        await asyncio.sleep(60)