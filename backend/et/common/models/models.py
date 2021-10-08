from cassandra.cqlengine.columns import DateTime, Float
from cassandra.cqlengine.columns import Text
from cassandra.cqlengine.columns import UUID
from cassandra.cqlengine.models import Model


class EventModel(Model):
    __table_name__ = "events"

    event_id = Text(
        required=True,
        primary_key=True,
        partition_key=True
    )
    context_id = Text(
        required=True,
        primary_key=True
    )
    trace_id = UUID(
        required=True,
        primary_key=True
    )
    span_id = UUID(
        required=True,
        primary_key=True
    )

    service_name = Text(
        required=True
    )
    created_at = DateTime(
        required=True
    )
    elapsed = Float(
        required=True
    )
    child_of = UUID(
        required=False
    )
    context = Text(
        required=False
    )

    name = Text(
        required=True
    )
    status = Text(
        required=False
    )
    error_msg = Text(
        required=False
    )
