from fastapi import FastAPI, Depends
from sqlmodel import Session, select

from database import create_db_and_tables, get_session
from models import Monitor

app = FastAPI()

@app.on_event("startup")
def on_startup():
    create_db_and_tables()


@app.get("/")
def read_root():
    return {"message": "Pulsecheck API is running"}


@app.post("/monitors")
def create_monitor(url: str, session: Session = Depends(get_session)):
    monitor = Monitor(url=url)

    session.add(monitor)
    session.commit()
    session.refresh(monitor)

    return monitor


@app.get("/monitors")
def get_monitors(session: Session = Depends(get_session)):
    monitors = session.exec(select(Monitor)).all()
    return monitors