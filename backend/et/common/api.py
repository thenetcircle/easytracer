import logging
from http import HTTPStatus
from typing import List

from loguru import logger

from et.collector.validator import Validator
from et.common.cassandra import CassandraHandler
from et.common.models.reprs import Event, EventWithChildren
from et.utils.exceptions import ParseError, ValidationError, CollectorException
from et.utils.parse_events import parse_events

logging.getLogger("cassandra").setLevel(logging.INFO)


class TracerApi:
    def __init__(self, env):
        self.storage = CassandraHandler(env)

    async def get(self, event_id: str) -> List[EventWithChildren]:
        events = self.storage.get_events(event_id)
        return parse_events(events)

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
