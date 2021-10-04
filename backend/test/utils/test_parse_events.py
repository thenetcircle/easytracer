from unittest import TestCase
from uuid import uuid4 as uuid

import arrow

from et.common.models.reprs import Event
from et.utils.parse_events import parse_events


def gen_event(event_id: str, child_of: str = None):
    return Event(
        event_id=event_id,
        context_id="1234",
        span_id=str(uuid()),
        trace_id=str(uuid()),
        name="test",
        created_at=arrow.utcnow().float_timestamp,
        service_name="test-service",
        status="ok",
        error_msg=None,
        context=None,
        child_of=child_of
    )


class TestParseEvents(TestCase):
    def setUp(self) -> None:
        pass

    def test_parse_one_root_event(self):
        events = [gen_event(str(uuid()))]
        parsed = parse_events(events)
        self.assertEqual(1, len(parsed))

    def test_parse_one_child(self):
        event_id = str(uuid())
        root_event = gen_event(event_id)
        events = [
            root_event,
            gen_event(event_id, child_of=root_event.span_id)
        ]

        parsed = parse_events(events)
        self.assertEqual(1, len(parsed))
        self.assertEqual(1, len(parsed[0].children))

    def test_parse_two_children(self):
        event_id = str(uuid())
        root_event = gen_event(event_id)
        events = [
            root_event,
            gen_event(event_id, child_of=root_event.span_id),
            gen_event(event_id, child_of=root_event.span_id),
        ]

        parsed = parse_events(events)
        self.assertEqual(1, len(parsed))
        self.assertEqual(2, len(parsed[0].children))
