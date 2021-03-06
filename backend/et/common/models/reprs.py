from typing import Optional, List

from pydantic import BaseModel


class Event(BaseModel):
    event_id: str
    context_id: str
    span_id: str
    trace_id: str
    name: str
    created_at: float
    elapsed: float
    service_name: str

    # 'ok' or 'exception'
    status: Optional[str] = None

    error_msg: Optional[str] = None
    context: Optional[dict] = None

    # root span doesn't have a parent
    child_of: Optional[str] = None


class EventWithChildren(BaseModel):
    event: Event
    children: List['EventWithChildren'] = None


# self-referencing only works in python 3.7+
EventWithChildren.update_forward_refs()
