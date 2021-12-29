import json
import logging as logging_system
import socket
from contextlib import contextmanager
from time import perf_counter
from typing import Optional
from uuid import uuid4 as uuid

import arrow

from easytracer.config_keys import ConfigKeys

logger = logging_system.getLogger(__name__)


def utcnow_ts():
    # force the use of milliseconds instead microseconds
    now = arrow.utcnow()
    seconds = now.int_timestamp
    ms = now.format("SSS")

    return round(float(f"{seconds}.{ms}"), 3)


class Span:
    def __init__(
            self,
            service_name: str,
            name: str,
            child_of=None,
            span_id: Optional[str] = None,
            trace_id: Optional[str] = None,
            event_id: Optional[str] = None,
            context_id: Optional[str] = None
    ):
        self.name: str = name
        self.child_of: Span = child_of
        self.service_name = service_name
        self.created_at = utcnow_ts()
        self.context: Optional[dict] = None

        self.span_id = span_id
        if self.span_id is None:
            self.span_id: str = str(uuid())

        if child_of is None:
            self.event_id = event_id
            self.context_id = context_id
            self.trace_id = trace_id

            if self.event_id is None:
                self.event_id = str(uuid())
                logger.warning(f"no event_id specified, generating one: {self.event_id}")

            if self.context_id is None:
                self.context_id = self.event_id

            if self.trace_id is None:
                self.trace_id = str(uuid())
        else:
            self.trace_id = child_of.trace_id
            self.event_id = child_of.event_id
            self.context_id = child_of.context_id

    def log_kv(self, kv: dict):
        self.context = kv

    def to_event(self, elapsed: float, status, error_msg):
        event = {
            "span_id": self.span_id,
            "name": self.name,
            "created_at": self.created_at,
            "service_name": self.service_name,
            "trace_id": self.trace_id,
            "event_id": self.event_id,
            "context_id": self.context_id,
            "status": status,
            "elapsed": elapsed,
            "error_msg": error_msg
        }

        if self.child_of:
            event["child_of"] = self.child_of.span_id

        if self.context:
            event["context"] = self.context
        else:
            event["context"] = dict()

        return event

    def __str__(self):
        if self.child_of is None:
            child_of = ""
        else:
            child_of = f"id={self.child_of.span_id},name={self.child_of.name}"

        return f"[trace_id={self.trace_id},span_id={self.span_id},name={self.name},child_of=[{child_of}]]"


class Tracer:
    def __init__(self, service_name: str, logging: bool, sampler: float, config: dict):
        self.service_name = service_name
        self.logging = logging
        self.sampler = sampler

        if 'mock' in config and config['mock']:
            self.udp_socket = None
            logger.warning("mocking tracing as per config")
        else:
            agent_socket = config.get(ConfigKeys.AGENT_SOCKET, "/var/run/easytracer/easytracer.sock")
            self.udp_socket = socket.socket(socket.AF_UNIX, socket.SOCK_DGRAM)
            self.udp_socket.connect(agent_socket)

    def report_span(self, span: Span, elapsed: float, status: str, error_msg: str):
        if self.udp_socket is None:
            return

        if self.logging:
            logger.info(f"[{status}] elapsed {elapsed:.4f}s, reporting span: {span}")

        try:
            binary_event = bytes(json.dumps(span.to_event(elapsed, status, error_msg)), "utf-8")
        except Exception as e:
            logger.error(f"could not convert span to event: {str(e)}")
            return

        try:
            self.udp_socket.send(binary_event)
        except Exception as e:
            logger.error(f"could not send event to socket: {str(e)}")

    @contextmanager
    def start_span(
            self,
            name: str,
            child_of: Optional[Span] = None,
            event_id: Optional[str] = None,
            context_id: Optional[str] = None
    ):
        start = perf_counter()
        span = Span(self.service_name, name, child_of, event_id=event_id, context_id=context_id)
        status = "ok"
        error_msg = ""

        try:
            yield span
        except Exception as e:
            status = "exception"
            error_msg = str(e)

        end = perf_counter()
        elapsed = end - start
        self.report_span(span, elapsed, status, error_msg)
