import time
import datetime
import httpx

from sqlmodel import Session, select

from database import engine
from models import Monitor, CheckResult


def check_once():
    with Session(engine) as session:
        monitors = session.exec(select(Monitor)).all()

        for monitor in monitors:
            start = time.time()

            try:
                response = httpx.get(monitor.url, timeout=5.0)
                response_time = int((time.time() - start) * 1000)

                result = CheckResult(
                    monitor_id=monitor.id,
                    status_code=response.status_code,
                    response_time=response_time,
                    timestamp=datetime.datetime.utcnow(),
                    is_up=response.status_code < 400
                )

            except Exception:
                result = CheckResult(
                    monitor_id=monitor.id,
                    status_code=0,
                    response_time=0,
                    timestamp=datetime.datetime.utcnow(),
                    is_up=False
                )

            session.add(result)

        session.commit()


def run_scheduler():
    while True:
        print("Running checks...")
        check_once()
        time.sleep(60)  