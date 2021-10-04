from pydantic import BaseModel
from typing import Optional


class Event(BaseModel):
    span_id: str
    trace_id: str
    name: str
    created_at: str
    service_name: str

    # 'ok' or 'exception'
    status: str

    error_msg: Optional[str]
    context: Optional[dict]

    # root span doesn't have a parent
    child_of: Optional[str]
