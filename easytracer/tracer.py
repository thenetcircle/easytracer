import logging
from contextlib import contextmanager
from datetime import datetime as dt
from time import perf_counter
from typing import Optional
from uuid import uuid4 as uuid

logger = logging.getLogger(__name__)


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
        self.created_at = dt.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")
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

    def to_event(self):
        event = {
            "span_id": self.span_id,
            "name": self.name,
            "created_at": self.created_at,
            "service_name": self.service_name,
            "trace_id": self.trace_id,
            "child_of": "",
            "context": dict()
        }

        if self.child_of:
            event["child_of"] = self.child_of.span_id

        if self.context:
            event["context"] = self.context

    def __str__(self):
        if self.child_of is None:
            child_of = ""
        else:
            child_of = f"id={self.child_of.span_id},name={self.child_of.name}"

        return f"[trace_id={self.trace_id},span_id={self.span_id},name={self.name},child_of=[{child_of}]]"


class Tracer:
    def __init__(self, service_name: str, logging: bool, sampler: float):
        self.service_name = service_name
        self.logging = logging
        self.sampler = sampler

    def report_span(self, span: Span, elapsed: float):
        if self.logging:
            logger.info(f"elapsed {elapsed:.4f}s, reporting span: {span}")

            # TODO: send udp to collector
            logger.debug(span.to_event())

    @contextmanager
    def start_span(self, name: str, child_of: Optional[Span]):
        start = perf_counter()
        span = Span(self.service_name, name, child_of)

        yield span

        end = perf_counter()
        elapsed = end - start
        self.report_span(span, elapsed)
