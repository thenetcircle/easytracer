from http import HTTPStatus

from loguru import logger

from et.common.cassandra import CassandraHandler
from et.common.models.reprs import Event, EventWithChildren
from et.collector.validator import Validator
from et.utils.exceptions import ParseError, ValidationError, CollectorException
import logging

logging.getLogger("cassandra").setLevel(logging.INFO)


class CollectorApi:
    def __init__(self, env):
        self.storage = CassandraHandler(env)

    async def get(self, event_id: str):
        events = self.storage.get_events(event_id)
        children_of = dict()
        root_event = None

        for event in events:
            if event.child_of is None:
                if root_event is not None:
                    logger.error(f"multiple root-events for event id {event_id}")
                root_event = event

            else:
                if event.span_id not in children_of.keys():
                    children_of[event.span_id] = list()
                children_of[event.span_id].append(event)

        return EventWithChildren(
            event=root_event,
            children=children_of[root_event.span_id]  # TODO: recursive
        )

    async def post(self, event: Event):
        try:
            Validator.validate(event)
        except ValidationError as e:
            raise CollectorException(
                status_code=HTTPStatus.BAD_REQUEST,
                parent=e,
                event=event
            )

        try:
            # CassandraHandler will convert pydantic to ORM
            self.storage.save_event(event)

        except ParseError as e:
            raise CollectorException(
                status_code=HTTPStatus.BAD_REQUEST,
                parent=e,
                event=event
            )

        except Exception as e:
            logger.exception(e)
            raise CollectorException(
                status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
                parent=e,
                event=event
            )
