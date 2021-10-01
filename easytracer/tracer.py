import json
import logging as logging_system
from contextlib import contextmanager
from time import perf_counter
from typing import Optional
from uuid import uuid4 as uuid

import socket

from easytracer.config import ConfigKeys
import arrow

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
            trace_id: Optional[str] = None
    ):
        self.name: str = name
        self.child_of: Span = child_of
        self.service_name = service_name
        self.created_at = utcnow_ts
        self.context: Optional[dict] = None

        self.span_id = span_id
        if self.span_id is None:
            self.span_id: str = str(uuid())

        if child_of is None:
            self.trace_id = trace_id
            if self.trace_id is None:
                self.trace_id = str(uuid())
        else:
            self.trace_id = child_of.trace_id

    def log_kv(self, kv: dict):
        self.context = kv

    def to_event(self, status, error_msg):
        event = {
            "span_id": self.span_id,
            "name": self.name,
            "created_at": self.created_at,
            "service_name": self.service_name,
            "trace_id": self.trace_id,
            "status": status,
            "error_msg": error_msg
        }

        if self.child_of:
            event["child_of"] = self.child_of.span_id
        if self.context:
            event["context"] = self.context

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

        agent_socket = config.get(ConfigKeys.AGENT_SOCKET, "/var/run/easytracer.sock")
        self.udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.udp_socket.connect(agent_socket)

    def report_span(self, span: Span, elapsed: float, status: str, error_msg: str):
        if self.logging:
            logger.info(f"[{status}] elapsed {elapsed:.4f}s, reporting span: {span}")

        binary_event = bytes(json.dumps(span.to_event(status, error_msg)), "utf-8")
        self.udp_socket.send(binary_event)

    @contextmanager
    def start_span(self, name: str, child_of: Optional[Span] = None):
        start = perf_counter()
        span = Span(self.service_name, name, child_of)
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
