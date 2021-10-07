import arrow
from cassandra.cluster import PlainTextAuthProvider
from cassandra.cqlengine import connection
from cassandra.cqlengine.management import sync_table
from loguru import logger

from et.common.models.models import EventModel
from et.common.models.reprs import Event
from et.utils.config import ConfigKeys
from et.utils.exceptions import ParseError


def to_ts(ds):
    # millis not micros
    return round(arrow.get(ds).float_timestamp, 3)


class CassandraHandler:
    def __init__(self, env):
        self.env = env
        self.setup_tables()

    def setup_tables(self):
        key_space = self.env.config.get(ConfigKeys.KEY_SPACE, domain=ConfigKeys.STORAGE)
        hosts = self.env.config.get(ConfigKeys.HOST, domain=ConfigKeys.STORAGE)
        hosts = hosts.split(",")

        kwargs = {
            "default_keyspace": key_space,
            "protocol_version": 3,
            "retry_connect": True
        }

        username = self._get_from_conf(ConfigKeys.USERNAME, ConfigKeys.STORAGE)
        password = self._get_from_conf(ConfigKeys.PASSWORD, ConfigKeys.STORAGE)

        if password is not None:
            auth_provider = PlainTextAuthProvider(
                username=username,
                password=password,
            )
            kwargs["auth_provider"] = auth_provider

        connection.setup(hosts, **kwargs)

        sync_table(EventModel)

    def _get_from_conf(self, key, domain):
        if key not in self.env.config.get(domain):
            return None

        value = self.env.config.get(key, domain=domain)
        if value is None or not len(value.strip()):
            return None

        # no configured secret for this key
        if value.startswith("$"):
            return None

        return value

    def get_events(self, event_id: str):
        events = (
            EventModel.objects(
                EventModel.event_id == event_id
            )
            .all()
        )

        return [CassandraHandler.event_base_from_entity(event) for event in events]

    def save_event(self, event: Event):
        event_dict = event.dict()

        # convert timestamp (float) to datetime object
        event_dict["created_at"] = arrow.get(event_dict["created_at"]).datetime

        logger.debug(f"saving to cassandra {event_dict}")

        try:
            EventModel.create(**event_dict)
        except Exception as e:
            logger.error(f"could not save model to cassandra: {str(e)}")
            raise ParseError(e)

    @staticmethod
    def event_base_from_entity(event: EventModel):
        return Event(
            event_id=str(event.event_id),
            context_id=event.context_id,
            span_id=str(event.span_id),
            trace_id=str(event.trace_id),
            elapsed=round(event.elapsed * 1000, 3),  # return milliseconds
            name=event.name,
            created_at=to_ts(event.created_at),
            service_name=event.service_name,
            status=event.status,
            error_msg=event.error_msg,
            context=event.context,
            child_of=event.child_of
        )
