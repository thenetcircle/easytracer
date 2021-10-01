from loguru import logger

import arrow
from et.collector.models.event import Event


class CassandraHandler:
    def __init__(self):
        # TODO: env
        pass

    def save(self, event: Event):
        event_dict = event.dict()

        # convert timestamp (float) to datetime object
        event_dict["created_at"] = arrow.get(event_dict["created_at"]).datetime

        # event_model = EventModel(**event_dict)
        logger.debug(f"saving to cassandra {event_dict}")
