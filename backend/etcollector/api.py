from starlette.requests import Request
from loguru import logger

from backend.etcollector.validator import EventValidator


class CollectorApi:
    def __init__(self):
        pass

    async def post(self, request: Request):
        event = await request.json()
        is_valid, error_msg = EventValidator.validate(event)

        if not is_valid:
            logger.error(f"event did not validate: {error_msg}")
            return
