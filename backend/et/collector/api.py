from http import HTTPStatus

from starlette.requests import Request
from loguru import logger

from et.collector.cassandra import CassandraHandler
from et.collector.validator import Validator
from et.utils.exceptions import ParseError, ValidationError, CollectorException


class CollectorApi:
    def __init__(self):
        self.storage = CassandraHandler()

    async def post(self, request: Request):
        # TODO: use pydantic not the raw request
        data = await request.json()

        try:
            Validator.validate(data)
        except ValidationError as e:
            raise CollectorException(
                status_code=HTTPStatus.BAD_REQUEST,
                parent=e,
                event=data
            )

        try:
            # CassandraHandler will convert pydantic to ORM
            self.storage.save(data)
        except ParseError as e:
            raise CollectorException(
                status_code=HTTPStatus.BAD_REQUEST,
                parent=e,
                event=data
            )

        except Exception as e:
            logger.exception(e)
            raise CollectorException(
                status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
                parent=e,
                event=data
            )
