import sys

from starlette.requests import Request
from loguru import logger

from backend.etcollector.cassandra import CassandraHandler
from backend.etcollector.validator import Validator
from backend.utils.exceptions import ParseError, ValidationError


class CollectorApi:
    def __init__(self):
        self.storage = CassandraHandler()

    async def post(self, request: Request):
        # TODO: use pydantic not the raw request
        data = await request.json()

        try:
            Validator.validate(data)
        except ValidationError as e:
            logger.error(e)
            return

        try:
            # CassandraHandler will convert pydantic to ORM
            self.storage.save(data)
        except ParseError as e:
            logger.error(e)
            logger.debug(data)
        except Exception as e:
            logger.error(e)
            logger.debug(data)
            logger.exception(sys.exc_info())
