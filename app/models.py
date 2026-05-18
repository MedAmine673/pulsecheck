import datetime


class Monitor:
    id: int
    url: str

class CheckResult:
    id: int
    monitor_id: int
    status_code: int
    response_time: int
    timestamp: datetime
    is_up: bool