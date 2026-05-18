from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List
import datetime



class Monitor(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    url: str
    results: List["CheckResult"] = Relationship(back_populates="monitor")


class CheckResult(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    monitor_id: int = Field(foreign_key="monitor.id", ondelete="CASCADE")
    status_code: int
    response_time: int
    timestamp: datetime.datetime = Field(default_factory=datetime.datetime.utcnow)
    is_up: bool
    monitor: Optional[Monitor] = Relationship(back_populates="results")