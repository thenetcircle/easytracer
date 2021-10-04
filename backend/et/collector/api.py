from http import HTTPStatus

from loguru import logger

from et.collector.cassandra import CassandraHandler
from et.collector.models.event_repr import Event
from et.collector.validator import Validator
from et.utils.exceptions import ParseError, ValidationError, CollectorException
import logging

logging.getLogger("cassandra").setLevel(logging.INFO)


class CollectorApi:
    def __init__(self, env):
        self.storage = CassandraHandler(env)

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
            self.storage.save(event)

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
