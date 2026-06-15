from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from typing import List
import datetime

from database import get_session
from models import Monitor, CheckResult

router = APIRouter(prefix="/monitors", tags=["Monitors"])

from sqlmodel import SQLModel


class MonitorCreate(SQLModel):
    url: str

@router.post("/", response_model=Monitor)
def create_monitor(
    data: MonitorCreate,
    session: Session = Depends(get_session)
):
    monitor = Monitor(url=data.url)

    session.add(monitor)
    session.commit()
    session.refresh(monitor)

    return monitor

@router.get("/", response_model=List[Monitor])
def get_monitors(session: Session = Depends(get_session)):
    return session.exec(select(Monitor)).all()

@router.get("/{monitor_id}/history", response_model=List[CheckResult])
def get_history(
    monitor_id: int,
    session: Session = Depends(get_session)
):
    monitor = session.get(Monitor, monitor_id)

    if not monitor:
        raise HTTPException(status_code=404, detail="Monitor not found")

    results = session.exec(
        select(CheckResult)
        .where(CheckResult.monitor_id == monitor_id)
        .order_by(CheckResult.timestamp.desc())
    ).all()

    return results

@router.delete("/{monitor_id}")
def delete_monitor(monitor_id: int, session: Session = Depends(get_session)):
    monitor = session.get(Monitor, monitor_id)

    if not monitor:
        raise HTTPException(status_code=404, detail="Monitor not found")

    try:
        session.delete(monitor)
        session.commit()
        return {"message": "Monitor deleted successfully"}

    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    
@router.get("/health")
def health():
    return {"status": "ok"}